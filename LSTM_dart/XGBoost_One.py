import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import matplotlib.font_manager as fm

font_path = r'C:/Windows/Fonts/NanumGothic.ttf'
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)

# ✅ 설정
SEQ_LENGTH = 20

# ✅ 데이터 불러오기
df = pd.read_csv("./finance_collector/company_list/삼성전자.csv", encoding='utf-8')
df['날짜'] = pd.to_datetime(df['날짜'])
df = df.sort_values('날짜')

prices = df['시가'].values.reshape(-1, 1)
dates = df['날짜'].values

# ✅ 정규화
scaler = MinMaxScaler()
prices_scaled = scaler.fit_transform(prices)

# ✅ 시퀀스 생성
def create_dataset(data, seq_length):
    x, y = [], []
    for i in range(len(data) - seq_length):
        x.append(data[i:i + seq_length].flatten())
        y.append(data[i + seq_length][0])
    return np.array(x), np.array(y)

X_all, y_all = create_dataset(prices_scaled, SEQ_LENGTH)

# ✅ 학습/테스트 분리
train_X, test_X = X_all[:1200 - SEQ_LENGTH], X_all[1200 - SEQ_LENGTH:]
train_y, test_y = y_all[:1200 - SEQ_LENGTH], y_all[1200 - SEQ_LENGTH:]
test_dates = dates[1200:]

# ✅ XGBoost 학습
model = XGBRegressor(n_estimators=100, learning_rate=0.1)
model.fit(train_X, train_y)

# ✅ 예측
preds_scaled = model.predict(test_X)
preds = scaler.inverse_transform(preds_scaled.reshape(-1, 1))
real = scaler.inverse_transform(test_y.reshape(-1, 1))

# ✅ 평가
rmse = np.sqrt(mean_squared_error(real, preds))
print(f"RMSE: {rmse:.4f}")

# ✅ 시각화
plt.figure(figsize=(12, 6))
plt.plot(test_dates, real, label='실제 시가')
plt.plot(test_dates, preds, label='예측 시가')
plt.title("XGBoost 기반 주가 예측 (80일)")
plt.xlabel("날짜")
plt.ylabel("시가")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

from sklearn.metrics import mean_absolute_error, r2_score

r2 = r2_score(real, preds)
print(f"R²   (설명력):             {r2:.4f}")