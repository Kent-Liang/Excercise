from sqlite3 import dbapi2 as sqlite
from easygui import *
from sys import exit

def run_query(db, query, args=None):
    '''Return the results of running the given query on database db.'''
    
    con = sqlite.connect(db)
    cur =  con.cursor()
    if args == None:
        cur.execute(query)
    else:
        cur.execute(query, args)
    data = cur.fetchall()
    cur.close()
    con.close()
    return data

def setup_athlete(db, filename_list):
    '''Create and populate the Athlete table for database db using the
    contents of the file named filename.'''

    con = sqlite.connect(db)
    cur = con.cursor()
    

    cur.execute('Drop table if exists Athlete ')
    cur.execute('CREATE TABLE Athlete(Country VARCHAR(20), Name VARCHAR(40), Gender VARCHAR(10), Age INT(3), Sport VARCHAR(15),Gold INT(3), Silver INT(3), Bronze INT(3), Total INT(5))')
    
    for filename in filename_list:
        data_file = open(filename, 'r')
        country = filename.split('.')[0]
        print(country)
        
        line = data_file.readline()
        line = data_file.readline()
        while line != '':
            data = line.split(',')
            for i in [5, 6, 7, 8]:
                if data[i].strip() == '':
                    data[i] = 0
            cur.execute('''INSERT INTO Athlete VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',\
                        (country, data[1].strip(), data[2].strip(), 
                         int(data[3].strip()), data[4].strip(),
                         int(data[5]), int(data[6]),
                         int(data[7]), int(data[8])))   
            line = data_file.readline()
        
        data_file.close()
    
    cur.close()
    con.commit() 
    con.close()

def setup_sports(db, filename_list):
    '''Create and populate the Sports table for database db using the
     contents of the file named filename.'''

    con = sqlite.connect(db)
    cur = con.cursor()
    cur.execute('Drop table if exists Sports ')
    cur.execute('CREATE TABLE Sports(Sport VARCHAR(20), Event VARCHAR(20), Gold VARCHAR(20), Silver VARCHAR(20), Bronze VATCHAR(20))')
    
    for filename in filename_list:
        data_file = open(filename)
        sport = filename.split('.')[0]

        line = data_file.readline()
        line = data_file.readline()
  
        while line.strip() != '':
            data = line.split(',')
            cur.execute('''INSERT INTO Sports VALUES(?, ?, ?, ?, ?)''',\
                    (sport, data[0].strip(), data[1].strip(), \
                     data[2].strip(), data[3].strip()))   
            
            line = data_file.readline()
        
        data_file.close()

    cur.close()
    con.commit()
    con.close()
    
def get_athlete_totals(dbname):
    return run_query(dbname,'''SELECT NAME,TOTAL FROM Athlete''')
    

def get_athletes_by_country(dbname, country):
    return run_query(dbname,'''SELECT Name FROM Athlete WHERE Country = ?''',(country,))
    

def is_valid_name(dbname, name):
    return (run_query(dbname,'''SELECT * FROM Athlete WHERE Name = ?''',(name,)) != [])
    
         
def get_medal_winners_by_sport(dbname="Olympics.db", sport="Alpine Skiing"):
    result = []
    medal = ["Gold", "Silver", "Bronze"]
    db_result = run_query(dbname,'''SELECT * FROM Sports WHERE sport=?''',(sport,))
    for element in db_result:
        for i in range(3):
            country = get_athelete_country(dbname, element[i+2])
            #Percautionary step for country not found. Since the data set are 
            #small, country not on the should be found 
            if country == []:
                country = ""
            else:
                country = country[0][0]
            
            #For team sport like relay    
            if (element[i+2].upper(),) in get_countries(dbname):
                result.append(["", element[i+2], element[1], medal[i]])
            else:
                result.append([element[i+2], country, element[1], medal[i]])
    return result

def get_athelete_country(dbname, athelete):
    return run_query(dbname,'''SELECT Country FROM Athlete WHERE Name= ?''',(athelete,))

def get_event_won(dbname="Olympics.db", athlete="Bode Miller"):
    sport = run_query(dbname,'''SELECT Sport FROM Athlete WHERE Name = ?''',(athlete,))
    if sport != []:
        sport = sport[0][0]
    else:
        return []
    result = []
    winners = get_medal_winners_by_sport(dbname, sport)
    for element in winners:
        if athlete in element:
            result.append([sport, element[2], element[3]])
    return result                      
            
def get_avg_age_by_sport(dbname):
    return run_query(dbname,'''SELECT AVG(Age),sport FROM Athlete''' )
    
    
def get_same_country_winners(dbname):
    return run_query(dbname,'''SELECT a.Name, b.Name FROM Athlete As a, Athlete As b WHERE a.Name != b.Name AND a.Country = b.Country''' )
     
def get_countries(dbname):
    return run_query(dbname,'''SELECT DISTINCT Country FROM Athlete''')   


def get_sports(db):
    
    L = run_query(db, '''SELECT DISTINCT Sport FROM Sports''')
    sports = []
    for sublist in L:
        sports.append(str(sublist[0]))
    return sports 


# GUI functions DO NOT TOUCH THIS CODE


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

    fcns_dict = {'menu':menu, 'athlete':athlete_lookup, 'country':country_reps, \
                 'medal':medal_winners, 'quit':quit}
    
    choice = menu(fcns_dict, db, [])

    while 1:
        if choice:
            func = fcns_dict[choice]
        choice = func(fcns_dict, db, [])
        
    # END OF DO NOT CHANGE



