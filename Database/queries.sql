----------------SQL_Queries-------------------

---------------------01-----------------------
SELECT AVG(price)
FROM Listing
WHERE beds = 8;

---------------------02-----------------------
SELECT AVG(L.price)
FROM Listing L,
      Listing_amenity_map M
WHERE L.listing_id = M.listing_id
      AND M.amenity_id = (SELECT A.amenity_id
                          FROM Amenity A
                          WHERE A.amenity_name = "TV");

---------------------03-----------------------
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

---------------------04-----------------------
SELECT COUNT(L.listing_id)  --TODO check it's right
FROM Listing L,
     Host H1,
     Host H2
WHERE L.host_id = H1.host_id
      AND L.host_id = H2.host_id
      AND

---------------------05-----------------------
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
---------------------06-----------------------
---------------------07-----------------------
---------------------08-----------------------
---------------------09-----------------------
---------------------10-----------------------
