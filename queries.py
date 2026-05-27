queries = {

"Top 10 strongest earthquakes": """
SELECT mag, country 
FROM earthquake_info 
ORDER BY mag DESC 
LIMIT 10;
""",

"Top 10 deepest earthquakes": """
SELECT depth_km, Earthquake_flags 
FROM earthquake_info
WHERE Earthquake_flags='Deep'
ORDER BY depth_km DESC
LIMIT 10;
""",

"Shallow high magnitude earthquakes": """
SELECT depth_km, mag 
FROM earthquake_info
WHERE Earthquake_flags='Shallow'
AND depth_km < 50
AND mag > 7.5;
""",

"Average magnitude by magType": """
SELECT AVG(mag) AS avg_mag, magtype
FROM earthquake_info
GROUP BY magtype;
""",

"Earthquakes per year": """
SELECT year, COUNT(*) AS total
FROM earthquake_info
GROUP BY year;
""",

"Earthquakes per month": """
SELECT month, COUNT(*) AS total
FROM earthquake_info
GROUP BY month
ORDER BY total DESC;
""",

"Earthquakes per day of week": """
SELECT Day_of_week, COUNT(*) AS total
FROM earthquake_info
GROUP BY Day_of_week
ORDER BY total DESC;
""",

"Earthquakes per hour": """
SELECT HOUR(time) AS hour, COUNT(*) AS total
FROM earthquake_info
GROUP BY hour
ORDER BY hour;              
""",

"Most active network": """
SELECT net, COUNT(*) AS total
FROM earthquake_info
GROUP BY net
ORDER BY total DESC
LIMIT 1;
""",

"High felt earthquakes": """
SELECT place, MAX(felt) AS max_felt
FROM earthquake_info
GROUP BY place
ORDER BY max_felt DESC
LIMIT 5;
""",

"Top 5 places with highest casualties": """select max(felt) as High_casuality,place
from earthquake_info
group by place
order by High_casuality desc
limit 5; 
""",

"Average economic loss by alert level": """select alert,count(*) as Avg_Economic_loss
from earthquake_info
group by alert
order by Avg_Economic_loss desc;
""",

"Count of reviewed vs automatic earthquakes": """select count(*) as Count,status
from earthquake_info
group by status;
""",

"Count by earthquake type (type)": """select count(*) as Count,type
from earthquake_info
group by type
order by Count desc;
""",

"Number of earthquakes by data type (types)": """select count(*) as Earthquake_Counts,types
from 
earthquake_info
where type='earthquake'
group by types
limit 50;
""",

"Events with high station coverage (nst > threshold)": """select * from earthquake_info
where nst>100 
limit 50;
""",

"Number of tsunamis triggered per year": """select count(*) as tsunami_Count,year
from earthquake_info
where tsunami=1
group by year
order by year desc;
""",

"Count earthquakes by alert levels": """select count(*) as Earthquake_counts,alert
from earthquake_info
group by alert
order by Earthquake_counts desc;
""",

"Top 5 countries with the highest average magnitude of earthquakes in past 10 years": 
"""select country,mag,time from earthquake_info where mag>(select avg(mag) as Avg_magnitude_Earthquake
from earthquake_info) and time>= DATE_SUB(CURDATE(), INTERVAL 10 YEAR)
order by mag desc
limit 5;
""",

"Countries with both shallow and deep earthquakes within the same month": 
"""select country,year,month from earthquake_info
where Earthquake_flags in ('Deep','Shallow')
group by country,year,month
having count(distinct Earthquake_flags)=2
limit 100;
""",

"year-over-year growth rate in the total number of earthquakes globally": """
WITH yearly_earthquakes AS (
    SELECT 
        year,
        COUNT(*) AS total_earthquakes
    FROM earthquake_info
    GROUP BY year
)
SELECT
    year,
    total_earthquakes,
    LAG(total_earthquakes) OVER (ORDER BY year) AS previous_year_total,
    ROUND(
        (
            (total_earthquakes - LAG(total_earthquakes) OVER (ORDER BY year))
            / LAG(total_earthquakes) OVER (ORDER BY year)
        ) * 100,
        2
    ) AS growth_percentage
FROM yearly_earthquakes
ORDER BY year;
""",

"3 most seismically active regions by combining both frequency and average magnitude": """
select count(*) as Frequency,avg(mag) as Average_magnitude,place
from earthquake_info
group by place
order by Frequency desc,Average_magnitude desc
limit 3;
""",

"Average depth of earthquakes within ±5° latitude range for each countries": """
select avg(depth_km) as Avg_depth,country
from earthquake_info
where latitude between -5 and +5
group by country
order by Avg_depth desc;
""",

"Highest ratio of shallow to deep earthquakes": """
SELECT COALESCE(
        1.0 * SUM(CASE WHEN Earthquake_flags = 'Shallow' THEN 1 ELSE 0 END)
        / NULLIF(
            SUM(CASE WHEN Earthquake_flags = 'Deep' THEN 1 ELSE 0 END),
            0
        ),
        0
    ) AS Ratio,
    CASE 
        WHEN place LIKE '%,%' 
        THEN TRIM(SUBSTRING_INDEX(place, ',', -1))
        ELSE place
    END AS country

FROM earthquake_info

GROUP BY 
    CASE 
        WHEN place LIKE '%,%' 
        THEN TRIM(SUBSTRING_INDEX(place, ',', -1))
        ELSE place
    END

ORDER BY Ratio DESC
limit 100;
""",

"Events with the lowest data reliability": """
select place,avg(gap) as avg_gap,avg(rms) as avg_rms from earthquake_info
group by place
ORDER BY avg_gap DESC, avg_rms DESC
limit 100;
""",

"Pairs of consecutive earthquakes that occurred within 50 km of each other and within 1 hour": """
SELECT 
    a.time AS time1,
    b.time AS time2,
    a.place AS place1,
    b.place AS place2
FROM earthquake_info a
JOIN earthquake_info b
    ON a.time < b.time
    AND TIMESTAMPDIFF(SECOND, a.time, b.time) <= 3600
    AND ST_Distance_Sphere(
    POINT(a.longitude, a.latitude),
    POINT(b.longitude, b.latitude)
) <= 50000
    limit 100;
    """,

"Regions with highest frequency of deep-focus earthquakes": """
select place,count(*) as deep_earthquake_counts
from earthquake_info
where depth_km>300
group by place
order by deep_earthquake_counts desc
limit 100;
"""
}