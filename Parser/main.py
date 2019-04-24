import clean_and_insert_reviews as reviews
import clean_and_insert_listings as listings
import clean_and_insert_calendar as calendar
import pandas as pd
import os

import csv_tokenizer as tok

reviews_files = ["barcelona.csv", "berlin.csv", "madrid.csv"]
reviews_files = ["temp/temp_reviews_" + file for file in reviews_files]

listings_files = ["barcelona_listings.csv", "madrid_listings_filtered.csv", "berlin_listings_filtered.csv"]
listings_files = ["../Dataset/Provided/" + file for file in listings_files]

calendar_files = ["Barcelona.csv", "Madrid.csv", "Berlin.csv"]
calendar_files = ["temp/temp_calendar_"+file for file in calendar_files]




listings.create_insert_queries(listings_files)

for filename in reviews_files :
    reviews.insert_reviews_reviewers(filename)

# print("calendars ")
# calendar.insert_calendar(calendar_files)
#
# print("begin main checks")
# for filename in os.listdir('insert'):
#     if filename != ".DS_Store":
#         filename = "insert/" + filename
#         print("check if columns size equal values line size for : " + filename)
#         columns, values = tok.tokenize(filename)
#         if len(columns) != len(values[0]):
#             print("# columns = ", len(columns), " and values first line size = ", len(values[0]), " for file : ", filename)
#         if "listing." in filename.lower():
#             print("check duplicates in listing id for : " + filename)
#             seen = set([])
#             duplicated = []
#             for v in values:
#                 if v[0] in seen:
#                     duplicated.append(v[0])
#                 else:
#                     seen.add(v[0])
#
#             print("duplicates : ", duplicated )
#
#         if "host." in filename.lower():
#             print("check duplicates in host id for : " + filename)
#             seen = set([])
#             duplicated = []
#             for v in values:
#                 if v[0] in seen:
#                     duplicated.append(v[0])
#                 else:
#                     seen.add(v[0])
#
#             print("duplicates : ", duplicated)
