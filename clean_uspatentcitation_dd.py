import pandas as pd
#import zipfile
#import gzip
import re
import csv
import dask.dataframe as dd

file=["data/uspatentcitation.tsv.zip"]
dst='data/cleanuspatentcitation.csv.gz'
#file="D:\\PatentsView_2020\\uspatentcitation.tsv.zip"
#dst='D:\\PatentsView_2020\\cleanuspatentcitation.csv.gz'

df=dd.read_csv(file, compression='zip', sep="\t", error_bad_lines=False, encoding="utf-8", usecols=['patent_id', 'citation_id', 'date'])
cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
# first_patent = datetime.date(1790, 7, 31)
first_patent = pd.to_datetime('1790-06-30', format="%Y-%m-%d") #helps us to identify citations with problems - small change from the actual first patent's grant date because one of the citations for n1 seems to be right
df['patent_id']=df['patent_id'].apply(cleaning_patent)
df.date.replace({'-00':'-01'}, regex=True, inplace=True)
df['date']=pd.to_datetime(df['date'], format="%Y-%m-%d", errors='coerce', infer_datetime_format=True)
df.dropna(subset=['date'], inplace=True)
df.to_csv(dst, mode='w', compression='gzip', encoding='utf-8')
