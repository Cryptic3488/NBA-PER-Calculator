# ==========================================================================================================
# NBA Player Data Scraper and Analyzer
# April 2024
# Written by Andrew Byerly, Hamdan Ashfaq, and Mason Cromwell
# This program is designed to scrape NBA player data from basketball-reference.com, 
# store it in an SQLite database,calculate Player Efficiency Rating (PER) for each player,
# and provide various analyses such as top players by position, overall top players, and top players by team.
# ===========================================================================================================

import sqlite3
import os.path
import requests
from bs4 import BeautifulSoup
import re

def scrape_nba_player_data(year):
    """
    Scrapes NBA player data from basketball-reference.com for the specified year.

    Parameters:
        year (int): The year for which to scrape the data.

    Returns:
        sanitized_headers (list): A list of sanitized column headers.
        player_data (list): A list of lists containing player information.
    """

    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"id": "per_game_stats"})

    headers = [th.getText().strip().replace("%", "Pct") for th in table.findAll("tr", limit=2)[0].findAll("th")]
    headers = headers[1:]

    sanitized_headers = []
    for header in headers:
        sanitized_header = re.sub(r'\W+', '', header)
        if sanitized_header[0].isdigit():
            sanitized_header = "_" + sanitized_header
        sanitized_headers.append(sanitized_header)

    player_data = []
    rows = table.findAll("tr")[1:]
    for row in rows:
        player_info = [td.getText() for td in row.findAll("td")]
        player_data.append(player_info)

    return sanitized_headers, player_data

