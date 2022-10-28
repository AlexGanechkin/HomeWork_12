from flask import Blueprint, render_template

search_page_blueprint = Blueprint('search_page_blueprint', __name__, template_folder='templates')


@search_page_blueprint.route('/search')
def search_page():
    return render_template("index.html")
