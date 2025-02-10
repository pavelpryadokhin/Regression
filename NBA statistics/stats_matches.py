# подробная статистика в матче
import statistics
from data import team_info
from test import web, located
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from collections import defaultdict
import time
from tqdm import tqdm

Xpath_lineups = '//*[@id="detail"]/div[10]/div[1]/div[2]/div'
Xpath_stadion = '//*[@id="detail"]/section/div[5]/div/div[2]/div/div[2]/strong'
Xpath_stadion24 = '//*[@id="detail"]/section/div[6]/div/div[2]/div/div[4]/strong'
Xpath_stadion24_1 = '//*[@id="detail"]/section/div[5]/div/div[2]/div/div[4]/strong'
Xpath_table = '//*[@id="detail"]/div[8]/div[2]/div[3]'
Xpath_date = '//*[@id="detail"]/div[4]/div[1]/div'
Xpath_stats = '//*[@id="detail"]'
load_more_xpath1 = '//*[@id="detail"]/div[8]/div[2]/div[1]/div[3]'
load_more_xpath2 = '//*[@id="detail"]/div[8]/div[2]/div[2]/div[3]'
load_more_xpath3 = '//*[@id="detail"]/div[8]/div[2]/div[3]/div[3]'
extracted_matches = []

with open('all_matches_2425.txt', 'r', encoding='utf-8') as file:  # Открытие файла в режиме чтения
    for line in file:
        if line.strip():  # Проверяем, что строка не пустая
            href, text_content = line.split(': ', 1)  # Разделяем строку по первому ':'
            text_content = text_content.strip().split(', ')  # Убираем пробелы и делим на части
            extracted_matches.append((href, text_content))  # Сохраняем в виде кортежа

browser = web()


# [[игрок 1 к1, игрок 2 к1, .. игрок 5 к1]], [игрок 1 к2.....]]
def lineups(uri):
    uri += '/lineups'
    try:
        browser.get(uri)
        located(browser, Xpath_lineups)
        time.sleep(0.5)
        generated_html = browser.page_source
    except:
        return [], []

    soup = BeautifulSoup(generated_html, 'html5lib')
    sides = soup.find('div', class_='lf__sides')
    players = []
    try:
        for side in sides:
            players.append([player.get_text().strip() for player in side.find_all('strong')])
        return players
    except:
        print(iteration, 'lineups')
        return [], []


# ['имя стадион','data']
def match_stadion(uri):
    uri += '/match-summary'
    try:
        browser.get(uri)
        try:
            located(browser, Xpath_stadion24)
            element = browser.find_element(By.XPATH, Xpath_stadion24).text
        except:
            located(browser, Xpath_stadion24_1)
            element = browser.find_element(By.XPATH, Xpath_stadion24_1).text
        date = browser.find_element(By.XPATH, Xpath_date).text.split()[0]
        return [element, date]
    except:
        print(iteration, 'match_stadion')
        return [], []


# {команда1:[{дата,в/п,результат},...],команда2:[...],H2H:[дата,результат]}
# def match_summary(uri):
#     uri = uri[:-13] + 'h2h/overall'
#     try:
#         browser.get(uri)
#         located(browser, Xpath_table)
#         el1 = located(browser, load_more_xpath1)
#         browser.execute_script("arguments[0].click();", el1)
#         el2 = located(browser, load_more_xpath2)
#         browser.execute_script("arguments[0].click();", el2)
#         el3 = located(browser, load_more_xpath3)
#         browser.execute_script("arguments[0].click();", el3)
#         generated_html = browser.page_source
#     except:
#         return
#
#     tables = BeautifulSoup(generated_html, 'html5lib')
#     tables = tables.find('div', class_='h2h').find_all('div', class_='h2h__section section')
#     statics = dict()
#     firstcomand = None
#     for table in tables[:2]:
#         name = table.find('div', class_='section__title').get_text().split("Последние игры: ")[-1].strip()
#         statics[name] = list()
#         firstcomand = name if not firstcomand else firstcomand
#         for row in table.find_all('div', class_='h2h__row'):
#             stat = dict()
#             stat['date'] = row.find('span', class_='h2h__date').text.strip()
#             stat['win_loss'] = row.find('span', class_='h2h__icon').find('div').get('title')
#             result_index = row.find_all('span', class_=['h2h__participantInner winner', 'h2h__participantInner'])
#             result_index = [span.get_text(strip=True) for span in result_index]
#             try:
#                 index = result_index.index(name)
#                 result = row.find('span', class_='h2h__result')
#                 stat['result'] = [int(span.get_text(strip=True)) for span in result.find_all('span')][index]
#             except ValueError:
#                 stat['result'] = None
#             statics[name].append(stat)
#     statics['H2H'] = []
#     for table in tables[2:]:
#         for row in table.find_all('div', class_='h2h__row'):
#             stat = dict()
#             stat['date'] = row.find('span', class_='h2h__date').text.strip()
#             result_index = row.find_all('span', class_=['h2h__participantInner winner', 'h2h__participantInner'])
#             result_index = [span.get_text(strip=True) for span in result_index]
#             index = result_index.index(firstcomand)
#             result = row.find('span', class_='h2h__result')
#             result_match = [int(span.get_text(strip=True)) for span in result.find_all('span')]
#             if index == 0:
#                 stat['result'] = result_match
#             else:
#                 stat['result'] = result_match[::-1]
#             statics['H2H'].append(stat)
#     return statics


