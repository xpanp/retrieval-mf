# Retrieval-mf API

图像检索系统API文档。

## 用户管理

### 注册

使用邮箱注册账号，只可注册普通用户账户。管理员账户系统默认创建。

**method** 

post

**url**

`/user/register`

**请求参数**

参数类型：form

| 参数名称 | 参数类型 | 是否必填 | 参数描述                  |
| :------- | :------- | :------- | :------------------------ |
| account  | string   | 是       | 邮箱地址                  |
| passwd   | string   | 是       | 密码                      |
| nickname | string   | 是       | 名称                      |
| type     | int      | 是       | 默认100，表示通过邮箱注册 |

**请求参数示例**

![img](pic/register.png)

**返回数据**

数据类型：json

| 数据名称 | 数据类型 | 是否必填 | 数据描述                             |
| -------- | -------- | -------- | ------------------------------------ |
| code     | int      | 是       | 自定义状态码，0为正常                |
| msg      | string   | 是       | 信息，正常返回`ok`，异常返回错误信息 |

**返回数据示例**

```json
{
    "code": 0,
    "msg": "ok"
}
```

### 登录

使用邮箱登录，返回token。

业务相关接口必须在请求头中增加`Authorization`字段，值为该接口返回的`token`，否则会调用失败。如：`Authorization:eyJhbGci……`。

**method** 

post

**url**

`/user/login`

**请求参数**

参数类型：form

| 参数名称 | 参数类型 | 是否必填 | 参数描述                  |
| :------- | :------- | :------- | :------------------------ |
| account  | string   | 是       | 邮箱地址                  |
| passwd   | string   | 是       | 密码                      |
| type     | int      | 是       | 默认100，表示通过邮箱登录 |

**请求参数示例**

![img](pic/login.png)

**返回数据**

json

| 数据名称 | 数据类型 | 是否必填 | 数据描述               |
| -------- | -------- | -------- | ---------------------- |
| code     | int      | 是       | 自定义状态码，0为正常  |
| msg      | string   | 是       | 信息，异常返回错误信息 |
| data     | object   | 否       | 具体数据               |
| token    | string   | 是       | 授权信息               |

**返回数据示例**

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjIsInNjb3BlIjoiVXNlclNjb3BlIiwidGltZSI6MTY4MTk5MDQzMSwiZXhwIjoxNjgyMDc2ODMxfQ.NPMn-jMDbG4uYLgkRLF-hi-IXUW_sEnCn1VTTKkfN2Q"
    }
}
```

## 图像检索

### 增加一张图片

仅管理员可操作！

通过form表单上传一张图片，将其加入到数据库中。

**method** 

post

**url**

`/api/add_pic`

**请求参数**

form

| 参数名称 | 参数类型 | 是否必填 | 参数描述 |
| :------- | :------- | :------- | :------- |
| file     | File     | 是       | 图片文件 |

**请求参数示例**

![img](pic/add_pic.png)

**返回数据**

json

| 数据名称 | 数据类型 | 是否必填 | 数据描述               |
| -------- | -------- | -------- | ---------------------- |
| code     | int      | 是       | 自定义状态码，0为正常  |
| msg      | string   | 是       | 信息，异常返回错误信息 |

**返回数据示例**

```json
{
    "code": 0,
    "msg": "add_pic success"
}
```

### 批量添加图片

仅管理员可操作！

需要提前将待处理的图片文件夹放到系统可以直接访问到的位置，如共享文件夹或直接放在系统所在机器上。

通过该接口可以批量处理文件夹中的图片，将其加入数据库中。

需要注意由于文件夹可能非常大，因此该接口会直接返回成功，然后在后台慢慢处理。

**method** 

post

**url**

`/api/add_dir`

**请求参数**

form

| 参数名称 | 参数类型 | 是否必填 | 参数描述   |
| :------- | :------- | :------- | :--------- |
| dir      | string   | 是       | 文件夹地址 |

**请求参数示例**

![img](pic/add_dir.png)

**返回数据**

json

| 数据名称  | 数据类型 | 是否必填 | 数据描述                           |
| --------- | -------- | -------- | ---------------------------------- |
| code      | int      | 是       | 自定义状态码，0为正常              |
| msg       | string   | 是       | 信息，异常返回错误信息             |
| data      | object   | 否       | 具体数据                           |
| taskid    | string   | 是       | 任务号，后续可通过该任务号查看进度 |
| task_nums | int      | 是       | 文件夹中的图片数量                 |

**返回数据示例**

```json
{
    "code": 0,
    "msg": "add_dir start process",
    "data": {
        "taskid": "task-1681991139840",
        "task_nums": 102
    }
}
```

### 查看批量任务状态

批量添加图片接口在后台进行，其任务状态可由该接口查看。

**method** 

post

**url**

`/api/add_dir/status`

**请求参数**

form

| 参数名称 | 参数类型 | 是否必填 | 参数描述 |
| :------- | :------- | :------- | :------- |
| taskid   | string   | 是       | 任务号   |

**请求参数示例**

![img](pic/add_dir_status.png)

**返回数据**

json

| 数据名称       | 数据类型 | 是否必填 | 数据描述               |
| -------------- | -------- | -------- | ---------------------- |
| code           | int      | 是       | 自定义状态码，0为正常  |
| msg            | string   | 是       | 信息，异常返回错误信息 |
| data           | object   | 否       | 具体数据               |
| taskid         | string   | 是       | 任务号                 |
| processed_nums | int      | 是       | 当前已经完成的任务数量 |
| task_nums      | int      | 是       | 总任务数               |

**返回数据示例**

Note: 若`processed_nums`与`task_nums`相等，则表示该任务已经完成。

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "taskid": "task-1684051220872",
        "processed_nums": 8,
        "task_nums": 102
    }
}
```

