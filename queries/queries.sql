
-- Create Table combining salaries and stats from 1990-2023
CREATE TABLE salaries_and_stats AS
SELECT 
    salaries.salary,
    stats.*
FROM 
    master_player_salaries AS salaries
INNER JOIN 
    player_stats AS stats 
ON 
    stats."Name" = salaries.name
AND 
    stats.season = salaries.season;


-- Create Table combining Salries and Stats with player bio metric data
CREATE TABLE salaries_stats_heights AS
SELECT 
    players."pos",
	players."height",
	players."weight",
	players."age",
	players."nationality",
	players."college-team",
	players."draft-status",
    stats.*
FROM 
    salaries_and_stats AS stats
INNER JOIN 
    player_biometric_data AS players 
ON 
    stats."Name" = players.name
AND 
    stats.season = players.season;



-- Highest percentile Scorers with Heights N Weights

SELECT

stats."Name",
stats."PPG",
PERCENT_RANK() OVER ( order by stats."PPG" DESC) as ranking,
stats.height,
stats.weight,
stats.salary,
stats.season

from salaries_stats_heights as stats

where stats."PPG" >=30

-- Player Stats going back to 1970

SELECT

stats."Name",
stats."PPG",
PERCENT_RANK() OVER ( order by stats."PPG" DESC) as ranking,
stats.season

from player_stats as stats

where stats."PPG" >= 29.5


-- Selecting for Top Scorers in last 9 seasons

SELECT

stats."Name",
stats."PPG",
PERCENT_RANK() OVER ( order by stats."PPG" DESC) as ranking,
stats.season

from player_stats as stats

where stats."PPG" >= 29.5 and Substring(stats.season, 1, 4)::int >= 2015