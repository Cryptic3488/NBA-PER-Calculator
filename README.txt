# NBA Player Data Scraper & Analyzer

## Overview
The National Basketball Association (NBA) is the most popular basketball league in the United States, 
renowned for its intense gameplay characterized by high scoring matches. Due to its fast paced nature, 
it allows us to receive plenty of data that can be analyzed. The player efficiency rating (PER) is an 
example of one such metric, as it is a variable that we have created that is calculated by taking in a 
wide range of basketball data and assigns a rating for the player based on their performances. 
In this project, we aim to scrape data off of the web to create our own player efficiency rating variable 
(PER), as well as use that rating to compare how efficiently the top players of each basketball position 
match up. We want to see if it is possible to create a measure that can accurately show how skilled a
player is. Our PER rating will have its own formula that takes into account offensive and defensive statistics
of a player. While the top ten players with the highest PER may not always align with the general consensus
on the top ten players overall, it does offer valuable insight into their performance in the league.

## Introduction
This Python program scrapes NBA player data from basketball-reference.com for a specified year, 
calculates Player Efficiency Rating (PER), and provides various analyses based on the scraped data.
It utilizes web scraping techniques, SQLite database management, and data analysis algorithms to offer
insights into NBA player performances.

## Prerequisites
To run this program, ensure you have the following installed:
- Python 3.x
- Required Python libraries: `sqlite3`, `os.path`, `requests`, `BeautifulSoup`, `re`

## Usage

This program needs to be run by the user, and the code will handle the rest. No user input is required for this
program to run, all functions will run automatically. However, prior to running the program the user must 
manually change what years to scrape for in the main function. The program will print the top 75 overall and
top 10 players of their position by player efficiency rating.

**Run the Program:**
    ```
    python nba_player_data_scraper.py
    ```

## Functionality
### 1. Scrape NBA Player Data
- `scrape_nba_player_data(year)`: Scrapes NBA player data for the specified year from basketball-reference.com.

### 2. Create NBA Database
- `create_nba_database(headers, player_data, year)`: Creates an SQLite database file for the specified year,
stores NBA player data, and renames columns for clarity.

### 3. Calculate Player Efficiency Rating (PER)
- `PER_calculator(year)`: Calculates the Player Efficiency Rating (PER) for each player based on their
statistics and updates the SQLite database.

### 4. Print Top Players
- `print_top_players(year)`: Prints the top 10 players at each position and the top 75 players overall based
on PER, omitting players who didn't play over 50 games.

### 5. Print Top Players by Team
- `print_top_players_by_team(year)`: Prints the ranking of the top 5 players on each team based on PER,
along with the number of games played and started by each player.

## Main Function
The `main()` function orchestrates the entire process by specifying the years to scrape data for,
calling relevant functions, and displaying the outputs.

## Note
- Only the printing for the year 2024 is kept due to the large amount of output generated
for each year. However, databases for 2020-Present have been created are available for browsing purposes.

## Author
This program is authored by Andrew Byerly, Mason Cromwell, and Hamdan Ashfaq. 
For any queries or suggestions, please contact byerly_a1@denison.edu. 

# The following program is was used for testing purposes but I thought it'd be appropriate to include.

# NBA Database File Deletion Script

## Introduction
This Python script allows you to delete an NBA database file corresponding to a specific year. It checks if 
the database file exists and deletes it if found, providing feedback on the success or failure of the operation.

## Usage
1. **Modify Database File Path:**
    - Replace 'year' in the variable `db_file` with the desired year of the database file to be deleted.

2. **Run the Script:**
    - Execute the Python script in your preferred environment.

3. **Check Output:**
    - The script will output whether the database file was successfully deleted or if it does not exist.

## Prerequisites
- Python 3.x
- Operating System: Windows, Linux, macOS

## Note
- Ensure that you have appropriate permissions to delete files in the specified directory.
- This script only deletes the database file and does not perform any other operations on the database 
or its contents.

