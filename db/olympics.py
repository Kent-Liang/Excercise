from easygui import *
from query_fcns import *
from sys import exit

# GUI functions


def quit(fcns_dict, db, param):
    '''Exits the program.  demo_opts is not used.'''
  
    exit(0)
  
def menu(fcns_dict, db, param):
    '''Display a choicebox giving the user 4 options to research the olympics.'''
    
    field_dict = {'Check if an athlete participated in the 2010 Winter Olympics.':'athlete', \
                  'Look up athletes from a list of countries.':'country', \
                  'Look up medal winners for a sport.':'medal',
                  'Quit.':'quit'}
    
    choice = choicebox('Please select an option:', 'Main Menu', list(field_dict.keys()))
    
    if not choice:
        return 'quit'
    
    return field_dict[choice]

def athlete_lookup(fcns_dict, db, param_list):
    '''Given a list of functions (not used), database and list of parameters
    (not used), prompt the user for an athlete name, display the result of 
    querying whether they are in the database db.'''
    
    name = enterbox( 'Name: ', 'Research an athlete.')
        
    result = is_valid_name(db, name)
    
    if result:
        msg = name + " was an athlete in the 2010 Olympic games."
    else:
        msg = name + " was not an athlete in the 2010 Olympic games."
    msgbox(msg, name)
    
    return 'menu'

def write_to_textbox(msg, title, s):
    
    textbox(msg, title, s)
    save = buttonbox('Do you wish to save this data to a file?', "Save?", \
                     ['Yes, create file', 'Yes, append to file', 'No'])
    if save == 'Yes, create file':
        filename = enterbox('Enter the filename: ', 'Filename')
        f = open(filename, 'w')
        f.write(s.encode('utf-8'))
        f.close()
    elif save == 'Yes, append to file':
        filename = fileopenbox()
        f = open(filename, 'a')
        f.write(s.encode('utf-8'))
        f.close()
    return 'menu'

def country_reps(fcns_dict, db, param_list):
    
    
    # get list of countries in database
    countries = list(get_countries(db))

    for i in range(len(countries)):
        countries[i] = str(countries[i][0])
    choices = multchoicebox('Select your countries:', '', countries)
    athletes = {}
    for item in choices:
        athletes[item] = get_athletes_by_country(db, item)
        
    s = ''
    for (key, values) in athletes.items():
        s += "\n" + str(key) + "\n\n"
        for name in values:
            s += name[0] + "\n"
    
    msg = "Countries and their athletes:"
    title = "Country Data"
    write_to_textbox(msg, title, s)
    
    return 'menu'

def medal_winners(fcns_dict, db, param_list):
    
    
    sport_list = get_sports(db)
    
    
    # sport = enterbox('Enter a sport:', 'Medals Awarded')
    sport = choicebox('Select a sport:', 'Sport Selection', sport_list)
    winners = get_medal_winners_by_sport(db, sport)
    
    # create string to print
    s = 'Athlete\t Country\t Event\t Medal\n'

    for sublist in winners:
        for item in sublist:
            s += item + "\t"
        s += "\n"
        
    msg = "Medal winners for " + sport + ":"    
    write_to_textbox(msg, "Medal Winners", s)
    return 'menu'




def get_sports(db):
    
    L = run_query(db, '''SELECT DISTINCT Sport FROM Sports''')
    sports = []
    for sublist in L:
        sports.append(str(sublist[0]))
    return sports 
    

if __name__ == '__main__':

     # DO NOT CHANGE

    # database name
    db = 'Olympics.db'
    
    # Get files for Athlete table
    athlete_file = open('athletelist.txt', 'r')
    athlete_list = athlete_file.read().strip().split(',')
    athlete_file.close()
    setup_athlete(db, athlete_list)
    
    # Get files for Sports table
    sport_file = open('sportlist.txt', 'r')
    sport_list = sport_file.read().strip().split(',')
    sport_file.close()
    setup_sports(db, sport_list)

    # END OF DO NOT CHANGE
           
    fcns_dict = {'menu':menu, 'athlete':athlete_lookup, 'country':country_reps, \
                 'medal':medal_winners, 'quit':quit}
    
    choice = menu(fcns_dict, db, [])

    while 1:
        if choice:
            func = fcns_dict[choice]
        choice = func(fcns_dict, db, [])
        
    
    
    
