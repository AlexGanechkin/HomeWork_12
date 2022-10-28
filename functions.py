import json
import logging

logging.basicConfig(filename="log.txt")


def load_posts():
    """
    Загружаем список постов из файла
    Входящие данные: нет
    Исходящие данные: список постов (картинка + словарь)
    """

    try:
        with open('posts.json', 'r', encoding='utf-8') as file:
            posts = json.load(file)
    except FileNotFoundError:
        logging.error("файл post.json отсутствует. Передан пустой список для сохранения работоспособности")
        posts = [{'pic': '', 'content': ''}]
    return posts


def search_posts(search_request):
    """
    Ищем посты содержащие набор символов, полученный от пользователя
    Входящие данные: search_request - запрос пользователя
    Исходящие данные: список постов содержащий запрос пользователя
    """

    found_posts = []
    posts = load_posts()
    for post in posts:
        if search_request.lower() in post['content'].lower():
            found_posts.append(post)
    logging.info(f"Выполнен поисковый запрос пользователя, найдено {len(found_posts)} постов")
    return found_posts


def add_post(pic, content):
    """
    Добавляем в список постов новый пост
    Входящие данные: pic, content - файл с картинкой и текст, полученные от пользователя
    Исходящие данные: список постов, дополненный новым постом и сохраненный в виде файла post.json
    """

    posts = load_posts()
    posts.append({'pic': pic, 'content': content})
    with open('posts.json', 'w', encoding='utf-8') as file:
        json.dump(posts, file, ensure_ascii=False)
    return
