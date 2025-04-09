import feedparser
import sys
import io
import csv

# 터미널 출력 인코딩 설정 (윈도우에서 한글 & 유니코드 깨짐 방지)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# 삼성전자 관련 RSS 피드 (예: 구글 뉴스에서 삼성전자+증시 검색)
rss_url = "https://news.google.com/rss/search?q=삼성전자+증시&hl=ko&gl=KR&ceid=KR:ko"

# 시장 영향 가능성이 높은 키워드 목록
impact_keywords = [
    "실적", "호실적", "어닝", "적자", "흑자", "감산", "수출", "반도체", 
    "공급망", "리콜", "신제품", "투자", "인수합병", "규제", "환율", "금리"
]

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 관련 뉴스 필터링
important_news = []
for entry in feed.entries:
    title = entry.title
    summary = entry.summary if 'summary' in entry else ''
    content = f"{title} {summary}"

    # 키워드 포함 여부 확인
    if any(keyword in content for keyword in impact_keywords):
        important_news.append({
            'title': title,
            'link': entry.link,
            'published': entry.published,
        })

# 결과 출력
for news in important_news:
    print(f"[{news['published']}] {news['title']}")
    print(f"Link: {news['link']}\n")

# CSV 저장
csv_file = "삼성전자_중요뉴스.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=["published", "title", "link"])
    writer.writeheader()
    writer.writerows(important_news)

print(f"✅ {csv_file} 파일로 저장 완료!")
