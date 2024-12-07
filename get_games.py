import requests
import json
from datetime import datetime, timedelta
import time

def fetch_games_for_date(date):
    """Fetch all games for a specific date from the NCAA API"""
    url = date.strftime(
        "https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/%Y/%m/%d/all-conf"
    )
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data for {date}: {e}")
        return None

def process_games(raw_data):
    """Convert raw API data into our desired format"""
    games = []
    
    if not raw_data or 'games' not in raw_data:
        return games
    
    for game in raw_data['games']:
        try:
            game_data = {
                'date': game['game']['startDate'],
                'home_team': game['game']['home']['names']['full'],
                'away_team': game['game']['away']['names']['full'],
                'score_home': game['game']['home']['score'],
                'score_away': game['game']['away']['score']
            }
            games.append(game_data)
        except KeyError as e:
            print(f"Error processing game data: {e}")
            continue
            
    return games

def get_season_games(start_date, end_date):
    """Get all games between start_date and end_date"""
    all_games = []
    current_date = start_date
    
    while current_date <= end_date:
        print(f"Fetching games for {current_date.strftime('%Y-%m-%d')}")
        
        daily_data = fetch_games_for_date(current_date)
        if daily_data:
            games = process_games(daily_data)
            all_games.extend(games)
        
        # Add delay to be nice to the API
        time.sleep(1)
        current_date += timedelta(days=1)
    
    return all_games

def main():
    # Example date range for a season (adjust as needed)
    start_date = datetime(2023, 11, 6)  # Season typically starts in November
    end_date = datetime(2024, 4, 8)     # Usually ends in early April
    
    games = get_season_games(start_date, end_date)
    
    # Write to JSON file
    with open('basketball_games.json', 'w') as f:
        json.dump(games, f, indent=2)
    
    print(f"Saved {len(games)} games to basketball_games.json")

if __name__ == "__main__":
    main()
