import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from datetime import datetime, timedelta
    
def get_news_visible(company, max_pages=2, delay=2.0):
    def convert_relative_date(text):
        today = datetime.today()
        try:
            if "시간 전" in text:
                return today.strftime("%Y-%m-%d")
            elif "일 전" in text:
                days = int(re.search(r'(\d+)일 전', text).group(1))
                return (today - timedelta(days=days)).strftime("%Y-%m-%d")
            elif "주 전" in text:
                weeks = int(re.search(r'(\d+)주 전', text).group(1))
                return (today - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
            elif "개월 전" in text:
                months = int(re.search(r'(\d+)개월 전', text).group(1))
                return (today - timedelta(days=months*30)).strftime("%Y-%m-%d")
            elif "년 전" in text:
                years = int(re.search(r'(\d+)년 전', text).group(1))
                return (today - timedelta(days=years*365)).strftime("%Y-%m-%d")
            else:
                return text.strip()
        except:
            return "날짜파싱실패"
        
    def find_first_valid_date_span(spans):
        for span in spans:
            text = span.text.strip()
            if re.search(r"(시간|일|주|개월|년) 전", text) or re.match(r"\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}", text):
                return text
        return None

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--lang=ko-KR")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_news = []

    for page in range(1, max_pages + 1):
        start = 1 + (page - 1) * 10
        url = f"https://search.naver.com/search.naver?where=news&query={company}&start={start}&sort=1"
        print(f"▶︎ [페이지 {page}] {company} 접속: {url}")
        driver.get(url)
        time.sleep(delay)

        news_blocks = driver.find_elements(
            By.CSS_SELECTOR,
            'div.sds-comps-vertical-layout.sds-comps-full-layout.EPe0s1rCZZ86kDLT_SY2'
        )

        for block in news_blocks:
            try:
                # 뉴스 제목 및 링크 추출 (a 태그 내부에 함께 있음)
                link_elem = block.find_element(By.CSS_SELECTOR, 'a.lu8Lfh20c9DvvP05mqBf.tym_MoKIfC84Aqvg9SKg')
                title_elem = link_elem.find_element(By.CSS_SELECTOR, 'span.sds-comps-text-type-headline1')
                title_text = title_elem.text.strip()
                href = link_elem.get_attribute("href").strip()

                # 날짜 후보 span들 중 첫 유효 날짜 선택
                spans = block.find_elements(By.CSS_SELECTOR, 'span.sds-comps-text')
                date_text = find_first_valid_date_span(spans)
                if not date_text:
                    continue

                date_str = convert_relative_date(date_text)

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


    driver.quit()
    return pd.DataFrame(all_news)

def load_krx_names(path='krx_company_list.csv', top_n=1):
    df = pd.read_csv(path)
    return df['회사명'].head(top_n).tolist()

def collect_all_news(csv_path='krx_company_list.csv', max_pages=3):
    companies = load_krx_names(csv_path)
    all_data = []

    for i, company in enumerate(companies):
        print(f"[{i+1}/{len(companies)}] {company} 뉴스 수집 중...")
        try:
            df = get_news_visible(company, max_pages=max_pages)
            all_data.append(df)
        except Exception as e:
            print(f"❌ {company} 실패: {e}")
        time.sleep(1.5)  # 너무 빠르게 요청하면 차단 위험

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv("krx_top_news_visible.csv", index=False, encoding="utf-8-sig")
    print("✅ 저장 완료: krx_top_news_visible.csv")

if __name__ == "__main__":
    collect_all_news("krx_company_list.csv", max_pages=3)

