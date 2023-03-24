from flask import Flask, Response, request, send_file
import os
import json

'''
    一个简易的http文件服务器，仅供该项目内部使用，
    目录结构由调用者通过参数传递。
    若后续高并发导致性能问题，可以考虑用其他语言实现，
    但不要直接使用成熟软件代替，因为后续可能有加密需求，
    必须在文件服务器内部做加密，保证落盘的数据是加密后的。
'''

# 资源文件夹位置
resource_dir = "resource"
host = "0.0.0.0"
port = 8001

app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <html>
            <body>
                <h1>文件服务器</h1>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <span>文件夹位置(dataset/dir):</span>
                    <input type="text" name="dir">
                    <input type="submit" value="上传">
                </form>
            </body>
        </html>
    '''


@app.route('/upload', methods=['POST'])
def upload():
    '''
        返回的url字段不是可以直接下载使用的url，而是文件的相对路径。

        考虑到文件服务器可能被nginx代理，或添加https，因此实际的url
        由调用者自行拼接。
    '''
    file = request.files['file']
    filename = file.filename
    dir = request.form['dir']
    dir = os.path.join(resource_dir, dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    filename = os.path.join(dir, filename)
    print("save to:", filename)
    file.save(filename)
    return Response(json.dumps({"url": filename}), status=200, mimetype='application/json')


@app.route('/download/<path:filename>')
def download(filename):
    print(f'download: {filename}')
    return send_file(filename)


if __name__ == '__main__':
    app.run(host=host, port=port, debug=False)
