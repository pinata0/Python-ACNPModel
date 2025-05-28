# 1페이지당 10일치 데이터

import os
import pandas as pd
import requests
import time
from io import StringIO

def get_price_naver(stock_code, max_pages=10):
    result = []
    for page in range(1, max_pages + 1):
        url = f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}&page={page}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)

        html = StringIO(res.text)
        df = pd.read_html(html, encoding='euc-kr')[0]
        df = df.dropna()
        result.append(df)
        time.sleep(0.5)
    
    if not result:
        raise ValueError(f"No data found for {stock_code}")
    
    data = pd.concat(result)
    data.columns = ['날짜', '종가', '전일비', '시가', '고가', '저가', '거래량']
    data['날짜'] = pd.to_datetime(data['날짜'])
    return data.sort_values('날짜').reset_index(drop=True)

def load_krx_codes(path='krx_company_list.csv', top_n=None):
    df = pd.read_csv(path, dtype={'종목코드': str})
    if top_n:
        df = df.head(top_n)
    return df[['회사명', '종목코드']][:top_n]

def collect_and_save_prices(krx_df, max_pages=2, save_dir="company_list"):
    os.makedirs(save_dir, exist_ok=True)

    for idx, row in krx_df.iterrows():
        name = row['회사명'].replace("/", "-")  # 파일명에 슬래시 방지
        code = row['종목코드']
        print(f"[{idx+1}/{len(krx_df)}] Collecting {name} ({code})...")

        try:
            df = get_price_naver(code, max_pages=max_pages)
            df['회사명'] = name
            df['종목코드'] = code

            save_path = os.path.join(save_dir, f"{name}.csv")
            df.to_csv(save_path, index=False, encoding='utf-8-sig')
            print(f"✅ 저장 완료: {save_path}")
        except Exception as e:
            print(f"❌ Failed: {name} ({code}) - {e}")

if __name__ == "__main__":
    krx_df = load_krx_codes("krx_company_list.csv", top_n=2643)
    collect_and_save_prices(krx_df, max_pages=257)