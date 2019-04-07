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
    newname = '/'.join(splited_original_name[:-1]) + "/cleaned/cleaned_" + splited_original_name[-1:][0]
    data_frame.to_csv(newname, encoding='utf8')
    print("new cleaned version of the file has been saved under name : " + newname)

    file.close()
    return newname

def addQuotes(string):
    string = str(string)
    return string


def insert_reviews(filename):
    """
    write a .sql file containing INSERT statements required to insert data contained in filename
    """
    file = open(filename, newline='')
    data_frame = pd.read_csv(filename, dtype={'listing_id': int, 'id': int, 'reviewer_id': int, 'reviewer_name': str, 'comments': str})

    queries = []

    for index, row in data_frame.iterrows():
        #here get columns and create sql query
        #columns are in order: review_id, review_date, review_comments, reviewer_id, listing_id
        sql_query = """INSERT INTO Review VALUES ({}, {}, {}, {}, {})""".format(
                row['id'],
                row['date'],
                '"' + str(row['comments']) + '"',
                row['reviewer_id'],
                row['listing_id']
        )
        queries.append(sql_query)

        #insert reviewer in reviewer table
        sql_query = """INSERT INTO Reviewer VALUES ({}, {})""".format(
                row['reviewer_id'],
                row['reviewer_name']
        )
        queries.append(sql_query)


    splited_original_name = filename.split('/')
    outname = '/'.join(splited_original_name[:-1]) + '/' + splited_original_name[-1:][0].split('.')[0] + "_insert_queries.sql"
    outputfile = open(outname, 'w')

    for q in queries:
        outputfile.write(q + '\n')

    print("insert queries have been written for (", filename, ") in : ", outname)
    outputfile.close()

reviews_files = ["barcelona_reviews.csv", "berlin_reviews.csv", "madrid_reviews.csv"]

reviews_files = ["../Dataset/" + file for file in reviews_files]

cleaned_files = []

for file in reviews_files:
    cleaned_files.append(clean_reviews_data(file))

for file in cleaned_files:
    insert_reviews(file)
