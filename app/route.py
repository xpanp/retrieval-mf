from app.api import search, add, user

def route(app):
    # 设置路由
    app.add_url_rule('/api/search', view_func=search.search, methods=['POST'])
    app.add_url_rule('/api/add_pic', view_func=add.add_pic, methods=['POST'])
    app.add_url_rule('/api/add_dir', view_func=add.add_dir, methods=['POST'])

    app.add_url_rule('/user/register', view_func=user.register, methods=['POST'])
    app.add_url_rule('/user/login', view_func=user.login, methods=['POST'])