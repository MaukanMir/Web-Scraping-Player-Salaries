
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



-- Highest percentile

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