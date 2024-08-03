
import pandas as pd
from bs4 import BeautifulSoup

def extract_player_salaries(html_content, year:int)->pd.DataFrame:
    """
    Grabs all of the players salaries from 2011-2024

    Args:
        html_content (_type_): HTML Content
        year (int): Year

    Returns:
        _type_: Pandas Dataframe
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    player_data = []
    players = soup.find_all('li', class_='list-group-item')

    for player in players:
        data = {}

        name_div = player.find('div', class_='link')
        salary_span = player.find('span', class_='medium')
        team_position_small = player.find('small')
        
        if name_div:
            
            data['player'] = name_div.text.strip()

            block = team_position_small.text.strip().split(",")
            team = block[0]
            pos = block[1]
            data['team'] = team
            data["pos"] = pos
            salary = salary_span.text.strip().replace("$", "").replace(",", "")
            data['salary'] = int(salary)
            player_data.append(data)
    
    df = pd.DataFrame(player_data)
    df["season"] = str(year) + "-" + str(year+1)
    return df

def extract_team_info(html_content, year:int)->pd.DataFrame:
    """
    This functions purpose is to grab all the
    NBA teams and salaries

    Args:
        html_content (_type_): HTML Content
        year (_type_): Integer

    Returns:
        Pandas Dataframe
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tds = soup.findAll("td")
    stats = [td.text.strip() for td in tds]
    sep_blocks = " ".join(stats).split(".")[1:]
    teams_salaries = [block.strip().split(" ")[:4] for block in sep_blocks]
    
    df = []
    for block in teams_salaries:
        teams = {}
        for idx, part in enumerate(block):
            if "$" in part and block[idx-1].isalpha():
                integer = part.replace("$", "").replace(",", "")
                teams["salary"] = int(integer)
            elif part.isalpha():
                if block[idx+1].isalpha():
                    teams["Team"] = part + " " + block[idx+1]
                    df.append(teams)
                elif not block[idx+1].isalpha() and not block[idx-1].isalpha():
                    teams["Team"] = part
                    df.append(teams)
    
    master_df= pd.DataFrame(df)
    
    nba_team_abbreivated = {
  "Atlanta":"ATL",
  "Cleveland": "CLE",
  "New York": "NYK",
  "Charlotte": "CHA",
  "Detroit": "DET",
  "Dallas": "DAL",
  "Philadelphia": "PHI",
  "Milwaukee": "MIL",
  "Phoenix":"PHX",
  "Brooklyn":"BKN",
  "Boston":"BOS",
  "Portland":"POR",
  "Golden State":"GSW",
  "San Antonio":"SAS",
  "Indiana":"IND",
  "Utah":"UT",
  "Oklahoma City":"OKC",
  "Houston":"HOU",
  "Denver":"DEN",
  "LA Clippers":"LAC",
  "Chicago":"CHI",
  "Washington":"WAS",
  "Sacramento":"SAC",
  "Miami":"MIA",
  "Minnesota":"MIN",
  "Orlando":"ORL",
  "New Orleans":"NOP",
  "Memphis":"MEM",
  "Toronto":"TOR",
  "LA Lakers":"LAL"
}
    
    master_df["Team"] = master_df["Team"].apply(lambda x: nba_team_abbreivated[x])
    master_df["season"] = year
    return master_df

def extract_nba_stats(html_content, year:int)->pd.DataFrame:
  """
  Extracts Player Statistical Information

  Args:
      html_content (_type_): HTML Content
      year (_type_): Integer

  Returns:
      _type_: Pandas Dataframe
  """
  
  soup = BeautifulSoup(html_content, 'html.parser')
  master_df = []
  tds = soup.find_all("td")
  player_stats = [td.text.strip() for td in tds]
  player_columns = ["Rank", "Name", "Team", "GP", "MPG", "PPG", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", "ORB", "DRB", "RPG", "APG", "SPG", "BPG", "TOV", "PF"]

  count = 0
  player_dict = {}
  for idx, player_stat in enumerate(player_stats):
    
    if count == 22:
      master_df.append(player_dict)
      player_dict = {}
      count = 0
    else:
      col = player_columns[count]
      player_dict[col] = player_stat
      count +=1
  
  df = pd.DataFrame(master_df)
  df["season"] = str(year-1) +'-'+ str(year)
  return df

def load_into_db(df:pd.DataFrame, engine, table:str):
  """
  Loads Pandas Dataframe into DB

  Args:
      df (pd.DataFrame): Dataframe
      engine (_type_): SQL Engine
      table (str): STR of Table Name
  """
  
  try:
      df.to_sql(table, engine, if_exists='replace', index=False)
      print("Data successfully written to the database.")
  except Exception as e:
      print(f"Database operation failed. Error: {e}")