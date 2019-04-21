search_fields = {"Listing": ("listing_name", "accommodates", "square_feet",
                             "price", "is_business_travel_ready",
                             "review_scores_rating", "property_type_id",
                             "cancellation_policy_id"),
                 "Host" : ("host_name", "host_since"),
                 "Neighbourhood" : ("neighbourhood_name", "city_id"),
                 "Review" : ("reviewer_id", "listing_id"),
                 }

result_fields = {}
