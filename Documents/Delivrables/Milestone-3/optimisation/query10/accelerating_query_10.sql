CREATE INDEX since_on_host_with_host_id USING BTREE ON Host(host_since, host_id); -- goes from 1min 17sec to 1min 9sec

CREATE INDEX available_on_calendar ON Calendar(calendar_available);
