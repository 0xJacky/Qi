# Qi

SZTU 强智教务系统课表转 ics 日历文件

Copyright (c) 2020-2021 0xJacky


## 说明
1. Qi 支持手动维护的放假、补课安排，配置信息在 `holiday.py` 目前支持2020年国庆及中秋节放假、补课安排，欢迎通过提交 PR 补充假期安排
2. 学号及密码仅用于请求教务系统
3. ics 文件导入 iOS 日历，请将 ics 通过邮件发送到 iOS 设备上，通过系统自带的邮件 App 可以直接将日历导入，建议在导入前新建一个新的日历分区
4. macOS 用户可以直接导入 ics 文件
5. 获取日历相关捷径前往 https://jackyu.cn/projects/qi

## 依赖
```
pip3 install beautifulsoup4 requests
```

## 使用方法
1. 复制一份 `config-default.ini` 为 `config.ini`
2. 进入 `config.ini` 配置教务系统学号及密码
3. 执行 `python3 main.py` 即可生成本学期课表

## LICENSE
MIT
