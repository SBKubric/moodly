import vk_api
import re

import local_settings

stop_words = ['суицид']


def search_url(text):
    for word in text.split():
        if 'id' in word:
            id = re.search(r'\d+', word)
            return id.group()
    return False


def search_stop_word(text):
    for word in stop_words:
        if word in text:
            url = search_url(text)
            if url:
                return (word, url)
            else:
                return False
    return False


def vk_auth(login, password):
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    return vk


def vk_group_search(vk, query):
    '''Поиск групп по заданой строке'''
    response = vk.groups.search(q=query, offset=0, count=50)
    print(response['count'])
    for item in response['items']:
        print(f'{item["id"]} - {item["name"]}')


def vk_wall_search(vk, owner_id):
    '''Поиск по стене'''
    response = vk.wall.get(owner_id=owner_id, offset=0, count=1)
    wall_size = int(response['count'])
    result = []
    for index in range(0, wall_size, 100):
        response = vk.wall.get(
            owner_id=owner_id, offset=index, count=index + 100)
        for item in response['items']:
            temp = search_stop_word(item.get('text').lower())
            if temp:
                result.append(temp)
        print('{} - {}'.format(index, len(result)))
    with open('unchecked_pages.txt', 'w', encoding='utf-8') as f:
        f.write('Количество: {}\n'.format(len(result)))
        for item in result:
            f.write(f'{item[0]} - {item[1]}\n')


def check_pages(vk):
    result = []
    with open('unchecked_pages.txt', 'r', encoding='utf-8') as f:
        for line in f:
            result.append(line.split()[-1])
    checked_result = []
    for index in range(1, len(result), 50):
        user_ids = ','.join(result[index:index + 50])
        response = vk.users.get(user_ids=user_ids)
        for user in response:
            if user.get('can_access_closed'):
                checked_result.append(user['id'])

    with open('checked_pages.txt', 'w', encoding='utf-8') as f:
        f.write('Количество: {}\n'.format(len(checked_result)))
        for item in checked_result:
            f.write(f'{item}\n')


def create_subscriptions_list(vk):
    user_ids = []
    with open('checked_pages.txt', 'r', encoding='utf-8') as f:
        for line in f:
            user_ids.append(line)
    subscriptions_users = []
    subscriptions_groups = []
    i = 0
    for id in user_ids[1:]:
        result = vk.users.getSubscriptions(user_id=int(id), fields='name')
        subscriptions_users.extend(result['users']['items'])
        subscriptions_groups.extend(result['groups']['items'])
        i += 1
        if i % 10 == 0:
            print(i)
    with open('subscriptions_users.csv', 'w', encoding='utf-8') as f:
        f.write('user\n')
        for user in subscriptions_users:
            f.write(f'{user}\n')
    with open('subscriptions_groups.csv', 'w', encoding='utf-8') as f:
        f.write('group\n')
        for group in subscriptions_groups:
            f.write(f'{group}\n')


if __name__ == '__main__':
    vk = vk_auth(local_settings.login, local_settings.password)
    groups = vk_group_search(vk, 'Дэд пейдж')
    vk_wall_search(vk, -125339469)
    check_pages(vk)
    create_subscriptions_list(vk)
