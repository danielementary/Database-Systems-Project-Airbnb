##Deliverable 2

Note :  
* Queries 1, 2, 3, 5 are functional.  
* Queries 4, 6, 7, 8, 9, 10 do not work but are implemented.



---------
###Queries

1. The query finds the average price for a listing with a specified number of bedrooms. We use 8 bedrooms for the example. <br>
Since the table Listing has an attribute for the number of bedrooms and one for the price, the query is direct.
    ```sql
    SELECT AVG(price)
    FROM Listing
    WHERE beds = 8;
    ```
2. The query finds the average cleaning review score for the listings with TV. We suppose that these listings include TV's and Smart TV's. <br>
The implementation requires the Listing and Amenity tables, and the relation that maps both of them (Listing_amenity_map).
    ```sql
    SELECT AVG(L.price)
    FROM Listing L,
         Listing_amenity_map M
    WHERE L.listing_id = M.listing_id
          AND M.amenity_id = (SELECT A.amenity_id
                              FROM Amenity A
                              WHERE A.amenity_name = "TV"
                              OR "Smart TV");

    ```
3. The query finds the hosts that have an available listing between two dates (03.2019 and 09.2019). We suppose that it suffices that the listing is available just one day in this interval. <br>
We need the Host table for the name, the Listing, the Day and the Calendar tables for the implementation.
    ```sql
    SELECT DISTINCT H.host_name
    FROM Host H,
         Listing L,
         Day D,
         Calendar C
    WHERE H.host_id = L.host_id
          AND L.listing_id = C.listing_id
          AND C.calendar_available = 1
          AND C.calendar_day_id = D.day_id
          AND D.day_date >= "2019-03-01"
          AND D.day_date < "2019-10-01";
    ```
4. The query finds how many listings exist that are posted by two different hosts but the hosts have the same name.
    ```sql
    -- TODO
    ```
5. The query finds the dates that a specified host (we use 'Viajes Eco') has available accommodations for rent. <br>
The Day, Calendar (listing-calendar relation), Listing (shows which listings Viajes Eco owns) and Host tables are necessary for the implementation.

    ```sql
    SELECT DISTINCT D.day_date
    FROM Day D,
         Calendar C,
         Listing L,
         Host H
    WHERE D.day_id = C.calendar_day_id
          AND C.listing_id = L.listing_id
          AND C.calendar_available = 1
          AND L.host_id = H.host_id
          AND H.host_name = "Viajes Eco";
    ```

6. The query finds all the pairs (host_ids, host_names) that only have one listing online. <br>
We only need Listing and Host table to implement this query. The COUNT syntax is necessary to implement the constraint of "exactly one".

    ```sql
    SELECT DISTINCT H.host_id, H.host_name
    FROM Host H,
         Listing L
    WHERE H.listing_id = L.listing_id
    GROUP BY L.listing_id
    HAVING COUNT(L.listing_id) = 1;
    ```

7. The query computes the difference of price (average) between listings with or without Wifi. We suppose that the listing with Wifi have either 'Wifi' or 'Pocket wifi' in their amenities. <br>
For the implementation we need the many-to-many Listing_amenity_map to link the wifi information (Amenity table) and the listings (Listing table).
    ```sql
    SELECT AVG(L1.price) - AVG(L2.price)
    FROM Listing L1,
         Listing L2,
         Listing_amenity_map M1,
         Listing_amenity_map M2,
    WHERE (L1.listing_id = M1.listing_id)
          AND (M1.amenity_id IN (SELECT A.amenity_id
                                FROM Amenity A
                                WHERE A.amenity_name = "Wifi"
                                OR A.amenity_name = "Pocket wifi"))
          AND (L2.listing_id = M2.listing_id)
          AND M2.amenity_id NOT IN (SELECT A.amenity_id
                                    FROM Amenity A
                                    WHERE A.amenity_name = "Wifi"
                                    OR A.amenity_name = "Pocket wifi");
    ```
8. The query computes the difference of price in a room with 8 beds in Berlin compared to Madrid.<br>
We need the Listing, Neighbourhood and City tables to implement the query, since the Neighbourhood table links the Listing and the City by our normalization.

    ```sql
    SELECT AVG(L1.price) - AVG(L2.price)
    FROM Listing L1,
         Listing L2
    WHERE (L1.listing_id IN (SELECT L.listing_id
                            FROM Listing L,
                                 Neighbourhood N,
                                 City C
                            WHERE L.neighbourhood_id = N.neighbourhood_id
                            AND N.city_id = C.city_id
                            AND C.city_name = "Berlin"
                         ))
    AND (L1.beds = 8)
    AND (L2.listing_id IN (SELECT L.listing_id
                          FROM Listing L
                               Neighbourhood N,
                               City C
                          WHERE L.neighbourhood_id = N.neighbourhood_id
                          AND N.city_id = C.city_id
                          AND C.city_name = "Madrid"))
    AND (L2.beds = 8);
    ```
9. The query finds the top-10 host (host_ids, host_names) in terms of number of listings per host in Spain.

    ```sql

    ```
10. The query finds the top-10 listings (review_score_rating) in terms of review_score_rating apartments in Barcelona.<br>
For the implementation, we used the TOP synthax which seems to not work.

    ```sql
    SELECT L.listing_id, L.listing_name
    FROM Listing L
    WHERE L.review_score_rating IN (SELECT TOP 10 review_score_rating
                                   FROM Listing
                                   ORDER BY review_score_rating DESC
                                  );
    ```