### 检索

上传一张图片，指定需要使用的特征提取算法，返回最为相似的图片列表。

**method** 

post

**url**

`/api/search`

**请求参数**

form

| 参数名称   | 参数类型 | 是否必填 | 参数描述                                     |
| :--------- | :------- | :------- | :------------------------------------------- |
| algo       | string   | 是       | 算法，可选：`fusion|vit|vgg|color|lbp|color` |
| result_num | int      | 是       | 返回结果数量                                 |
| file       | File     | 是       | 图片文件                                     |
| x_min      | int      | 否       | 截取框的左上角x坐标                          |
| y_min      | int      | 否       | 截取框的左上角y坐标                          |
| x_max      | int      | 否       | 截取框的右下角x坐标                          |
| y_max      | int      | 否       | 截取框的右下角y坐标                          |

**请求参数示例**

![img](pic/search.png)

**返回数据**

json

| 数据名称           | 数据类型 | 是否必填 | 数据描述                           |
| ------------------ | -------- | -------- | ---------------------------------- |
| code               | int      | 是       | 自定义状态码，0为正常              |
| msg                | string   | 是       | 信息，异常返回错误信息             |
| data               | object   | 否       | 具体数据                           |
| taskid             | string   | 是       | 任务号，后续可通过该任务号反馈结果 |
| compare_mode       | string   | 是       | 比对算法                           |
| result             | array    | 是       | 结果数组                           |
| id                 | int      | 是       | 图片id号                           |
| score              | float    | 是       | 比对得分                           |
| filename           | string   | 是       | 文件名                             |
| filepath           | string   | 是       | http文件路径                       |
| filepath_thumbnail | string   | 是       | 缩略图http文件路径                 |

**返回数据示例**

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "taskid": "task-1681991558583",
        "compare_mode": "cosine",
        "result": [
            {
                "id": 156,
                "score": 0.9274682998657227,
                "filename": "000007.jpg",
                "filepath": "http://10.199.130.173:8001/download/resource/rmf_image200/000007.jpg",
                "filepath_thumbnail": "http://10.199.130.173:8001/download/resource/rmf_image200/000007.jpg"
            },
            {
                "id": 187,
                "score": 0.6655550003051758,
                "filename": "000159.jpg",
                "filepath": "http://10.199.130.173:8001/download/resource/rmf_image200/000159.jpg",
                "filepath_thumbnail": "http://10.199.130.173:8001/download/resource/rmf_image200/000159.jpg"
            },
			……
        ]
    }
}
```

### 结果反馈

若使用特征融合算法进行图像检索，可以指定较为满意的结果或者不满意的结果，反馈给系统调整融合参数。

**method** 

post

**url**

`/api/feedback`

**请求参数**

form

| 参数名称  | 参数类型 | 是否必填 | 参数描述          |
| :-------- | :------- | :------- | :---------------- |
| taskid    | string   | 是       | 检索任务号        |
| pictureid | int      | 是       | 图片id号          |
| type      | int      | 是       | 0：Bad \| 1：Good |

**请求参数示例**

![img](pic/feedback.png)

**返回数据**

json

| 数据名称 | 数据类型 | 是否必填 | 数据描述               |
| -------- | -------- | -------- | ---------------------- |
| code     | int      | 是       | 自定义状态码，0为正常  |
| msg      | string   | 是       | 信息，异常返回错误信息 |

**返回数据示例**

```json
{
    "code": 0,
    "msg": "ok"
}
```



