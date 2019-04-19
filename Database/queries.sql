----------------SQL_Queries-------------------

-------01-------
SELECT AVG(L.price)
FROM Listing L
WHERE L.beds = 8;

-------02-------
SELECT AVG(L.price)
FROM Listing L
WHERE L.amenities_id EXISTS ( SELECT A.amenities_id
                              FROM Amenities A
                              WHERE A.amenities = ''


)
