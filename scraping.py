import pandas as pd
import requests
import numpy as np
import time

raw_api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=2011-12&SeasonType=Regular%20Season&StatCategory=PTS'
headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br, zstd',
    'Accept-Language':'es-419,es;q=0.7',
    'Connection':'keep-alive',
    'Host':'stats.nba.com',
    'Origin':'https://www.nba.com',
    'Referer':'https://www.nba.com/',
    'Sec-Ch-Ua':'"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform':'"Windows"',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-site',
    'Sec-Gpc':'1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

r = requests.get(url=raw_api_url, headers=headers).json()

df_cols_short = r['resultSet']['headers']
df_cols = ['Year','Season_Type'] + df_cols_short
years = ['2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']
season_types = ['Regular%20Season','Playoffs']

df = pd.DataFrame(columns=df_cols)

begin_loop = time.time()

for y in years:
    for s in season_types:
        api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season='+y+'&SeasonType='+s+'&StatCategory=PTS'
        r = requests.get(url=api_url, headers=headers).json()
        temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=df_cols_short)
        temp_df2 = pd.DataFrame({'Year':[y for i in range(len(temp_df1))],
                                 'Season_Type':[s for i in range(len(temp_df1))]})
        temp_df3 = pd.concat([temp_df2, temp_df1], axis=1)
        df = pd.concat([df, temp_df3], axis=0)
        print(f'Finished scraping data from the {y} {s}')
        lag = np.random.uniform(low=20, high=40)
        print(f'Waiting {round(lag,1)} seconds...')
        time.sleep(lag)

print(f'Finished. Total run time: {round(time.time()-begin_loop,1)} seconds')
df.to_excel('nba_data.xlsx',index=False)