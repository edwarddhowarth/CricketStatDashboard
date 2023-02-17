from bs4 import BeautifulSoup
from urllib.request import urlopen

with open(".\warner.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

#soup = BeautifulSoup(urlopen("https://stats.espncricinfo.com/ci/engine/player/219889.html?class=1;orderby=start;orderbyad=reverse;template=results;type=batting;view=innings"), 'html.parser')


#extract table tags with the engineTable class and put them into a list
def extract_tables_as_string():
    table_list = []
    for row in soup.find_all('table', 'engineTable'):
        table_list.append(str(row))
    return table_list

tables = soup.find_all('table', 'engineTable')
#print(tables[2].get_text())

#extract the thead tag from the table
def extract_table_headers():
    table_headers = []
    for row in soup.find_all('table', 'engineTable'):
        table_headers.append(row.thead)
    return table_headers

#extract the tbody from the table
def extract_table_body():
    table_body = []
    for row in soup.find_all('table', 'engineTable'):
        table_body.append(row.tbody)
    return table_body


heads = extract_table_headers()
bodys = extract_table_body()

#print(heads[2])
#print(heads[3])

#remove html tags from text
# def remove_html_tags(text):
#     """Remove html tags from a string"""
#     import re
#     clean = re.compile('<.*?>')
#     return re.sub(clean, '', text)

# # print(len(remove_html_tags(str(heads[3]))))
# # print(len(remove_html_tags(str(bodys[3]))))

# #open file called heads.txt and write the table headers to it
# with open('F:\Programming Project Misc\heads.txt', 'w') as f:
#     f.write(remove_html_tags(str(heads[3])))

# with open('F:\Programming Project Misc\\bodys.txt', 'w') as f:
#     f.write(remove_html_tags(str(bodys[3])))


#create object that stores batting innings by innings list values
class BattingInnings:
    def __init__(self, runs, mins, balls, fours, sixes, strike_rate, pos, dismissal, innings, opponent, ground, start_date, test_number):
        self.runs = runs
        self.mins = mins
        self.balls = balls
        self.fours = fours
        self.sixes = sixes
        self.strike_rate = strike_rate
        self.pos = pos
        self.dismissal = dismissal
        self.innings = innings
        self.opponent = opponent
        self.ground = ground
        self.start_date = start_date
        self.test_number = test_number

    #print each class member on a new line with their name
    def __str__(self):
        return "Runs: {}\nMins: {}\nBalls: {}\nFours: {}\nSixes: {}\nStrike Rate: {}\nPosition: {}\nDismissal: {}\nInnings: {}\nOpponent: {}\nGround: {}\nStart Date: {}\nTest Number: {}".format(self.runs, self.mins, self.balls, self.fours, self.sixes, self.strike_rate, self.pos, self.dismissal, self.innings, self.opponent, self.ground, self.start_date, self.test_number)

#remove asterix from string if it exists
def remove_asterix(string):
    if string[-1] == '*':
        return string[:-1]
    else:
        return string
    
#replace DNB with 0
def replace_DNB(string):
    if string == "DNB":
        return "0"
    else:
        return string
    
def numerise_runs(string):
    return replace_DNB(remove_asterix(string))

#store bodys values in a list of BattingInnings
def store_batting_innings():
    batting_innings_list = []
    for row in bodys[3].find_all('tr'):
        batting_innings_list.append(BattingInnings(
            numerise_runs(row.find_all('td')[0].get_text()), 
            row.find_all('td')[1].get_text(), 
            row.find_all('td')[2].get_text(), 
            row.find_all('td')[3].get_text(), 
            row.find_all('td')[4].get_text(), 
            row.find_all('td')[5].get_text(), 
            row.find_all('td')[6].get_text(), 
            row.find_all('td')[7].get_text(), 
            row.find_all('td')[8].get_text(), 
            row.find_all('td')[10].get_text(), 
            Ground(row.find_all('td')[11].get_text(),
            remove_non_numeric(row.find_all('td')[11].find('a').get('href'))), 
            row.find_all('td')[12].get_text(),
            row.find_all('td')[13].get_text()))
    return batting_innings_list

#class to store name and id of the ground
class Ground:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __str__(self):
        return "Name: {}\nID: {}".format(self.name, self.id)

#extract the ground id's and name from each of the innings and store them in a list of Ground objects
def extract_grounds():
    grounds = []
    for row in bodys[3].find_all('tr'):
        grounds.append(Ground(
            row.find_all('td')[11].get_text(),
            row.find_all('td')[11].find('a').get('href')))
    return grounds

#extract the numeric ground id from the href tag and remove alpha characters
def extract_ground_id():
    ground_id = []
    for row in bodys[3].find_all('tr'):
        ground_id.append(row.find_all('td')[11].find('a').get('href')[-5:])
    return ground_id

#remove non numeric characters from any string
def remove_non_numeric(string):
    return ''.join(i for i in string if i.isdigit())


def extract_ground_ids():
    ground_ids = []
    for row in bodys[3].find_all('tr'):
        ground_ids.append(row.find_all('td')[11].find('a').get('href'))
    return ground_ids



#print(bodys[3].find_all('tr'))

player_innings = store_batting_innings()

print(len(player_innings))
print(player_innings[0].__str__() + "\n")


avg = 0
out = 0
i = 0
while i < 50:
    print(player_innings[i].runs)
    avg = avg + int(player_innings[i].runs)
    if(player_innings[i].dismissal != "not out"):
        out = out + 1
    i = i + 1

print("\nLast " + str(i-1) + " Match average: " + str((avg-200)/(out-1)) + "\n")

print("\nLast " + str(i) + " Match average: " + str(avg/out) + "\n")
