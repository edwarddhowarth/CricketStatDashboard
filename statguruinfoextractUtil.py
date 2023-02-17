from bs4 import BeautifulSoup
from urllib.request import urlopen

# with open("F:\Programming Project Misc\warner.html") as fp:
#     soup = BeautifulSoup(fp, 'html.parser')

soup = BeautifulSoup(open("F:\Programming Project Misc\statguruinfo.html"), 'html.parser')

names = soup.find('select', 'name=team')


#seperate by select tag into a list
def extract_select_tags():
    select_tags = []
    for row in soup.find_all('select'):
        select_tags.append(row)
    return select_tags

myList = extract_select_tags()



#remove html tags from a list of text
def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

cleanList = []
for text in myList:
    #append the text to a list
    cleanList.append(remove_html_tags(str(text)))


len(cleanList)

for text in cleanList:
    print(text)