import os
import pandas as pd
from keyphrasetransformer import KeyPhraseTransformer

# 설정
INPUT_CSV = "krx_top_news_visible.csv"
SAVE_DIR = "extracted_by_date"

# 모델 초기화
kp = KeyPhraseTransformer()

# CSV 로드
df = pd.read_csv(INPUT_CSV)

# 날짜별 저장을 위한 딕셔너리
seen = {}

for _, row in df.iterrows():
    company = str(row["회사명"]).strip()
    title = str(row["뉴스제목"]).strip()
    date = str(row["날짜"]).strip()
    url = str(row["링크"]).strip()

    # 키워드 추출
    keywords = kp.get_key_phrases(title)
    label = ", ".join(keywords)

    if not label:
        continue

    # 중복 체크
    if date not in seen:
        seen[date] = set()
    if label in seen[date]:
        continue
    seen[date].add(label)

    # 날짜별 폴더 생성
    day_folder = os.path.join(SAVE_DIR, date)
    os.makedirs(day_folder, exist_ok=True)
    file_path = os.path.join(day_folder, f"{date}_summary.csv")

    # 결과 저장
    record = {
        "회사명": company,
        "사건내용": label,
        "날짜": date,
        "링크": url
    }
    pd.DataFrame([record]).to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False, encoding="utf-8-sig")

print("✅ 키워드 추출 및 날짜별 CSV 저장 완료")
