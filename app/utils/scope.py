
'''
    权限管理
    添加图片以及用户管理等仅管理员有权限调用
    普通用户仅可以搜索，以及反馈搜索结果好坏
'''

class Scope:
    allow_api = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))
        return self


class AdminScope(Scope):
    allow_api = ['add_pic', 'add_dir']

    def __init__(self):
        self + UserScope()


class UserScope(Scope):
    allow_api = ['search']


scope_map = {"UserScope": UserScope(), "AdminScope":AdminScope()}


def is_in_scope(scope:str, endpoint:str) -> bool:
    print(f'-----------scope: {scope} endpoint: {endpoint}')
    scope = scope_map[scope]
    if endpoint not in scope.allow_api:
        return False
    return True