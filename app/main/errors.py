from flask import render_template
from . import main
#页面未发现
@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',hide_right=True),400

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html',hide_right=True),500
