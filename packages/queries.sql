

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