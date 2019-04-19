import clean_and_insert_reviews as reviews
import clean_and_insert_listings as listings
import pandas as pd
import os

reviews_files = ["barcelona_reviews.csv", "berlin_reviews.csv", "madrid_reviews.csv"]
reviews_files = ["../Dataset/" + file for file in reviews_files]

listings_files = ["barcelona_listings.csv", "madrid_listings_filtered.csv", "berlin_listings_filtered.csv"]
listings_files = ["../Dataset/" + file for file in listings_files]



for filename in reviews_files :
    reviews.insert_reviews_reviewers(filename)

listings.create_insert_queries(listings_files)

print("begin main checks")
# for filename in os.listdir('insert'):
#     filename = "insert/" + filename
#     print("check for duplicates in : " + filename)
#     df = pd.read_csv(filename)
#     dup = df.duplicated()
#     for i in dup:
#         if i:
#             print("MAIN : there were duplicates in : " + filename)
#     df.drop_duplicates()
#     df.to_csv(filename)
