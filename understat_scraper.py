import json
import re

import bs4
import requests

__author__ = 'Ifeanyi Obinelo'

LEAGUES = ['EPL', 'La_liga', 'Bundesliga', 'Serie_A', 'Ligue_1', 'RFPL']

BASE_URL = 'https://understat.com'

JSON_PARSE_REGEX = re.compile("JSON.parse\('(.*)'\)")


def get_match_url(match_id):
    return f'{BASE_URL}/match/{match_id}'

def get_league_url(league, season):
    return f'{BASE_URL}/league/{league}/{season}'


def scrape_match_data(match_id):
    """Scrapes match data from understat.com"""
    # Get the match URL.
    match_url = get_match_url(match_id)
    # Fetch data from the URL.
    r = requests.get(match_url)
    # Parse with BeautifulSoup.
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    # Find all script tags.
    script_tags = soup.find_all('script')
    # Extract the text we are interested in.
    shots_data, match_info = JSON_PARSE_REGEX.findall(script_tags[1].string)
    # Fix encodings.
    shots_data = shots_data.encode('utf-8').decode('unicode_escape')
    match_info = match_info.encode('utf-8').decode('unicode_escape')
    # Load in JSON format.
    shots_data = json.loads(shots_data)
    match_info = json.loads(match_info)

    output = {
        'shots_data': shots_data, 
        'match_info': match_info
        }
    return output

def scrape_league_data(league, season):
    """Scrapes league data from understat.com"""
    # Get the league url.
    league_url = get_league_url(league, season)
    # Fetch data from the URL.
    r = requests.get(league_url)
    # Parse with BeautifulSoup.
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    # Find all script tags.
    script_tags = soup.find_all('script')

    for tag in script_tags:

        if tag.string == None:
            continue
    
        # Save the tags that contain useful information.
        if 'datesData' in tag.string:
            dates_data_tag = tag
        if 'teamsData' in tag.string:
            teams_data_tag = tag
        if 'playersData' in tag.string:
            players_data_tag = tag

    # Extract the text we are interested in.
    dates_data = JSON_PARSE_REGEX.findall(dates_data_tag.string)[0]
    teams_data = JSON_PARSE_REGEX.findall(teams_data_tag.string)[0]
    players_data = JSON_PARSE_REGEX.findall(players_data_tag.string)[0]
    # Fix encodings.
    dates_data = dates_data.encode('utf-8').decode('unicode-escape')
    teams_data = teams_data.encode('utf-8').decode('unicode-escape')
    players_data = players_data.encode('utf-8').decode('unicode-escape')
    # Load the data in JSON format.
    dates_data = json.loads(dates_data)
    teams_data = json.loads(teams_data)
    players_data = json.loads(players_data)

    output = {
        'dates_data': dates_data, 
        'teams_data': teams_data, 
        'players_data': players_data
        }
    return output


