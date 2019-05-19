-- Query 1 )
SELECT count(Host.host_id), city_name
FROM Host,
	Listing,
	Neighbourhood,
	City
WHERE Listing.host_id = Host.host_id
	AND Listing.neighbourhood_id = Neighbourhood.neighbourhood_id
	AND Neighbourhood.city_id = City.city_id
	AND Host.host_id IN (
		SELECT Host.host_id
		FROM Host,
			Listing
		WHERE Listing.host_id = Host.host_id
			AND square_feet IS NOT NULL
		)
GROUP BY city_name;
