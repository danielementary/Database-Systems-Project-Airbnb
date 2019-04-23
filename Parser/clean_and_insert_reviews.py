import pandas as pd
import numpy as np

outputfile_reviews_name = "insert/Reviews.csv"
outputfile_reviewers_name = "insert/Reviewers.csv"

def clean_reviews_data(filename):
    """
    clean data in reviews files. return a data_frame containing reviews data and
    one containing reviewers data.
    """

    file = open(filename, newline='')
    data_frame = pd.read_csv(filename, dtype={'listing_id': int, 'id': int, 'reviewer_id': int, 'reviewer_name': str, 'comments': str})

    # add fixed offset for each city to evict duplicates when putting all together
    if "barcelona" in filename.lower():
        offset = 0
    elif "madrid" in filename.lower():
        offset = 300000000
    else:
        offset = 600000000

    data_frame['reviewer_id'] = data_frame['reviewer_id'] + offset
    #add double quotes surrounding every comments
    data_frame['comments'] = data_frame['comments'].apply(cleanString)
    data_frame['reviewer_name'] = data_frame["reviewer_name"].apply(cleanString)

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
    # splited_original_name = filename.split('/')
    # newname = '/'.join(splited_original_name[:-1]) + "/cleaned/cleaned_" + splited_original_name[-1:][0]
    # data_frame.to_csv(newname, encoding='utf8')
    # print("new cleaned version of the file has been saved under name : " + newname)

    return (review_df, reviewer_df)

def cleanString(string):
    string = str(string)

    string = string.replace('\n', ' ')

    #remove ' if surrounding the string
    if string != "" and len(string) > 1:
        if string[0] == "'":
            string = string[1:]
        if string[-1] == "'":
            string = string[:-1]
        #put a quote before every quotes appearing in the string to escape it
        string = string.replace("''", "'")
        string = string.replace("'", "''")

        #add surrounding quotes
        string = "'" + string.strip() + "'"

    if string.lower() == "'nan'":
        string = "''"
    return string


def insert_reviews_reviewers(filename):
    """
    write a .csv files containing columns names for inserting reviewers and reviews and all values
    """
    (review_df, reviewer_df) = clean_reviews_data(filename)

    create_output_csvs_if_not_exist()

    outputfile_reviews = open(outputfile_reviews_name, 'a')
    outputfile_reviewers = open(outputfile_reviewers_name, 'a')

    outputfile = outputfile_reviews
    for index, row in review_df.iterrows():
        #here get columns and create sql query
        #columns are in order: review_id, review_date, review_comments, reviewer_id, listing_id
        csv_line = """{},{},{},{},{}""".format(
                row['id'],
                row['date'],
                str(row['comments']),
                row['reviewer_id'],
                row['listing_id']
        )
        outputfile.write(csv_line + '\n')


    outputfile = outputfile_reviewers
    for index, row in reviewer_df.iterrows():
        #insert reviewer in reviewer table
        csv_line = """{},{}""".format(
                row['reviewer_id'],
                row['reviewer_name']
        )
        outputfile.write(csv_line + '\n')

    print("insert queries have been written for (", filename)

    outputfile_reviews.close()
    outputfile_reviewers.close()


def create_output_csvs_if_not_exist():
    try:
        file = open(outputfile_reviews_name, 'r')
    except:
        file = open(outputfile_reviews_name, 'w')
        file.write("review_id,review_date,review_comments,reviewer_id,listing_id\n")
        file.close()
    else:
        file.close()

    try:
        file = open(outputfile_reviewers_name, 'r')
    except:
        file = open(outputfile_reviewers_name, 'w')
        file.write("reviewer_id,reviewer_name\n")
        file.close()
    else:
        file.close()
