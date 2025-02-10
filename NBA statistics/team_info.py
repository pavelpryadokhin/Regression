# информация о каждой команде. домашний стадион и состав команды.
from test import web, located
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time

url = 'https://www.flashscorekz.com/basketball/usa/nba/standings/#/nRrQOhwm/table/overall'
browser = web()

browser.set_page_load_timeout(11)

Xpath_table = '//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div[2]/div/div[2]'
Xpath_table_teams = '//*[@id="overall-all-table"]/div[1]'
Xpath_info = '//*[@id="mc"]/div[6]/div[1]/div[2]/div[2]'
selector_table = '#tournament-table-tabs-and-content > div:nth-child(3)'

try:
    browser.get(url)
    located(browser, Xpath_table)

    generated_html = browser.page_source

    soup = BeautifulSoup(generated_html, 'html5lib')
    teams_member = soup.select_one(selector_table)
finally:
    pass

tables = teams_member.find_all('div', class_='tableWrapper')

print('пошли по ссылкам ходить')
list_uri = []
for table in tables[:2]:
    table_body = table.find('div', class_='ui-table__body')
    for row in table_body.find_all('div', class_='ui-table__row'):
        href = row.find('a')['href']
        list_uri.append(href)

team_info = dict()

for uri in list_uri:
    list_team = []
    uri = 'https://www.flashscorekz.com' + uri

    browser.get(uri)
    located(browser, Xpath_info)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html5lib')
    team = soup.find('div', class_='heading')
    team_title = team.find('div', class_='heading__name').text.strip()
    stadion = team.find('span', class_='heading__info--key').next_sibling.strip()
    team_info[team_title] = [stadion]

    uri += 'squad/'
    browser.get(uri)
    located(browser, Xpath_table_teams)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html5lib')
    teams_member = soup.find_all('div', class_='lineupTable__row')
    for team in teams_member:
        list_team.append(team.find('a', class_='lineupTable__cell--name').text.strip())
    team_info[team_title].append(list_team)

    print(team_info)

print(team_info)
