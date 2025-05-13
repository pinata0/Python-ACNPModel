# 📁 articlebody_collector.py (main_env에서 실행)

import pandas as pd
import os, re, requests
from bs4 import BeautifulSoup

def sanitize_filename(s):
    return re.sub(r'[\/*?"<>|]', "_", s)

def extract_article_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text().strip() for p in paragraphs).strip()
    except:
        return ""

df = pd.read_csv("krx_top_news_visible.csv")
out = []

for i, row in df.iterrows():
    body = extract_article_text(row["링크"])
    if body:
        out.append({
            "회사명": row["회사명"],
            "날짜": row["날짜"],
            "뉴스제목": row["뉴스제목"],
            "링크": row["링크"],
            "본문": body
        })

pd.DataFrame(out).to_csv("krx_top_news_visible_full.csv", index=False, encoding="utf-8-sig")
print("✅ 본문 포함 CSV 저장 완료")
