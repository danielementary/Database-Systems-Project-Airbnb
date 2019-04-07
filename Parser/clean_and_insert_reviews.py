import csv
import pandas as pd
import numpy as np


def clean_reviews_data(filename):
    file = open(filename, newline='')
    data_frame = pd.read_csv(filename, dtype={'listing_id': int, 'id': int, 'reviewer_id': int, 'reviewer_name': str, 'comments': str})

    #add double quotes surrounding every comments
    data_frame['comments'] = data_frame['comments'].apply(addQuotes)

    #remove \n from comments replacing them by a space
    data_frame['comments'] = data_frame['comments'].str.replace('\n', ' ')

    du = data_frame.duplicated(['id']).tolist()
    duplicated_id = True in du

    print("Is there duplicated ids in file (", filename, ")? : ", duplicated_id)

    #save the cleaned version back

    splited_original_name = filename.split('/')
    newname = '/'.join(splited_original_name[:-1]) + "/cleaned_" + splited_original_name[-1:][0]
    data_frame.to_csv(newname, encoding='utf8')
    print("new cleaned version of the file has been saved under name : " + newname)

def addQuotes(string):
    string = str(string)
    return string


reviews_files = ["barcelona_reviews.csv", "berlin_reviews.csv", "madrid_reviews.csv"]

reviews_files = ["../Dataset/" + file for file in reviews_files]

for file in reviews_files:
    clean_reviews_data(file)
