import clean_and_insert_reviews as reviews
import clean_and_insert_listings as listings

reviews_files = ["barcelona_reviews.csv", "berlin_reviews.csv", "madrid_reviews.csv"]
reviews_files = ["../Dataset/" + file for file in reviews_files]

listings_files = ["barcelona_listings.csv", "madrid_listings_filtered.csv", "berlin_listings_filtered.csv"]
listings_files = ["../Dataset/" + file for file in listings_files]


for file in reviews_files:
    reviews.insert_reviews_reviewers(file)

for file in listings_files:
    listings.create_insert_queries(file)
