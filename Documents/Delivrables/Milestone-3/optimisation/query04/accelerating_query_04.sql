CREATE INDEX host_v_id_descr
ON Host_verification(host_verification_description(120), host_verification_id);
--DROP INDEX host_v_id_descr ON Host_verification;




CREATE INDEX canc_policy_verifi_descr_and_id
ON Cancellation_policy(cancellation_policy_name(10), cancellation_policy_id);
--DROP INDEX canc_policy_verifi_descr_and_id ON Cancellation_policy;


CREATE INDEX city_name_and_id
ON City(city_name(10), city_id);
--DROP INDEX city_name_and_id ON City;
