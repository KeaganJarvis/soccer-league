#!/usr/bin/python
import click
from tinydb import TinyDB, Query


class Match_Result:
    """
    A class to process the reult of a match
    """
    team_a = None
    team_b = None
    score_a = None
    score_b = None
    points_a = None
    points_b = None

    def __init__(self,match):
        """
        Match result contructor that performs string manipulation to get the data from the input match string into individual variables
        """
        team_a, team_b = match.split(',')
        team_b = team_b[1:] #get rid of space at beggining of team_b
        self.score_a = int(team_a[-1])
        self.team_a = team_a[:-2] #drop score from team name
        self.score_b = int(team_b[-1])
        self.team_b = team_b[:-2] #drop score from team name
    
    def getResult(self):
        """
        Function to determine the log points for each team depending on the matches results
        win = 3 points
        draw = 1 points
        loss = 0 points
        """
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
    """
    Check whether the db contains an entry for the team's based on their name
    """
    query = db.search(log.name == name)
    if query:
        return True
    else:
        return False

def process_match(match):
    """
    for each individual match, process the results of that match and update the log accordingly
    """
    db = TinyDB('soccer_league.json')
    current_standings = Query()
    #check result of the match
    match_result = Match_Result(match)
    match_result.getResult()
    previous_points = 0
    new_points = 0
    if team_exists(db,current_standings,match_result.team_a):
        #add the points onto the existing points
        previous_points = db.search(current_standings.name == match_result.team_a)[0]['points']
        new_points = previous_points + match_result.points_a
        db.update({'points': new_points}, current_standings.name == match_result.team_a) 
    else:
        db.insert({'name': match_result.team_a, 'points': match_result.points_a})
    #TODO repeating oneself...
    if team_exists(db,current_standings,match_result.team_b):
        #add the points onto the existing points
        previous_points = db.search(current_standings.name == match_result.team_b)[0]['points']
        new_points = previous_points + match_result.points_b
        db.update({'points': new_points}, current_standings.name == match_result.team_b)
    else:
        db.insert({'name': match_result.team_b, 'points': match_result.points_b})
    


def process_file(file_path):
    """
    Get each match from the input file to be processed
    """
    file_of_matches=open(file_path, "r")
    #loop over every line to get process individual matches
    for match in file_of_matches:
        process_match(match[:-1])#drop the \n from end of line 
    file_of_matches.close()

def display_log():
    """
    Sorts the log on points and then team name, outputs the log in the correct format
    """
    db = TinyDB('soccer_league.json')
    log = db.all()
    decorated = [(dict_["points"], str(dict_["name"])) for dict_ in log] #change the list of dictionary items into a list of tuples
    new_list = []
    #extremely hackey sorting method to be able to sort on points first, then on the the team name
    #only works on first letter of the team name...
    #should have used a better DB rather than tiny db that allows sorting of data
    while decorated:
        minimum = decorated[0]  # arbitrary number in list 
        for x in decorated: 
            if x[0] > minimum[0]:
                minimum = x
            elif x[0] == minimum[0] and x[1][0]<minimum[1][0]:
                minimum = x
        new_list.append(minimum)
        decorated.remove(minimum)    

    for idx,item in enumerate(new_list):
        log_position = idx + 1
        print (str(log_position) + '. ' + item[1] + ', ' + str(item[0]))

@click.command(help="Script that gives the current log standings for a soccer league, a file can be input to update the log standings with other matches")
@click.option("--file","-f", default=None, help="The path to the file that contains soccer match results, each on a new line in the correct format")
def main(file=None):
    """
    Entry function to get CLI input paramters
    """
    if file:
        process_file(file)
    display_log()


if __name__ == '__main__':
    #Run the server using the default config
    main()