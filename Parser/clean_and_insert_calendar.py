import pandas as pd
import numpy as np
import math

tables_to_attributes = {"Calendar": {"calendar_id":"calendar_id","calendar_available":"calendar_available","calendar_price":"calendar_price","listing_id":"listing_id","calendar_day_id":"calendar_day_id"},\
                        "Day": {"day_id":"day_id","day_date":"day_date"}}

def clean_calendar_data(filenames_list):

    df = pd.DataFrame()

    for filename in filenames_list:
        df_temp = pd.read_csv(filename)

        df = df.append(df_temp)

    df["available"] = df["available"].apply(replace_f_t_by_bit)
    df["price"] = df["price"].apply(clean_float_and_int)

    df = df.drop_duplicates()
    print("there are ", df.shape[0] ," lines in Calendar csvs")

    return df


def replace_f_t_by_bit(obj):
    f_t = str(obj)
    if(f_t == 't'):
        return 1
    return 0

def clean_float_and_int(a):
    a = str(a)
    a = a.replace("$", "")
    a = a.replace(",", "")
    if(a == ''):
        a = 'nan'
    return float(a)

def insert_calendar(filenames_list):
    df = clean_calendar_data(filenames_list)
    output_files = open_output_files(tables_to_attributes)

    # insert days in Day table
    dates_string = df["date"]
    dates_string = dates_string.drop_duplicates()
    dates_string = dates_string.apply(parse_date)
    dates_string = dates_string.tolist()
    dates_with_id = list(zip(dates_string, range(len(dates_string))))
    days_dict = dict(dates_with_id)

    output_file = output_files["Day"]

    for day, id in dates_with_id:
        csv_line = "{},{}\n".format(id, day)
        output_file.write(csv_line)


    cal_id = 0
    output_file = output_files["Calendar"]

    # insert calendar
    for id, row in df.iterrows():

        available = row["available"]
        price = row["price"]
        if math.isnan(price):
            price = "NULL"
        day_id = days_dict[parse_date(row["date"])]
        listing_id = row["listing_id"]

        csv_line = "{},{},{},{},{}\n".format(\
                    cal_id,\
                    available,\
                    price,\
                    listing_id,\
                    day_id)
        cal_id += 1

        output_file.write(csv_line)

    close_files(output_files.values())




def parse_date(string_date):
    year = string_date[:4]
    mounth = string_date[5:7]
    day = string_date[8:10]

    return "'date({},{},{})'".format(year, mounth, day)

def create_output_csvs_if_not_exist(tables_to_attributes):
    for table in list(tables_to_attributes.keys()):
        filename = "insert/"+table+".csv"
        try:
            file = open(filename, 'r')
        except:
            file = open(filename, 'w')
            s = ""
            for att in list(tables_to_attributes[table].keys()):
                s += att + ","
            s = s[:-1]
            s += "\n"
            file.write(s)
            file.close()
        else:
            file.close()

def open_output_files(tables_to_attributes):
    create_output_csvs_if_not_exist(tables_to_attributes)
    files = {}
    for table in tables_to_attributes.keys():
        filename = "insert/"+table+".csv"
        files[table] = open(filename, 'a')

    return files

def close_files(files):
    for f in files:
        f.close()