def edition_stats(uri):
    uri += '/match-statistics/0'
    try:
        browser.get(uri)
        located(browser, Xpath_stats)
        generated_html = browser.page_source
    except:
        print(iteration, 'edition_stats')
        return {}

    soup = BeautifulSoup(generated_html, 'html5lib')
    sections = soup.find_all('div', class_='section')
    dict_stats = defaultdict(dict)
    for section in sections:
        sub_sections = section.find_all('div', class_="wcl-row_OFViZ")
        for info in sub_sections:
            data = [side.get_text().strip() for side in info.find_all('strong')]
            dict_stats[0][data[1]] = float(data[0].split('%')[0])
            dict_stats[1][data[1]] = float(data[2].split('%')[0])
    return dict_stats


filename = 'teams_170.txt'


def contin(filename):
    teams = defaultdict(list)

    with open(filename, 'r') as f:
        current_team = None
        for line in f:
            line = line.strip()  # Убираем пробелы и символы новой строки
            if line.startswith('Итерация:'):
                iteration = line.split(': ')[1]  # Извлечение номера итерации
                print(f'Итерация: {iteration}')
            elif line.startswith('Team:'):
                current_team = line.split(': ')[1]  # Извлечение имени команды
            elif current_team and line:  # Если это строка с данными команды
                # Парсинг информации о команде
                team_info = eval(line)  # Используйте eval только если уверены в безопасности данных!
                teams[current_team].append(team_info)
    return teams, int(iteration)


url_test = 'https://www.flashscorekz.com/match/MmGLHUG8/#/match-summary'

teams, count = contin(filename)
# teams, count = defaultdict(list), 0
print(count)



for iteration, (uri, tx) in tqdm(enumerate(extracted_matches[count:], start=count)):
    team_1 = {'count': int(tx[2]), 'opponent': tx[1], 'win': int(tx[2]) >= int(tx[3])}
    team_2 = {'count': int(tx[3]), 'opponent': tx[0], 'win': int(tx[2]) < int(tx[3])}
    team_1['players'], team_2['players'] = lineups(uri)
    stadion, date = match_stadion(uri)
    if not stadion:
        time.sleep(0.5)
        stadion, date = match_stadion(uri)
    team_1['home'] = team_info[tx[0]][0] == stadion
    team_2['home'] = team_info[tx[1]][0] == stadion
    team_1['date'] = team_2['date'] = date
    edition_info = edition_stats(uri)
    if not edition_info:
        time.sleep(0.5)
        edition_info = edition_stats(uri)
    team_1.update(edition_info[0])
    team_2.update(edition_info[1])
    teams[tx[0]].append(team_1)
    teams[tx[1]].append(team_2)
    # Сохранение каждые 10 итераций
    if (iteration + 1) % 10 == 0:
        with open(f'teams_{iteration + 1}.txt', 'w') as f:
            f.write(f'Итерация: {iteration + 1}\n')
            for team, values in teams.items():
                f.write(f'Team: {team}\n')
                for value in values:
                    f.write(f'  {value}\n')

# Сохранение  данных
with open(f'teams_new_2425.txt', 'w') as f:
    f.write(f'Итерация: {len(extracted_matches)}\n')
    for team, values in teams.items():
        f.write(f'Team: {team}\n')
        for value in values:
            f.write(f'  {value}\n')
print(teams)
