# Qi
Version: 1.0

我校强智教务系统课表转 ics 日历文件

Copyright (c) 2020-2021 0xJacky


## 说明
1. Qi 支持手动维护的放假、补课安排，配置信息在 `qi-server/holiday.py` 欢迎通过提交 PR 补充假期安排
2. 学号及密码仅用于请求教务系统
3. ics 文件导入 iOS 日历，请将 ics 通过邮件发送到 iOS 设备上，通过系统自带的邮件 App 可以直接将日历导入，建议在导入前新建一个新的日历分区
4. macOS 用户可以直接导入 ics 文件
5. 获取日历相关捷径前往 https://jackyu.cn/projects/qi
6. 项目在线地址 https://qi.jackyu.cn

## 补课
1. 2020年国庆及中秋节放假、补课安排
2. 2021年元旦、清明放假安排

## 依赖
```
pip3 install -r qi-server/requirements.txt
```

## CLI 模式使用方法
1. 进入 `qi-server`
2. 复制一份 `config-default.ini` 为 `config.ini`
3. 进入 `config.ini` 配置教务系统学号及密码
4. 执行 `python3 cli.py -c` 即可生成本学期课表
5. 执行 `python3 cli.py -e` 即可生成考试安排


## Docker 前后端模式使用方法
1. 获取镜像
```
docker pull uozi/qi
```
2. 启动镜像
```
docker run -d --restart=always -p 5001:80 uozi/qi:latest
```
3. 反向代理

在 nginx 中添加反向代理配置块
```
location / {
	proxy_pass         http://127.0.0.1:5001/;
	proxy_redirect     off;

	proxy_set_header   Host                 $host;
	proxy_set_header   X-Real-IP            $remote_addr;
	proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
	proxy_set_header   X-Forwarded-Proto    $scheme;
}
```

4. 访问域名即可进入前端

## LICENSE
MIT
