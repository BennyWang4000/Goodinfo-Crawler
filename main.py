# %%
from config import *
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib import parse
# %%


def get_params(sheet='季資產狀況', sheet2='資產負債金額', rpt_time='最新資料'):
    '''return params for request
    params
        sheet: str, default='季資產狀況'
        sheet2: str, default='資產負債金額'
        rpt_time: str, default='最新資料'
    return
        dict
    '''

    params = {'SEARCH_WORD': '',
              'SHEET': sheet,
              'SHEET2': sheet2,
              'MARKET_CAT': '熱門排行',
              'INDUSTRY_CAT': '每股淨值最高@@每股淨值@@每股淨值最高',
              'STOCK_CODE': '',
              'RPT_TIME': rpt_time,
              'STEP': 'DATA'}

    headers = {'content-type': 'application/x-www-form-urlencoded;',
               'content-length': '0',
               'referer': URL + parse.urlencode(params),
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55'}

    return params, headers


def _to_float(s):
    '''number contains conmma to float
    param
        s: any
    return
        float or any
    '''
    nums = '1234567890'
    if type(s) is str:
        if len(s) > 0:
            if s[0] in nums and s[-1] in nums:
                if ',' in s:
                    return float(s.replace(',', ''))
    return s


def get_df(params, headers, url):
    '''Get all data in dataframe
    params
        params: dict<>, Parameters of payload for post 
        headers: dict<>, Request headers for post
    return
        pd.dataframe, All data after crawl
    '''
    all_dict = {}
    fields = []
    i = 0
    len_rank = 0
    while True:
        print('rank:', i)
        params['RANK'] = i
        response = requests.Session().post(
            url, data=parse.urlencode(params), headers=headers)
        if(response.status_code != 200):
            print(response.status_code)
        response.encoding = ENCODING
        result_table = BeautifulSoup(response.text, 'html.parser').find(
            'table', class_='r10 b1 p4_1')

        # record fields at first time
        if i == 0:
            options = BeautifulSoup(response.text, 'html.parser').find(
                'select', id='selRANK')
            len_rank = len(options)
            print('len:', len_rank)
            for ths in result_table.find_all('th'):
                for th in ths:
                    fields.append(th.text)

        for trs in result_table.find_all('tr'):
            tds = trs.find_all('td')
            if tds is None:
                continue
            tds_dict = {fields[idx]: _to_float(
                td.text) for idx, td in enumerate(tds)}
            if '代號' in tds_dict:
                if tds_dict['代號'] == '代號':
                    continue
                rank = tds_dict.pop('排名')
                all_dict[rank] = tds_dict
        i += 1
        if i >= len_rank:
            break

    return pd.DataFrame.from_dict(all_dict, orient='index')


def get_cols(df: pd.DataFrame, cols=['代號', '名稱', '股東權益(億)', '每股淨值(元)']):
    '''Get specific column from pd.dataframe
    params
        ori_df: pd.dataframe, dataframe from get_df()
        cols: lst<str>, list of columns. assert in ['代號', '名稱', '成交', '財報季度', '市值(億)', '現金(億)', '應收帳款(億)', '存貨(億)', '速動資產(億)', '流動資產(億)', '投資(億)', '固定資產(億)', '無形資產(億)', '其他資產(億)','資產總額(億)', '流動負債(億)', '長期負債(億)', '其他負債(億)', '負債總額(億)', '股東權益(億)', '每股淨值(元)', '財報評分']
    return 
        pd.dataframe
    '''
    # for col in cols:
    #     assert col in df.columns
    return df.loc[:, cols]


def save_df(df: pd.DataFrame, saving_path, file_type='csv', index=True):
    assert file_type in ['csv']
    if file_type == 'csv':
        df.to_csv(saving_path)

# %%


# %%
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--sheet', type=str, default='季資產狀況', help='資料顯示依據')
    parser.add_argument('--sheet2', type=str, default='資產負債金額', help='資料顯示依據')
    parser.add_argument('--rpt_time', type=str, default='最新資料', help='資料顯示依據')
    parser.add_argument('--saving_path', type=str,
                        default=None, help='saving path for csv file')
    parser.add_argument(
        '--columns', default=['代號', '名稱', '股東權益(億)', '每股淨值(元)'], help="columns, assert in ['代號', '名稱', '成交', '財報季度', '市值(億)', '現金(億)', '應收帳款(億)', '存貨(億)', '速動資產(億)', '流動資產(億)', '投資(億)', '固定資產(億)', '無形資產(億)', '其他資產(億)','資產總額(億)', '流動負債(億)', '長期負債(億)', '其他負債(億)', '負債總額(億)', '股東權益(億)', '每股淨值(元)', '財報評分']")

    args = parser.parse_args()
    params, headers = get_params(
        sheet=args.sheet, sheet2=args.sheet2, rpt_time=args.rpt_time)
    df = get_cols(get_df(params=params, headers=headers,
                  url=URL), cols=args.columns)
    # df = get_df(params=params, headers=headers,
    #             url=URL)

    if args.saving_path is not None:
        save_df(df, saving_path=args.saving_path)
# %%
