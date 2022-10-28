from flask import Blueprint, render_template

main_page_blueprint = Blueprint('main_page_blueprint', __name__, template_folder='templates')


@main_page_blueprint.route('/')
def main_page():
    return render_template("index.html")
