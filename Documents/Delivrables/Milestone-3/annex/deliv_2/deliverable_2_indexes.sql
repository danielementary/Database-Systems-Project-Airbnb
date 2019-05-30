
-----------------query 01---------------------
--without index : 2530ms
--with index : 0.34ms
CREATE INDEX listing_on_bed_and_price ON Listing(beds, price);
DROP INDEX listing_on_bed_and_price ON Listing;

-----------------query 02---------------------
--without index : 320ms
--no index improvement

-----------------query 03---------------------
--without index : 245ms
--no index improvement

-----------------query 04---------------------
--without index : 83800ms
--with index : 2948ms
CREATE INDEX host_on_name_and_id ON Host(host_name(60), host_id);
DROP INDEX host_on_name_and_id ON Host;
-----------------query 05---------------------
--without index : 38ms
--no index improvement

-----------------query 06---------------------
--without index : 16698ms
--no index improvement


-----------------query 07---------------------
--without index : TODO

-----------------query 08---------------------
--without index : TODO


-----------------query 09---------------------
--without index : 4623sec
--no index improvement

-----------------query 10---------------------
--without index : 35ms
--no index improvement
