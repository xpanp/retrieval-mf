from app.api import search, add, user

def route(app):
    # 设置路由
    app.add_url_rule('/api/search', view_func=search.search, methods=['POST'])
    app.add_url_rule('/api/feedback', view_func=search.feedback, methods=['POST'])
    app.add_url_rule('/api/add_pic', view_func=add.add_pic, methods=['POST'])
    app.add_url_rule('/api/add_dir', view_func=add.add_dir, methods=['POST'])
    app.add_url_rule('/api/add_dir/status', view_func=add.get_status, methods=['POST'])

    app.add_url_rule('/api/user/register', view_func=user.register, methods=['POST'])
    app.add_url_rule('/api/user/login', view_func=user.login, methods=['POST'])