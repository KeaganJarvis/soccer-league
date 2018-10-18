#!/usr/bin/python
import click
from tinydb import TinyDB, Query

#EITHER using stdin/stdout OR taking filenames on the command line is fine
#You can expect that the input will be well-formed. There is no need to add special handling for malformed input files.
#NB supporting tests needed
#TODO doc strings

class Match_Result:

    team_a = None
    team_b = None
    score_a = None
    score_b = None
    points_a = None
    points_b = None

    def __init__(self,match):
        team_a, team_b = match.split(',')
        team_b = team_b[1:] #get rid of space at beggining of team_b
        self.score_a = int(team_a[-1])
        self.team_a = team_a[:-2] #drop score from team name
        self.score_b = int(team_b[-1])
        self.team_b = team_b[:-2] #drop score from team name
        # print (team_a)
        # print (score_a)
        # print (team_b)
        # print (score_b)
    
    def getResult(self):
        if self.score_a > self.score_b:
            self.points_a = 3
            self.points_b = 0
        elif self.score_b > self.score_a:
            self.points_a = 0
            self.points_b = 3
        elif self.score_a == self.score_b:
            self.points_a = 1
            self.points_b = 1
     
def team_exists (db, log, name):
    
    query = db.search(log.name == name)
    if query:
        return True
    else:
        return False

def process_match(match):
    db = TinyDB('soccer_league.json')
    current_standings = Query()
    #check result of the match
    match_result = Match_Result(match)
    match_result.getResult()
    # import pudb; pudb.set_trace()
    if team_exists(db,current_standings,match_result.team_a):
        #add the points onto the existing points
        print match_result.team_a
    else:
        db.insert({'name': match_result.team_a, 'points': match_result.points_a})
    #TODO repeating oneself...
    if team_exists(db,current_standings,match_result.team_b):
        #add the points onto the existing points
        print match_result.team_b
    else:
        db.insert({'name': match_result.team_b, 'points': match_result.points_b})
    
    #update the table with points
    #if team exists in DB, increase their points
    #else, insert team into DB with their points

def process_file(file_path):
    file_of_matches=open(file_path, "r")
    #loop over every line to get process individual matches
    for match in file_of_matches:
        process_match(match[:-1])#drop the \n from end of line 
    file_of_matches.close()

def display_log():
    print ("Log")

@click.command()
@click.argument("match",required=False)#, help="Input a single match of the format <Team1Name> <Team1's_score>, <Team2Name> <Team2's_score> (eg Snakes 1, Lions 2")
@click.option("--file","-f", default=None, help="The path to the file that contains soccer match results, each on a new line in the correct format")
def main(file=None,match=None):
    """
    Entry function to get CLI input paramters
    """
    if file:
        process_file(file)
    else:
        process_match(match)
    #after either option, display the log
    display_log()


if __name__ == '__main__':
    #Run the server using the default config
    main()