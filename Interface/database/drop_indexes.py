drop_index_1 = """DROP INDEX listing_on_bed_and_price ON Listing;"""
drop_index_2 = """DROP INDEX host_on_name_and_id ON Host;"""
drop_index_3 = """DROP INDEX square_feet_on_listing ON Listing;"""
drop_index_4 = """DROP INDEX host_v_id_descr ON Host_verification;"""
drop_index_5 = """DROP INDEX since_on_host_with_host_id ON Host;"""

drop_indexes = [drop_index_1,
                drop_index_2,
                drop_index_3,
                drop_index_4,
                drop_index_5]
