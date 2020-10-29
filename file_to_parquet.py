"""
Script to convert zip files to parquet
"""
   
import pandas as pd
import os
import pyarrow

#file="data/uspatentcitation.tsv.zip"
#cols=['patent_id', 'citation_id', 'date']
file="data/patent.tsv.zip"
cols=['id', 'num_claims', 'date', 'type', 'kind']

df = pd.read_csv(file, compression='zip', chunksize=15*1024*1024, usecols=cols, dtype=object, sep="\t", error_bad_lines=False, encoding="utf-8")

for i, chunk in enumerate(df):
    #filename="parquet/uspatentcitation"+f"{i:03d}"+".parquet.gz"
    filename="parquet/patent"+f"{i:03d}"+".parquet.gz"
    chunk.to_parquet(filename, compression='gzip')