search_fields = {"Listing": ("listing_url", "listing_name", "accommodates",
                             "bathrooms", "bedrooms", "beds", "square_feet",
                             "price", "weekly_price", "monthly_price",
                             "minimum_nights", "is_business_travel_ready",
                             "review_scores_rating", "property_type_id",
                             "room_type_id", "cancellation_policy_id",
                             "amenity"),
                 "Host" : ("host_name", "host_since"),
                 "Neighbourhood" : ("neighbourhood_name", "city_id"),
                 "Review" : ("reviewer_id", "listing_id"),
                 }

result_fields = {}
