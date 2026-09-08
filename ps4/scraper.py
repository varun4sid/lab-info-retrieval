import csv
import requests
from bs4 import BeautifulSoup

winners_list_url = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

session = requests.Session()
session.headers.update({'User-Agent': user_agent})

winners_list_response = session.get(winners_list_url)
winners_list_soup = BeautifulSoup(winners_list_response.text, 'lxml')
    
winners_table = winners_list_soup.find('table', {'class': 'wikitable'})
winners_table_rows = winners_table.find_all('tr')
headers = [header.text.strip() for header in winners_table_rows[0].find_all('th')]

data = []
years = len(winners_table_rows[1:-2])
for index, row in enumerate(winners_table_rows[1:-2]):
    print(f"Processing row {index + 1}/{years}")
    year = row.find('th').text.strip()
    for subject, cell in enumerate(row.find_all('td')):
        anchor = cell.find('a')
        if anchor:
            record = [anchor.text.strip(), headers[subject], year, anchor['href']]
            data.append(record)
            
print(f"Total records extracted: {len(data)}")
            
for index, row in enumerate(data):
    row[-1] = str(row[-1]).replace('https://en.wikipedia.org/wiki/', '/wiki/')
    row.insert(0,index+1)
    
with open('nobel_laureates.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Index', 'Name', 'Category', 'Year', 'Link'])
    writer.writerows(data)
    
file.close()