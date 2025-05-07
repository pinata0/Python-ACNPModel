import pandas as pd

def get_market_list(market_type):
    """
    market_type: 'stockMkt' (코스피), 'kosdaqMkt' (코스닥)
    """
    url = f'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&marketType={market_type}'
    df = pd.read_html(url, encoding='euc-kr')[0]
    df['시장구분'] = '코스피' if market_type == 'stockMkt' else '코스닥'
    return df

def get_full_krx_list():
    df_kospi = get_market_list('stockMkt')
    df_kosdaq = get_market_list('kosdaqMkt')
    df_all = pd.concat([df_kospi, df_kosdaq], ignore_index=True)

    # 종목코드 포맷 통일 (6자리)
    df_all['종목코드'] = df_all['종목코드'].apply(lambda x: f"{int(x):06d}")

    # yfinance용 ticker 생성
    df_all['yf_ticker'] = df_all.apply(
        lambda row: row['종목코드'] + ('.KS' if row['시장구분'] == '코스피' else '.KQ'), axis=1
    )

    return df_all[['회사명', '종목코드', '업종', '상장일', '시장구분', 'yf_ticker']]

# 실행 및 저장
if __name__ == "__main__":
    krx_df = get_full_krx_list()
    krx_df.to_csv("krx_company_list.csv", index=False, encoding='utf-8-sig')
    print("✅ 저장 완료: krx_company_list.csv")
    print(krx_df.head())
