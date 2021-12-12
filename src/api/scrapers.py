import os
import requests
from bs4 import BeautifulSoup

def clean_text(text):
    for spaced in ['.', ' ', ',', '!', '?', '(', '—', ')', '|']:
        text = text.replace(spaced, '-')
    return text

def get_press_releases(page=0):
    if page == 0: add_page = ''
    else: add_page = f'page/{page}/'

    main_sauce = requests.get(f'https://www.whitehouse.gov/briefing-room/speeches-remarks/{add_page}')
    main_soup = BeautifulSoup(main_sauce.text, 'html.parser')

    h2_tags = main_soup.find_all('h2')

    press_release_links = []
    for h2 in h2_tags:
        if h2.a is None: continue
        press_release_link = h2.a.get('href')
        press_release_links.append(press_release_link)

    for link in press_release_links:
        sub_sauce = requests.get(link)
        sub_soup = BeautifulSoup(sub_sauce.text, 'html.parser')

        title_tag = sub_soup.find('title')
        title = clean_text(title_tag.text)

        p_tags = sub_soup.find_all('p')

        dir = 'data'
        filename = f'speech_{title}.txt'
        filename = os.path.join(dir, filename)

        with open(filename, 'w+') as f:
            for p in p_tags:
                paragraph = p.text
                if 'THE VICE PRESIDENT: ' in paragraph: paragraph = paragraph.replace('THE VICE PRESIDENT: ', '')
                if 'THE PRESIDENT: ' in paragraph: paragraph = paragraph.replace('THE PRESIDENT: ', '')
                f.write(paragraph)
