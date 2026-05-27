4,12,17,29
create database first_proj;
use first_proj;
show tables;
select * from earthquake_info where country='Russia Earthquake';

select count(distinct status) from earthquake_info;
ALTER TABLE earthquake_info
ADD COLUMN country VARCHAR(100);

UPDATE earthquake_info
SET country = CASE 
    WHEN place LIKE '%,%' 
    THEN TRIM(SUBSTRING_INDEX(place, ',', -1))
    ELSE place
END; 

-- 1. Top 10 strongest earthquakes (mag).
select mag,country from earthquake_info order by mag desc limit 10;

-- 2. Top 10 deepest earthquakes (depth_km).
select depth_km,Earthquake_flags from earthquake_info
where Earthquake_flags='Deep'
order by depth_km desc
limit 10;

-- 3. Shallow earthquakes < 50 km and mag > 7.5
select depth_km,Earthquake_flags,mag from earthquake_info
where Earthquake_flags='Shallow'
and depth_km < 50
and mag>7.5

-- 5. Average magnitude per magnitude type (magType).
select avg(mag) as Average_magnitude,magtype from earthquake_info
group by magtype


-- 6. Year with most earthquakes.
select year,count(*) as Count_Earthquake from earthquake_info
group by year;

-- 7. Month with highest number of earthquakes.
select month,count(*) as Count_Earthquake from earthquake_info
group by month
order by Count_Earthquake desc;

-- 8. Day of week with most earthquakes.
select Day_of_week ,count(*) as Count_Earthquake from earthquake_info
group by Day_of_week
order by Count_Earthquake desc;

-- 9. Count of earthquakes per hour of day.--Doubt
select hour(time) as Per_Hour,count(*) as Earthquake_Count
from earthquake_info
group by Per_Hour
order by Per_Hour desc;


-- 10.   Most active reporting network (net)
select net,count(*) as Earthquake_Count
from earthquake_info
group by net
order by Earthquake_Count desc
limit 1;

-- 11.  Top 5 places with highest casualties.
select max(felt) as High_casuality,place
from earthquake_info
group by place
order by High_casuality desc
limit 5; 

-- 13.  Average economic loss by alert level.
select alert,count(*) as Avg_Economic_loss
from earthquake_info
group by alert
order by Avg_Economic_loss desc;

-- 14.Count of reviewed vs automatic earthquakes
select count(*) as Count,status
from earthquake_info
group by status;

-- 15.  Count by earthquake type (type).
select count(*) as Count,type
from earthquake_info
group by type
order by Count desc;

-- 16.  Number of earthquakes by data type (types).
select count(*) as Earthquake_Counts,types
from 
earthquake_info
where type='earthquake'
group by types
limit 50;

-- 18.  Events with high station coverage (nst > threshold).
-- Threshold has been set as 100
select * from earthquake_info
where nst>100
limit 50;

-- 19.  Number of tsunamis triggered per year.
select count(*) as tsunami_Count,year
from earthquake_info
where tsunami=1
group by year
order by year desc;

-- 20.  Count earthquakes by alert levels (red, orange, etc.)
select count(*) as Earthquake_counts,alert
from earthquake_info
group by alert
order by Earthquake_counts desc;

-- 21.Find the top 5 countries with the highest average magnitude of earthquakes in the past 10 years
select country,mag,time from earthquake_info where mag>(select avg(mag) as Avg_magnitude_Earthquake
from earthquake_info) and time>= DATE_SUB(CURDATE(), INTERVAL 10 YEAR)
order by mag desc
limit 5;

-- 22.Find countries that have experienced both shallow 
-- and deep earthquakes within the same month.
select country,year,month from earthquake_info
where Earthquake_flags in ('Deep','Shallow')
group by country,year,month
having count(distinct Earthquake_flags)=2
limit 100;

-- 23.Compute the year-over-year growth rate in the total number of earthquakes globally.
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


-- 24. List the 3 most seismically active regions by combining both frequency 
-- and average magnitude.
select count(*) as Frequency,avg(mag) as Average_magnitude,place
from earthquake_info
group by place
order by Frequency desc,Average_magnitude desc
limit 3;

-- 25. For each country, 
-- calculate the average depth of earthquakes within ±5° latitude range of the equator
select avg(depth_km) as Avg_depth,country
from earthquake_info
where latitude between -5 and +5
group by country
order by Avg_depth desc;

-- 26. Identify countries having the highest ratio of shallow to deep earthquakes
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

--  28. Using the gap and rms columns, 
-- identify events with the lowest data reliability (highest average error margins).
select place,avg(gap) as avg_gap,avg(rms) as avg_rms from earthquake_info
group by place
ORDER BY avg_gap DESC, avg_rms DESC
limit 100;

--  29. Find pairs of consecutive earthquakes (by time) that occurred within 50 km of each other and within 1 hour.
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
    
    -- 30. Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km).
select place,count(*) as deep_earthquake_counts
from earthquake_info
where depth_km>300
group by place
order by deep_earthquake_counts desc
limit 100;





