# import packages
import wget
import os
import pandas as pd
import fuzzywuzzy as fuzz # <- This will be used later, just not here...
import re
from datetime import datetime as dt

# directory setup
currentdir = os.getcwd()
data_in = currentdir + '/soc_data_{0}'.format(dt.now().strftime('%Y%m%d_%H%M%S'))
socdata = os.mkdir(data_in)

# download data from bls
wget.download(
    'https://www.bls.gov/soc/2018/soc_2018_direct_match_title_file.xlsx',
    data_in + '/soc_2018_direct_match_title_file.xlsx'
    )

# load excel file and read only from line 7 onwards
socexcel = openpyxl.load_workbook(
    data_in + '/soc_2018_direct_match_title_file.xlsx'
    )
soc_raw = socexcel.get_sheet_by_name(socexcel.get_sheet_names()[0])
soc_pd = pd.DataFrame(soc_raw.values)[7:]

# functions to fix this dumpster fire of column names
def create_column_names(pdf, row):
    pdf = pdf.rename(columns=pdf.iloc[row])
    return pdf.drop(pdf.index[row])

def clean_column_names(name_list):
    assert isinstance(name_list, list)
    lowerlist = [string.lower() for string in name_list]
    nonumlist = [re.sub(r"[0-9]", '', string) for string in lowerlist]
    leadingspace = [re.sub(r"^\s", '', string) for string in nonumlist]
    scoredlist = [re.sub(r"\s", '_', string) for string in leadingspace]
    return scoredlist

# fix the column names
soc_pd = create_column_names(soc_pd, 0)
soc_pd.columns = clean_column_names(list(soc_pd.columns))

# write to csv
data_out = currentdir + '/soc_out_{0}'.format(dt.now().strftime('%Y%m%d_%H%M%S'))
socout = os.mkdir(data_out)
soc_pd.to_csv(
    data_out + '/soc_direct_match_title_file.csv', 
    sep='|', 
    encoding='utf-8',
    index='False'
    )