def create_nba_database(headers, player_data, year):
    """
    Creates an SQLite database file for the specified year if it doesn't exist.
    Creates a table for storing NBA player data.
    Inserts scraped player data into the database.
    Renames columns for better clarity.

    Parameters:
        headers (list): A list of sanitized column headers.
        player_data (list): A list of lists containing player information.
        year (int): The year for which to create the database.
    """

    db_file = f"nba_database_{year}.db"

    if not os.path.isfile(db_file):  # Check if the database file exists
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create a table for player data
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS players (
            player_name TEXT,
            player_team TEXT,
            {", ".join([f'{header} TEXT' for header in headers if header not in ['Player', 'Tm']])},
            PER REAL,
            PRIMARY KEY (player_name, player_team)
        )
        """
        cursor.execute(create_table_query)

        # Insert player data into the table
        for player_info in player_data:
            # Check if the player_info is empty or incomplete
            if len(player_info) < 2:
                continue
            
            # Split player data into player name, team name, and statistics
            player_name, player_team = player_info[:2]

            # Check if the record already exists in the database
            cursor.execute("SELECT COUNT(*) FROM players WHERE player_name = ? AND player_team = ?", (player_name, player_team))
            if cursor.fetchone()[0] == 0:  # If the record does not exist, insert it
                player_stats = player_info[2:]

                # Fill missing values with 0
                player_stats_filled = [stat if stat else '0' for stat in player_stats]

                # Generate insert query dynamically based on the number of columns in player data
                insert_query = f"""
                INSERT INTO players (player_name, player_team, {", ".join([header for header in headers if header not in ['Player', 'Tm']])}, PER)
                VALUES (?, ?, {", ".join(["?" for _ in player_stats_filled])}, ?)
                """
                cursor.execute(insert_query, [player_name, player_team] + player_stats_filled + [0])  # Initialize PER to 0

        # Rename columns
        cursor.execute('ALTER TABLE players RENAME COLUMN player_team TO Position')
        cursor.execute('ALTER TABLE players RENAME COLUMN Age TO Tm')
        cursor.execute('ALTER TABLE players RENAME COLUMN Pos TO Age')
        
        conn.commit()
        conn.close()
        print(f"NBA database for {year} created successfully!")
    else:
        print(f"NBA database for {year} already exists, skipping creation.")

def PER_calculator(year):
    """
    Calculates the Player Efficiency Rating (PER) for each player based on their statistics.
    Updates the SQLite database with the calculated PER.

    Parameters:
        year (int): The year for which to calculate PER.
    """

    headers, player_data = scrape_nba_player_data(year)

    # Fetch player data from the database
    db_file = f"nba_database_{year}.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    player_records = cursor.fetchall()

    for player_record in player_records:
        # Extract relevant statistics
        minutes_played = float(player_record[6])
        points = float(player_record[28])
        assists = float(player_record[23])
        defensive_rebounds = float(player_record[21])
        offensive_rebounds = float(player_record[20])
        steals = float(player_record[24])
        blocks = float(player_record[25])
        two_pointers_made = float(player_record[13])
        three_pointers_made = float(player_record[10])
        two_pointers_attempted = float(player_record[14])
        three_pointers_attempted = float(player_record[11])
        turnovers = float(player_record[26])
        personal_fouls = float(player_record[27])

        # Calculate PER
        PER = (
            points + assists + (defensive_rebounds / 2) + offensive_rebounds +
            (steals * 2) + (blocks * 2) + two_pointers_made +
            (three_pointers_made * 2)
        ) - (
            (two_pointers_attempted / 2) + three_pointers_attempted +
            (turnovers * 2) + (personal_fouls / 3)
        ) / minutes_played

        # Update the database with the calculated PER
        cursor.execute("UPDATE players SET PER = ? WHERE player_name = ? AND Position = ?", (PER, player_record[0], player_record[1]))

    conn.commit()
    conn.close()
    print(f"PER calculation and update completed successfully for {year}!")

def print_top_players(year):
    """
    Prints out the top 10 players at each position and the top 75 players overall based on PER,
    omitting players who didn't play over 50 games.

    Parameters:
        year (int): The year for which to print top players.
    """

    db_file = f"nba_database_{year}.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch players who played over 50 games and their PER
    cursor.execute("SELECT player_name, Position, PER FROM players WHERE G >= 50")
    player_records = cursor.fetchall()

    # Organize players by position
    players_by_position = {}
    for player_record in player_records:
        player_name, position, per = player_record
        if position not in players_by_position:
            players_by_position[position] = []
        players_by_position[position].append((player_name, per))

    # Print top 10 players at each position
    print(f"Top 10 Players for {year} at Each Position:")
    for position, players in players_by_position.items():
        players_sorted = sorted(players, key=lambda x: x[1], reverse=True)[:10]
        print(f"{position}:")
        for i, (player_name, per) in enumerate(players_sorted):
            print(f"{i+1}. {player_name} (PER: {per:.2f})")
        print()

    # Print top 75 players overall
    print(f"Top 75 Players for {year} Overall:")
    all_players = [(player_name, per) for players in players_by_position.values() for player_name, per in players]
    all_players_sorted = sorted(all_players, key=lambda x: x[1], reverse=True)[:75]
    for i, (player_name, per) in enumerate(all_players_sorted):
        print(f"{i+1}. {player_name} (PER: {per:.2f})")

    conn.close()

def print_top_players_by_team(year):
    """
    Prints out the ranking of the top 5 players on each team based on PER, along with the number of games played
    and started by each player.

    Parameters:
        year (int): The year for which to print top players by team.
    """

    db_file = f"nba_database_{year}.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch all teams
    cursor.execute("SELECT DISTINCT Tm FROM players")
    teams = [team[0] for team in cursor.fetchall()]

    # Print top 5 players on each team
    print(f"Top 5 Players by Team for {year}:")
    for team in teams:
        print(f"Team: {team}")
        cursor.execute("SELECT player_name, PER, G, GS FROM players WHERE Tm = ? ORDER BY PER DESC LIMIT 5", (team,))
        players = cursor.fetchall()
        for i, (player_name, per, games_played, games_started) in enumerate(players, start=1):
            print(f"{i}. {player_name} (PER: {per:.2f}, Games Played: {games_played}, Games Started: {games_started})")
        print()

    conn.close()

def main():
    # Note: I've created databases for 2020-Present but only kept 2024 as each year has a large amount of output
    # If you're curious, I've still kept the databases for browsing purposes. (Sorting by PER is interesting)
    years = [2024]  # List of years to scrape data for
    for year in years:
        headers, player_data = scrape_nba_player_data(year)
        create_nba_database(headers, player_data, year)
        PER_calculator(year)
        #print_top_players(year)
        #print_top_players_by_team(year)

main()