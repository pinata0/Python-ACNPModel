import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
import matplotlib.font_manager as fm

font_path = r'C:/Windows/Fonts/NanumGothic.ttf'
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)

# 하이퍼파라미터
SEQ_LENGTH = 20
EPOCHS = 100
LR = 0.001

# 데이터 로딩
df = pd.read_csv("./finance_collector/company_list/삼성전자.csv", encoding='utf-8')
df['날짜'] = pd.to_datetime(df['날짜'])
df = df.sort_values(by='날짜')
prices = df['시가'].values.reshape(-1, 1)
dates = df['날짜'].values

# 전체 길이
assert len(prices) == 1280

# 스케일링
scaler = MinMaxScaler()
prices_scaled = scaler.fit_transform(prices)

# 🔹 학습 데이터: 앞 1200일
train_data = prices_scaled[:1200]

# 시퀀스 생성 함수
def make_sequences(data, seq_len):
    x, y = [], []
    for i in range(len(data) - seq_len):
        x.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(x), np.array(y)

X_train, y_train = make_sequences(train_data, SEQ_LENGTH)

X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)

# 🔹 LSTM 모델
class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        return self.fc(out)

model = LSTMModel()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# 🔹 학습 루프
for epoch in range(EPOCHS):
    model.train()
    optimizer.zero_grad()
    output = model(X_train)
    loss = criterion(output, y_train)
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 10 == 0:
        print(f"[{epoch+1}/{EPOCHS}] Loss: {loss.item():.6f}")

# 🔹 예측: 마지막 80일 예측 (슬라이딩 윈도우 방식)
model.eval()
future_preds = []
input_seq = torch.tensor(prices_scaled[1200 - SEQ_LENGTH:1200], dtype=torch.float32).unsqueeze(0)

with torch.no_grad():
    for i in range(80):
        pred = model(input_seq)              # [1, 1]
        future_preds.append(pred.item())
        
        pred = pred.unsqueeze(2)             # [1, 1, 1]
        input_seq = torch.cat((input_seq[:, 1:, :], pred), dim=1)  # [1, 20, 1]

# 🔹 역정규화
future_preds = scaler.inverse_transform(np.array(future_preds).reshape(-1, 1))
real_future = prices[1200:]  # 실제 시가
future_dates = dates[1200:]

# 🔹 시각화
plt.figure(figsize=(12, 6))
plt.plot(future_dates, real_future, label='실제 시가')
plt.plot(future_dates, future_preds, label='예측 시가')
plt.title("LSTM 기반 주가 예측 (80일)")
plt.xlabel("날짜")
plt.ylabel("시가")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

from sklearn.metrics import mean_absolute_error, r2_score

r2 = r2_score(real_future, future_preds)
print(f"R²   (설명력):             {r2:.4f}")
