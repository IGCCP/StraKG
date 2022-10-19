import numpy as np
import pandas as pd
import re

def sheetNames(filename):
    sheet_data = pd.ExcelFile(filename)
    df_list = []
    for name in sheet_data.sheet_names:
        #print(name)
        df = pd.read_excel(sheet_data, name)
        row, col = df.shape
        for i in range(row):
            for j in range(1,col):
                cur_value = str(df.iloc[i, j])
                # print(type(cur_value))
                pure_char = replace_spec_char(cur_value).replace('\n', '').replace('\r', '').strip()
                df.iloc[i, j] = pure_char
        df_list.append(df)
    return df_list

def replace_spec_char(char):
    """替换掉特殊字符, 用某种自定义标记"""
    # pattern = re.sub('', "", char)
    pattern = re.sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+','', char)
    return pattern

if __name__ == '__main__':
    # 读取待查询的地层名称
    filename = './Raw_data/Rock-1028-Ar copy.xls'
    df_list = sheetNames(filename)
    # print(df_list)    # type(df_list):<class 'list'>

    pd_reader = pd.read_csv("location_res/location.csv")
    # print(pd_reader)

    for data in df_list:
        for index, row in data.iterrows():
            # print(type(row))  # <class 'pandas.core.series.Series'>
            temp = row['分布']
            # print(temp)

            locationstr = ''
            for cname in pd_reader['中文名称']:
                if cname in temp:
                    locationstr = locationstr + str(pd_reader.loc[pd_reader['中文名称'] == cname]['英文名称'].tolist())
            row['位置'] = locationstr

            if row['位置']:
                print(row['位置'])
            else:
                locationstr1 = ''
                for cname2 in pd_reader['简称']:
                    if cname2 in temp:
                        locationstr1 = locationstr1 + str(pd_reader.loc[pd_reader['简称'] == cname2]['英文名称'].tolist())
                row['位置'] = locationstr1

            valuse = dict(row)
            print(valuse)
            #print(pd.DataFrame(valuse, index=[0]))
            pd.DataFrame(valuse, index=[0]).to_csv('./location_res/resRock-1028-Ar.csv', header=0, encoding='utf-8', mode='a')