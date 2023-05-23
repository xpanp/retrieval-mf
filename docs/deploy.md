# Retrieval-mf 部署文档

部署文档细节

## MySQL

建议使用`docker`安装启动，也可自行从官网安装并启动。

确保安装好`docker`环境后，使用`docker`安装`mysql`:

```shell
docker pull mysql:latest
```

启动mysql：

```shell
docker run --restart=always -itd --name mysql-test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```

其中`MYSQL_ROOT_PASSWORD`指定密码，建议设复杂一点。

## Milvus

使用`docker-compose`启动，具体见：[Install Milvus Standalone with Docker Compose Milvus documentation](https://milvus.io/docs/install_standalone-docker.md)

首先确保安装好`docker-compose`环境，然后下载`yaml`配置文件，该项目中已包含配置文件[docker-compose.yml](../docker-compose.yml)。

在有`yaml`配置文件的目录中启动`milvus`：

```shell
sudo docker-compose up -d
```

## Python

要求：`python >= 3.9 torch>=1.10.1`

从官网下载安装[anaconda]([Free Download | Anaconda](https://www.anaconda.com/download/))或[miniconda]([Miniconda — conda documentation](https://docs.conda.io/en/latest/miniconda.html))，安装好conda环境后，创建python虚拟环境。

在本项目文件夹中执行安装依赖：

```shell
# 安装依赖项
pip install -r requirements
```

## Fileserver

项目中实现了一个简单的HTTP文件服务器，在`utils/file_server.py`，进入`utils`文件夹后启动：

```shell
python file_server.py
```

## Server

指定配置文件启动图像检索系统

```shell
python server.py -c conf/conf.ini
```

**Note**:在新机器上第一次启动时会联网下载vgg与vit模型文件，离线时可以直接将模型拷贝到对应目录中

```shell
ls ~/.cache/torch/hub/checkpoints
jx_vit_base_p16_224-80ecf9dd.pth vgg16-397923af.pth
```

## 前端部署

使用`npm run build`将前端程序打包以后，将`dist`文件夹放在服务器上，使用nginx代理该文件夹。

ubuntu安装nginx：

```shell
sudo apt install nginx
```

新增配置文件：

```shell
sudo vim /etc/nginx/conf.d/rmf.conf
```

具体配置如下：

```nginx
server {
    	# 设置具体需要监听的端口，通常为80
        listen 8003;
        listen [::]:8003;
		
    	# 服务器ip地址
        server_name 10.199.130.173;

    	# 代理页面
        location / {
        		# 具体的dist文件夹地址
                root /home/phs/program/python/retrieval-mf/tmp/dist;
        		# 设置首页
                index index.html;
                # 解决vue刷新404问题
                try_files $uri $uri/ /index.html;
        }
    
    	# 代理请求，转发到后端程序
        location /api/ {
                proxy_pass http://10.199.130.173:8000;
        }
}
```

nginx相关命令

```shell
# 测试配置文件是否正确
sudo nginx -t
# 重新启动nginx
sudo nginx -s reload
```

## 其他相关说明

### 配置文件

```ini
[server]
# 监听地址
HOST = 0.0.0.0
# 监听端口
PORT = 8000
# 算法引擎数，根据机器性能配置
NUM_WORKER = 1
# cpu -1, others gpuid
CUDA_VISIBLE_DEVICES = -1
DEBUG = False
# 临时文件存放目录
TMP_DIR = tmp
# 需要指定文件服务器地址，必须配置成Fileserver程序所在机器的ip地址，否则页面可能无法展示图片
FILE_SERVER_URL = http://10.199.130.173:8001/

[engine]
ALGO_RESIZE = 248
ALGO_WIDTH = 224
ALGO_HEIGHT = 224
VGG_AVG_SIZE = 7
VGG_MODEL = vgg16
VIT_MODEL = vit_base_patch16_224
VIT_EXTRACT_AVG = False

[compare]
# 比对方式，包括milvus与cosine两种算法
# 若数据较少，可以使用cosine方式启动，则不依赖milvus数据库
CMP_MODE = milvus
# 同步模式，若开启，则删除现有milvus库，使用mysql中的数据重新建milvus库
# 如之前使用cosine方法启动，后续需要改用milvus数据库，则将该选项配置为True
# 更详细细节见代码部分
SYNC_MILVUS = False

[db]
# mysql数据库相关配置
DB_HOST = 127.0.0.1
DB_PORT = 3306
DB_USER = root
DB_PASSWD = 123456
DB_NAME = rmf

[milvus]
MILVUS_HOST = 127.0.0.1
MILVUS_PORT = 19530
```

### 默认账户

管理员用户：`admin@qq.com`

管理员密码：`nimdappp`

**Note**：仅管理员用户可以建立特征库，普通用户仅可以进行搜索。普通用户需自行注册，注册时要求使用正常邮箱名。