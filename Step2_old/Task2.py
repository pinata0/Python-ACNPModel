# 📁 keyword_extractor.py (keybert_env에서 실행)

import pandas as pd
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
kw_model = KeyBERT(model)

df = pd.read_csv("krx_top_news_visible_full.csv")
records = []

for _, row in df.iterrows():
    content = str(row["본문"]).strip()
    if not content:
        continue
    keywords = kw_model.extract_keywords(content, top_n=3, keyphrase_ngram_range=(1, 3))
    label = ", ".join([kw[0] for kw in keywords]) or "이벤트"
    records.append({
        "회사명": row["회사명"],
        "날짜": row["날짜"],
        "사건내용": label
    })

pd.DataFrame(records).drop_duplicates(subset=["날짜", "사건내용"]).to_csv("extracted_events.csv", index=False, encoding="utf-8-sig")
print("✅ 키워드 추출 결과 저장 완료")
