##Deliverable 2
###Queries

1. What
is
the
average
price
for
a
listing
with
8
bedrooms?
2. What
is
the
average
cleaning
review
score
for
listings
with
TV?
3. Print
all
the
hosts
who
have
an
available
property
between
date
03.2019
and
09.2019.
4. Print
how
many
listing
items
exist
that
are
posted
by
two
different
hosts
but
the
hosts
have
the
same
name.
5. Print
all
the
dates
that
'Viajes
Eco'
has
available
accommodations
for
rent.
6. Find
all
the
hosts
(host_ids,
host_names)
that
have
only
one
listing.
7. What
is
the
difference
in
the
average
price
of
listings
with
and
without
Wifi.
8. How
much
more
(or
less)
costly
to
rent
a
room
with
8
beds
in
Berlin
compared
to
Madrid
on
average?
9. Find
the
top-­‐10
(in
terms
of
the
number
of
listings)
hosts
(host_ids,
host_names)
in
Spain.
10. Find
the
top-­‐10
rated
(review_score_rating)
apartments
(id,name)
in
Barcelona.
---------
For each query: <br>
Query a:
*Description of logic:*<br>
What does the query do and how do I decide to solve it
SQL statement
<The SQL statement>
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
5. The query finds the dates that a specified host (we use 'Viajes Eco') has available accommodations for rent.

    ```sql
    -- TODO
    ```

6. The query finds all the pairs (host_ids, host_names) that only have one listing online.


    ```sql
    -- TODO
    ```

7. The query computes the difference of price (average) between listings with or without Wifi.
    ```sql
    -- TODO
    ```
8. The query computes the difference of price in a room with 8 beds in Berlin compared to Madrid.

    ```sql
    -- TODO
    ```
9. The query finds the top-10 host (host_ids, host_names) in terms of number of listings per host in Spain.

    ```sql
    -- TODO
    ```
10. The query finds the top-10 listings (review_score_rating) in terms of review_score_rating apartments in Barcelona.

    ```sql
    -- TODO
    ```
