"""
#Sao Paulo, July 31st, 2020
#Script to join CLEAN USPATENT CITATION AND SELF CITATION
#As this file will be use to calculate centrality, the output will be in the format used by the graph_tool script (similar to patcitonly)
The file cleanuspatent.csv cannot be directly joined to self_cit.csv because the field 'name' presents some EOF within double quotes. To solve the issue, I first created only_uuid_pat_cit.csv, which is a version of cleanpatent.csv with only the relevant fields - namely uuid, citation_id and patent_id. This is done by the uscleanpat_exclude_name_field.py script.

"""
import gzip
import pandas as pd
import sys
sys.path.append('/home/rkogeyam/scripts/')
from append_output import append_output

pat='data/only_uuid_pat_cit.csv'
self_cit='data/self_cit.csv'

#file=gzip.open(pat, 'r')
#file2=gzip.open(self_cit, 'r')

df=pd.read_csv(pat, dtype=object)
df.set_index('uuid', inplace=True)

df.info()

#this function append basic df data to an output file
append_output(df, __file__.replace(".py",""))


df2=pd.read_csv(self_cit, dtype=object)
df2.set_index('uuid', inplace=True)
append_output(df2, __file__.replace(".py",""))

df=df.join(df2, how='outer')
append_output(df, __file__.replace(".py",""))

df=df[df.self_cit=="0"]
df.info()
"""
import dask.dataframe as dd

#dask generates a "dask.async.CParserError: Error tokenizing data. C error: EOF inside string starting at line 367620"
#it seems that dasks achieve parallelism by arbitrarily chunking the file - ie it may chunk at some problematic point
#more: https://stackoverflow.com/questions/62899330/read-csv-with-multiline-text-columns-by-dask

#I tried to clear the file with: "tr -dc '[:print:]\n' < data/cleanuspatentcitation.csv > data/cleanuspatentcitation2.csv"

#usecols=['uuid', 'patent_id', 'citation_id']
# Read in the csv files.
df1 = dd.read_csv(pat, sep=',', error_bad_lines=False).set_index('uuid')
#df1 = df1.set_index('uuid').persist()
df2 = dd.read_csv(self_cit, sep=',', error_bad_lines=False).set_index('uuid')
#df2 = df2.set_index('uuid').persist()

# Merge the csv files.
df = dd.merge(df1, df2, left_index=True)
"""

# Write the output.
#df = df[['patent_id', 'citation_id']] 
#the intention here is to keep only these columns, but this does not work because uuid is the index. so in the export command to_csv, I added 'index_col=False', but at this point I did not tested it)
df.to_csv('data/uspatclean_selfcit.csv', columns=['patent_id','citation_id'], index=False)

