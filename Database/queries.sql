----------------SQL_Queries-------------------

---------------------01-----------------------
SELECT AVG(price)
FROM  Listing
WHERE beds = 8;

---------------------02-----------------------
SELECT AVG(L.price)
FROM  Listing L, Listing_amenity_map M
WHERE L.listing_id = M.listing_id
      AND L.amenities_id EXISTS ( SELECT A.amenities_id
                                  FROM Amenities A
                                  WHERE A.amenities = 'TV' --??
                                );

---------------------03-----------------------
SELECT H.host_name
FROM  Host H, Listing L
WHERE H.host_id = L.host_id
      AND L.host_id EXISTS  ( SELECT C.host_id
                              FROM Calender C
                              WHERE C.calendar_available = '1'
                                    AND C.calendar_date >= 2019-03-01
                                    AND C.calendar_date < 2019-10-01
                                    --TODO finish this query
                            );
---------------------04-----------------------
---------------------05-----------------------
---------------------06-----------------------
---------------------07-----------------------
---------------------08-----------------------
---------------------09-----------------------
---------------------10-----------------------
