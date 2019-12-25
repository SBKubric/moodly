import vk
from bs4 import BeautifulSoup
from pathlib import Path
import local_settings
from collections import defaultdict
import json
import selenium


def get_link_2_account(vk_id):
    return 'https://vk.com/{}'.format(vk_id)


def get_audio_link(html):
    bs = BeautifulSoup(html, 'lxml')
    elem_list = bs.find_all('div', 'audios_module')
    for elem in elem_list:
        if elem.attrs['id'] == 'profile_audios':
            a = elem.find('a', 'module_header')
            return a.attrs['href']


def parse_audio_page(html, vk_id):
    songs = defaultdict(list)
    bs = BeautifulSoup(html, 'lxml')
    elem_list = bs.find_all('div', 'audio_row_content')
    for elem in elem_list:
        artist = elem.find('a', 'artist_link').text
        title = elem.find('span', 'audio_row__title_inner').text
        songs[artist].append(title)
    return {'user': vk_id, 'songs': songs}


def get_personal_page(vk_id):
    with open('./acc2_page.html', encoding='windows-1251') as html:
        return html.read()


def get_audio_page(vk_id):
    return ''


def write_songs_to_file(path, songs):
    with open(path, mode='w') as file:
        json.dump(songs, file)


def main():
    # html = get_audio_page('id1234')
    # songs_dict = parse_audio_page(html)
    # print(songs_dict)
    html = get_personal_page('test')
    link = get_audio_link(html)
    print(link)


if __name__ == '__main__':
    main()
