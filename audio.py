import vk
from bs4 import BeautifulSoup
from pathlib import Path
import local_settings
from collections import defaultdict
from json import j


def parse_audio_page(html, vk_id):
    songs = defaultdict(list)
    bs = BeautifulSoup(html, 'lxml')
    elem_list = bs.find_all('div', 'audio_row_content')
    for elem in elem_list:
        artist = elem.find('a', 'artist_link').text
        title = elem.find('span', 'audio_row__title_inner').text
        songs[artist].append(title)
    return {'user': vk_id, 'songs': songs}


def get_audio_page(vk_id):
    html = ''
    yield html


def main():
    html = get_audio_page('id1234')

    songs_dict = parse_audio_page(page_path)
    print(songs_dict)


if __name__ == '__main__':
    main()
