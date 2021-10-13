import sys
import os
import collections
import requests
from bs4 import BeautifulSoup
from colorama import Fore

args = sys.argv
history = collections.deque()
search_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']


if args[1]:
    if os.access(f'.\\{args[1]}', os.F_OK):
        pass
    else:
        os.mkdir(f'.\\{args[1]}')
    filepath = f'.\\{args[1]}'
else:
    filepath = os.getcwd()

command = input()
while command != 'exit':
    if os.access(f'{filepath}\\{command}', os.F_OK):
        site = requests.get(command)
        site = site.text
        print(site)
        filename = command[8:command.rfind('.')]
        history.append(filename)
        f = open(f'{filepath}\\{filename}', 'w', encoding='utf-8')
        f.write(site)
        f.close()
    elif command == 'back':
        if not history:
            pass
        else:
            history.pop()
            last_page = history.pop()
            f = open(f'{filepath}\\{last_page}', 'r', encoding='utf-8')
            for line in f:
                print(line)
            f.close()
    elif '.' not in command:
        print('Incorrect URL')
    else:
        if 'https://' not in command:
            command = 'https://' + command
        filename = command[8:command.rfind('.')]
        history.append(filename)
        f = open(f'{filepath}\\{filename}', 'w', encoding='utf-8')
        site = requests.get(command)
        soup = BeautifulSoup(site.content, 'html.parser')
        for tag in search_tags:
            if tag == 'a':
                addition = Fore.BLUE
            else:
                addition = ''
            tag_finds = soup.find_all(tag)
            for tag2 in tag_finds:
                print(addition + tag2.text)
                f.write(addition + tag2.text)
        f.close()
    command = input()
