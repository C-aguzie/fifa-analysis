-- Top 10 players by overall rating
SELECT name, overall 
FROM fifa
ORDER BY overall DESC 
LIMIT 10;

-- Top young players (under 23) by potential
SELECT name, age, potential 
FROM fifa
WHERE age < 23
ORDER BY potential DESC;

-- Average overall rating by age
SELECT age, avg(overall) from fifa
group by age
order by age asc;
 
select age, count(name) as player_count from fifa
group by age
order by player_count DESC;

SELECT count(name) as player_count from fifa;