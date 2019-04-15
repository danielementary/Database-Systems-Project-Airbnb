import pandas as pd
import numpy as np


def clean_reviews_data(filename):
    """
    clean data in reviews files. return a data_frame containing reviews data and
    one containing reviewers data.
    """
    file = open(filename, newline='')
    data_frame = pd.read_csv(filename, dtype={'listing_id': int, 'id': int, 'reviewer_id': int, 'reviewer_name': str, 'comments': str})

    #add double quotes surrounding every comments
    data_frame['comments'] = data_frame['comments'].apply(cleanString)

    #remove \n from comments replacing them by a space
    data_frame['comments'] = data_frame['comments'].str.replace('\n', ' ')

    du = data_frame.duplicated(['id']).tolist()
    duplicated_id = True in du

    print("Is there duplicated ids in file (", filename, ")? : ", duplicated_id)

    review_df = data_frame[['id', 'date', 'comments', 'listing_id', 'reviewer_id']]
    reviewer_df = data_frame[['reviewer_id', 'reviewer_name']]

    # remove duplicated reviewers
    # there is only one reviewer id duplicated with 2 different names (Casa Nuna : Mi Casa Bali)
    # We chose to remove one
    reviewer_df = reviewer_df.drop_duplicates(['reviewer_id'])

    du = reviewer_df.duplicated(['reviewer_id']).tolist()
    duplicated_reviewer = True in du

    print("duplicated reviewers : ", duplicated_reviewer)


    file.close()

    # not directly useful but for checks if needed
    splited_original_name = filename.split('/')
    newname = '/'.join(splited_original_name[:-1]) + "/cleaned/cleaned_" + splited_original_name[-1:][0]
    data_frame.to_csv(newname, encoding='utf8')
    print("new cleaned version of the file has been saved under name : " + newname)

    return (review_df, reviewer_df)

def cleanString(string):
    string = str(string)

    #remove ' if surrounding the string
    if string != "":
        if string[0] == "'":
            string = string[1:]
        if string[-1] == "'":
            string = string[:-1]
        #put a quote before every quotes appearing in the string to escape it
        string = string.replace("''", "'")
        string = string.replace("'", "''")

        #add surrounding quotes
        string = "'" + string.strip() + "'"
    return string


def insert_reviews_reviewers(filename):
    """
    write a .sql file containing INSERT statements required to insert data contained in filename
    """
    (review_df, reviewer_df) = clean_reviews_data(filename)

    splited_original_name = filename.split('/')
    outname = '/'.join(splited_original_name[:-1]) + '/' + splited_original_name[-1:][0].split('.')[0] + "_insert_queries.sql"
    outputfile = open(outname, 'w')

    for index, row in review_df.iterrows():
        #here get columns and create sql query
        #columns are in order: review_id, review_date, review_comments, reviewer_id, listing_id
        sql_query = """INSERT INTO Review VALUES ({}, {}, {}, {}, {});""".format(
                row['id'],
                row['date'],
                '"' + str(row['comments']) + '"',
                row['reviewer_id'],
                row['listing_id']
        )
        outputfile.write(sql_query + '\n')


    for index, row in reviewer_df.iterrows():
        #insert reviewer in reviewer table
        sql_query = """INSERT INTO Reviewer VALUES ({}, {});""".format(
                row['reviewer_id'],
                row['reviewer_name']
        )
        outputfile.write(sql_query + '\n')

    print("insert queries have been written for (", filename, ") in : ", outname)
    outputfile.close()

reviews_files = ["barcelona_reviews.csv", "berlin_reviews.csv", "madrid_reviews.csv"]

reviews_files = ["../Dataset/" + file for file in reviews_files]

cleaned_files = []

for file in reviews_files:
    insert_reviews_reviewers(file)
