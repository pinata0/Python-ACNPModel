# 1페이지당 10일치 데이터

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from io import StringIO

def get_price_naver(stock_code, max_pages=10):
    """
    주어진 종목코드에 대해 네이버 금융에서 일별 주가를 크롤링
    """
    result = []
    for page in range(1, max_pages + 1):
        url = f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}&page={page}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)

        html = StringIO(res.text)
        df = pd.read_html(html, encoding='euc-kr')[0]
        df = df.dropna()
        result.append(df)
        time.sleep(0.5)  # 네이버 서버 부하 방지
    data = pd.concat(result)
    data.columns = ['날짜', '종가', '전일비', '시가', '고가', '저가', '거래량']
    data['날짜'] = pd.to_datetime(data['날짜'])
    data = data.sort_values('날짜')
    return data.reset_index(drop=True)

def load_krx_codes(path='krx_company_list.csv', top_n=None):
    df = pd.read_csv(path, dtype={'종목코드': str})
    if top_n:
        df = df.head(top_n)
    return df[['회사명', '종목코드']][:3]

def collect_all_prices(krx_df, max_pages=2):
    all_prices = []
    for idx, row in krx_df.iterrows():
        name = row['회사명']
        code = row['종목코드']
        print(f"[{idx+1}/{len(krx_df)}] Collecting {name} ({code})...")
        try:
            df = get_price_naver(code, max_pages=max_pages)
            df['회사명'] = name
            df['종목코드'] = code
            all_prices.append(df)
        except Exception as e:
            print(f"❌ Failed: {name} ({code}) - {e}")
    return pd.concat(all_prices, ignore_index=True)

if __name__ == "__main__":
    krx_df = load_krx_codes("krx_company_list.csv", top_n=100)  # 상위 100개만 수집
    all_prices = collect_all_prices(krx_df, max_pages=30)
    all_prices.to_csv("krx_top100_naver_prices.csv", index=False, encoding='utf-8-sig')
    print("✅ 저장 완료: krx_top100_naver_prices.csv")
