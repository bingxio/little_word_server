### 如何使用它 ?

![](https://github.com/Turaiiao/little_word_server/blob/master/201811022203331.png)

[ENGLISH](https://github.com/Turaiiao/little_word_server/blob/master/README.md)

一个简单的 python3 tornado RESTFUL API 服务，你可以将它部署到你的服务器上

你可以保存一些优美的句子到你的数据库，然后用 API 接口随机加载

- 编辑 secret.conf 文件配置你的 MongoDB 服务器
- 在你的服务器上配置 python3
- 安装 install-script-doc.txt 里的模块
- 添加一些数据到你的数据库
- 使用你的服务器 IP + 6264 端口进行访问

### 关于数据库表

像这样去配置它，更多请查看 **app.py**

![](https://github.com/Turaiiao/little_word_server/blob/master/20181102224119.png)

#### GET
```
IP:6264/
```

#### POST
必须携带 content、author 字段值进行 POST，否则会报错 400 error server
```
IP:6264/
```

##### Welcome Star, Fork, Issues!

### License
```
Copyright 2018 Turaiiao

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
