--indexes of the 3 chosen queries

-----------------query 01---------------------
--without index : 1376ms
--with index : 47ms
CREATE INDEX square_feet_on_listing ON Listing (square_feet);

DROP INDEX square_feet_on_listing ON Listing;

-----------------query 04---------------------
--without index : 4430ms
--with index : 1876ms
CREATE INDEX host_v_id_descr ON Host_verification (
	host_verification_description(100)
	);

DROP INDEX host_v_id_descr ON Host_verification;

-----------------query 10---------------------
--without index : 75011ms
--with index : 58957ms
CREATE INDEX since_on_host_with_host_id ON Host (
	host_since,
	host_id
	);

DROP INDEX since_on_host_with_host_id ON Host;
