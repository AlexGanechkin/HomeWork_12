import logging
from flask import Flask, request, render_template, send_from_directory
from functions import *

POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"

logger = logging.getLogger()
file_handler = logging.FileHandler("log.txt")
logger.addHandler(file_handler)

from main_page.views import main_page_blueprint
from add_page.views import loader_blueprint

# from search_page.views import search_page_blueprint

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(main_page_blueprint)
app.register_blueprint(loader_blueprint)

# app.register_blueprint(search_page_blueprint)

@app.route('/search')
def search_page():
    """
    Осуществляем поиск постов по фразе, введенной пользователем, - через functions.search_posts
    На выходе формируем страницу со списком постов, либо сообщение, что не найдено
    """

    user_request = request.args['s']
    found_posts = search_posts(user_request)
    number = len(found_posts)
    return render_template('post_list.html', user_request=user_request, number=number, found_posts=found_posts)


@app.route("/post_uploaded", methods=["GET", "POST"])
def page_post_form():
    """
    Создаем новый пост, проверяем на наличие текста и картинки, расширение картинки.
    Если текст, файл отсутствуют или расширение не соответствует установленным, формируем сообщение польщзователю
    """

    allowed_extentions = {'png', 'jpg'}
    content = request.values.get('content')

    if not content:
        return render_template('load_error.html', error=2)
    picture = request.files.get('picture')

    if picture:
        filename = picture.filename
        extension = filename.split(".")[-1]

        if extension in allowed_extentions:
            picture.save(f"./uploads/images/{filename}")
            pic = "./" + UPLOAD_FOLDER + "/" + filename
            add_post(pic, content)
            return render_template('post_uploaded.html', pic=pic, content=content)
        else:
            logger.info(f"Файл не загружен: неправильное расширение файла {filename}")
            return render_template('load_error.html', error=1)

    else:
        logger.error("Ошибка при загрузке файла")
        return render_template('load_error.html', error=3)


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


if __name__ == "__main__":
    app.run()
