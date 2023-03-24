from app.api import search, add

def route(app):
    # 设置路由
    app.add_url_rule('/atom/search', view_func=search.search, methods=['POST'])
    app.add_url_rule('/atom/add/pic', view_func=add.add_pic, methods=['POST'])
    app.add_url_rule('/atom/add/dir', view_func=add.add_dir, methods=['POST'])