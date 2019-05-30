create_index_1 = """CREATE INDEX listing_on_bed_and_price ON Listing(beds, price);"""
create_index_2 = """CREATE INDEX host_on_name_and_id ON Host(host_name(60), host_id);"""
create_index_3 = """CREATE INDEX since_on_host_with_host_id ON Host (host_since, host_id);"""
create_index_4 = """CREATE INDEX host_v_id_descr ON Host_verification (host_verification_description(100));"""
create_index_5 = """CREATE INDEX square_feet_on_listing ON Listing (square_feet);"""

create_indexes = [create_index_1,
                  create_index_2,
                  create_index_3,
                  create_index_4,
                  create_index_5]
