-- room_type_id
CREATE INDEX room_type_id_on_listing ON Listing(room_type_id) -- doesn't change anything
--DROP INDEX room_type_id_on_listing ON Listing;


--!!!!! this index already exists !!!! no improvement 