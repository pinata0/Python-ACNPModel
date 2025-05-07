import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from datetime import datetime, timedelta
from bisect import insort

# 날짜 문자열을 datetime 객체로 변환
def convert_relative_date(text):
    today = datetime.today()
    try:
        if "시간 전" in text:
            return today.strftime("%Y.%m.%d")
        elif "일 전" in text:
            days = int(re.search(r'(\d+)일 전', text).group(1))
            return (today - timedelta(days=days)).strftime("%Y.%m.%d")
        elif "주 전" in text:
            weeks = int(re.search(r'(\d+)주 전', text).group(1))
            return (today - timedelta(weeks=weeks)).strftime("%Y.%m.%d")
        elif "개월 전" in text:
            months = int(re.search(r'(\d+)개월 전', text).group(1))
            return (today - timedelta(days=months * 30)).strftime("%Y.%m.%d")
        elif "년 전" in text:
            years = int(re.search(r'(\d+)년 전', text).group(1))
            return (today - timedelta(days=years * 365)).strftime("%Y.%m.%d")
        else:
            # 절대 날짜 형식 처리: 점/슬래시/하이픈 → 점(.)으로 통일
            cleaned = text.strip().rstrip(".")
            cleaned = re.sub(r"[/-]", ".", cleaned)
            try:
                return datetime.strptime(cleaned, "%Y.%m.%d").strftime("%Y.%m.%d")
            except:
                return "날짜파싱실패"
    except:
        return "날짜파싱실패"

# 날짜 span들 중 첫 유효 날짜 추출
def find_first_valid_date_span(spans):
    date_pattern = r"\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}\.?"  # 예: 2025.04.06. (끝 마침표 허용)
    for span in spans:
        text = span.text.strip()
        if re.search(r"(시간|일|주|개월|년) 전", text) or re.search(date_pattern, text):
            return text
    return None

# 각 회사에 대해 뉴스 리스트 반환
def get_news_visible(company, start_dt, delay=2.0):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # 브라우저 보고싶으면 주석
    options.add_argument("--lang=ko-KR")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_news = []
    page = 1

    while True:
        start = 1 + (page - 1) * 10
        url = f"https://search.naver.com/search.naver?where=news&query={company}&start={start}&sort=1"
        print(f"▶︎ [페이지 {page}] {company} 접속: {url}")
        driver.get(url)
        time.sleep(delay)

        news_blocks = driver.find_elements(
            By.CSS_SELECTOR,
            'div.sds-comps-vertical-layout.sds-comps-full-layout.EPe0s1rCZZ86kDLT_SY2'
        )

        if not news_blocks:
            print(f"📭 더 이상 뉴스 없음 (page {page})")
            break

        for block in news_blocks:
            try:
                link_elem = block.find_element(By.CSS_SELECTOR, 'a.lu8Lfh20c9DvvP05mqBf.tym_MoKIfC84Aqvg9SKg')
                title_elem = link_elem.find_element(By.CSS_SELECTOR, 'span.sds-comps-text-type-headline1')
                title_text = title_elem.text.strip()
                href = link_elem.get_attribute("href").strip()

                spans = block.find_elements(By.CSS_SELECTOR, 'span.sds-comps-text')
                date_text = find_first_valid_date_span(spans)
                if not date_text:
                    continue

                date_str = convert_relative_date(date_text)
                news_date = datetime.strptime(date_str, "%Y.%m.%d")

                # ⛔ 종료 조건: 이 날짜가 기준 이전이면 더 안 봄
                if news_date < start_dt:
                    print(f"🛑 수집 중단: {news_date.strftime('%Y.%m.%d')} < {start_dt.strftime('%Y.%m.%d')}")
                    driver.quit()
                    return all_news

                all_news.append({
                    '회사명': company,
                    '뉴스제목': title_text,
                    '날짜': date_str,
                    '링크': href
                })

                print(f"  - 제목: {title_text} / 날짜: {date_str} / 링크: {href}")

            except Exception as e:
                print(f"❌ 뉴스 블록 처리 실패: {e}")
                continue

        page += 1

    driver.quit()
    return all_news


# 상위 기업명 리스트 로드
def load_krx_names(path='krx_company_list.csv', top_n=3):
    df = pd.read_csv(path)
    return df['회사명'].head(top_n).tolist()

# 모든 뉴스 수집 및 정렬 저장
def collect_all_news(csv_path='krx_company_list.csv', start_date="2024.01.01"):
    companies = load_krx_names(csv_path)
    all_data = []
    start_dt = datetime.strptime(start_date, "%Y.%m.%d")

    for i, company in enumerate(companies):
        print(f"[{i + 1}/{len(companies)}] {company} 뉴스 수집 중...")
        try:
            news_list = get_news_visible(company, start_dt)
            for news in news_list:
                try:
                    date_obj = datetime.strptime(news["날짜"], "%Y.%m.%d")
                    insort(all_data, (date_obj, id(news), news))
                except Exception as e:
                    print(f"❌ 날짜 파싱 실패: {news['날짜']} / 오류: {e}")
        except Exception as e:
            print(f"❌ {company} 실패: {e}")
        time.sleep(1.5)

    sorted_news = [item[2] for item in all_data]
    final_df = pd.DataFrame(sorted_news)
    final_df.to_csv("krx_top_news_visible.csv", index=False, encoding="utf-8-sig")
    print("✅ 저장 완료: krx_top_news_visible.csv")

if __name__ == "__main__":
    collect_all_news("krx_company_list.csv", start_date="2025.01.01")
