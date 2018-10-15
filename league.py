#!/usr/bin/python
import click




@click.command()
@click.argument("match",required=False)#, help="Input a single match of the format <Team1Name> <Team1's_score>, <Team2Name> <Team2's_score> (eg Snakes 1, Lions 2")
@click.option("--file","-f", default=None, help="The path to the file that contains soccer match results, each on a new line in the correct format")
def main(file=None,match=None):
    """
    Entry function to get CLI input paramters
    """
    if file:
        print (file)
    else:
        print(match)


if __name__ == '__main__':
    #Run the server using the default config
    main()