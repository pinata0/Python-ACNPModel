import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from datetime import datetime, timedelta
from bisect import insort

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
            cleaned = text.strip().rstrip(".")
            cleaned = re.sub(r"[/-]", ".", cleaned)
            try:
                return datetime.strptime(cleaned, "%Y.%m.%d").strftime("%Y.%m.%d")
            except:
                return "날짜파싱실패"
    except:
        return "날짜파싱실패"

def find_first_valid_date_span(spans):
    date_pattern = r"\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}\.?"
    for span in spans:
        text = span.text.strip()
        if re.search(r"(시간|일|주|개월|년) 전", text) or re.search(date_pattern, text):
            return text
    return None

def get_news_scroll(company, start_dt, delay=2.0, max_scrolls=50):
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=ko-KR")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://search.naver.com/search.naver?where=news&query={company}&sort=1"
    driver.get(url)
    time.sleep(delay)

    all_news = []
    seen_links = set()
    scroll_count = 0
    last_layout_count = 0

    while scroll_count < max_scrolls:
        # 스크롤 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

        # 뉴스 묶음 블록들 전체 수집
        layout_blocks = driver.find_elements(
            By.CSS_SELECTOR,
            "div.sds-comps-vertical-layout.sds-comps-full-layout"
        )

        print(f"▶︎ 스크롤 {scroll_count + 1}회, 뉴스 묶음 {len(layout_blocks)}개 탐색 중...")

        # 새로 생긴 뉴스 묶음만 처리
        new_layouts = layout_blocks[last_layout_count:]

        if not new_layouts:
            print("📭 더 이상 새로운 뉴스 묶음 없음.")
            break

        for layout in new_layouts:
            news_blocks = layout.find_elements(By.CSS_SELECTOR, "div")
            for block in news_blocks:
                try:
                    """링크 못 뽑는중 수정좀"""
                    # 뉴스 링크 및 제목 추출
                    link_elem = block.find_element(By.CSS_SELECTOR, "a.n6AJosQA40hUOAe_Vplg.cdv6mdm2_kpW2D6slkm6")
                    title_elem = link_elem.find_element(By.CSS_SELECTOR, "span.sds-comps-text-type-headline1")
                    title_text = title_elem.text.strip()
                    href = link_elem.get_attribute("href").strip()

                    if href in seen_links:
                        continue
                    seen_links.add(href)

                    # 날짜 추출 및 비교
                    spans = block.find_elements(By.CSS_SELECTOR, 'span.sds-comps-text')
                    date_text = find_first_valid_date_span(spans)
                    if not date_text:
                        continue
                    date_str = convert_relative_date(date_text)
                    news_date = datetime.strptime(date_str, "%Y.%m.%d")

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
                    continue

        # 상태 갱신
        last_layout_count = len(layout_blocks)
        scroll_count += 1

    driver.quit()
    return all_news

def load_krx_names(path='krx_company_list.csv', top_n=3):
    df = pd.read_csv(path)
    return df['회사명'].head(top_n).tolist()

def collect_all_news(csv_path='krx_company_list.csv', start_date="2024.01.01"):
    companies = load_krx_names(csv_path, 1)
    all_data = []
    start_dt = datetime.strptime(start_date, "%Y.%m.%d")

    for i, company in enumerate(companies):
        print(f"[{i + 1}/{len(companies)}] {company} 뉴스 수집 중...")
        try:
            news_list = get_news_scroll(company, start_dt)
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
    final_df.to_csv("krx_top_news_scroll.csv", index=False, encoding="utf-8-sig")
    print("✅ 저장 완료: krx_top_news_scroll.csv")

if __name__ == "__main__":
    collect_all_news("krx_company_list.csv", start_date="2025.01.01")
