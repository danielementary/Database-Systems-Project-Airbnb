CREATE INDEX since_on_host_with_host_id USING BTREE ON Host(host_since, host_id); -- goes from 1min 17sec to 1min 9sec
--DROP INDEX since_on_host_with_host_id ON Host;

CREATE INDEX available_on_calendar ON Calendar(calendar_available)
--DROP INDEX available_on_calendar ON Calendar;