## Author
This program is authored by Andrew Byerly. 
For any queries or suggestions, please contact byerly_a1@denison.edu.

### Analysis and Final Conclusions

The Player Efficiency Rating is a system that we created that assigns a score to each player based on their 
statistics. They achieve a higher rating by getting points, rebounds and assists. Receiving personal fouls 
and turnovers penalize their rating. The higher the players rating, the more stats they are putting up a game.
For example, it is widely thought that Nikola Jokic is the best player and MVP favorite in the league currently,
yet he has the has the 4th highest PER rating of any player. This has some interesting implications as we can
start to see that the MVP award may not just be the best player in the league, but the best player on a top tier
team (2 seed and above in their respective conference). How much does media narative and team success affect MVP
chances? Well, our PER statistic says that it's more important than individual efficiency. Additionally,
although it is widely debated who the true top 10 players in the NBA are, our top 10 provides a concrete 
ranking. While we are able to see the players with the higher PER rating, we also printed out the top 10 
players with the highest PER by position. The averages of the top ten players in a position are point guards 
(52), power forwards  (48), centers(45), shooting guards (42) and small forwards(39). 

Point guards control the offensive floor, so it is no surprise that they have the highest PER.
Their abilities to set up plays and control the tempo of the game give them stats that strongly boost their 
PER score. Power forwards come in at second, as they have the ability to score baskets in many locations and
aid the defense with their rebounding and guarding skills. Centers come in third which come with a large 
stature that allows them to score in the paint and accumulate a high PER with their defensive presence. 
Shooting guards are often high scorers for their team. Though they may be able to receive a lot of points, 
they do not control the offensive scheme as well as a point guard does which may be why their PER average ranks
on the lower side. Small forwards come in at last on the list. They are responsible for doing a little bit of
everything in terms of scoring and defending. However, as they have no specialized area that they excel at,
that may impact the weight of their rating.

The conclusion that we drew from this project is that we are able to create a PER rating that accurately 
describes how efficient a player is. The PER formula created favors good performance in a game, while
penalizing fouls and other mishaps a player may have. As such, our players with the highest PER are widely
regarded as the best players in the league. Though the top ten on our list may not be completely indicative
of the players ranking in the NBA, it offers valuable insight as to how they compare overall. This goes to
show that it is possible to create a measure that shows how skilled a player is by using their in game data. 
As for the difference in the top ten players for each position by PER, we can use our basketball knowledge to
understand why each position has that average rating. It is important to note that our PER formula favors 
some stats over others, so a player in a position that often receives those favorable stats will have an
easier time receiving that higher PER rating. This in no way shows that one position is more valuable than
another, more that each position has their own specialized role on the court. Players like point guards will
have the highest PER due to their control of the offense, which nets them many points and assists. 
Power forwards and centers can use their size and position on the court to make a mixture of offensive and
defensive plays. While shooting guards and small forwards are skilled at scoring, they may only be able to
excel at one area of play. This drags their rating down as they do not have multiple stats that they can
boost in play. The PER metric gives us an insight into the stats a player receives, but does not completely
determine a player's worth. Of course players with higher PER are highly skilled and talented,
but our PER measures certain stats as more valuable than others. This may be why some positions often
have a higher PER value than others. Of course, basketball is a team game at its core. It takes the combined
effort of all the players on the court with their strengths and weaknesses to win a game. Our PER can give us
the gist of a certain player, but does not determine their worth. But most of all, while Nikola Jokic is
widely considered one of the top players and a favorite for MVP, his PER ranks fourth among all players.
This suggests that individual efficiency may not be the sole determinant for accolades like MVP. 
Team success and media narratives could play significant roles, as evidenced by our analysis.

# Credits

Hamdan Ashfaq - ashfaq_h1@denison.edu
Andrew Byerly - byerly_a1@denison.edu
Mason Cromwell - cromwe_m1@denison.edu
Data - "https://www.basketball-reference.com”