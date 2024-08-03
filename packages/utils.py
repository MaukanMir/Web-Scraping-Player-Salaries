
import pandas as pd
from bs4 import BeautifulSoup

def extract_player_salaries(html_content, year:int)->pd.DataFrame:
    """
    Grabs all of the players salaries from 2011-2024

    Args:
        html_content (_type_): HTML Content
        year (int): Year

    Returns:
        _type_: _description_
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
        A datafrom with all information
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
    master_df["season"] = year
    return master_df