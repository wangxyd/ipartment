## 插件描述

爱情公寓专享插件，用于回复消息时取消(随机)at对方，以及识别对方的身份。

## 安装方法

```sh
#installp https://github.com/wangxyd/ipartment.git
#scanp
```

## 配置步骤

1. 配置文件为`config.json`，可以自行修改，示例如下：

```json
{
  "group_at_probability": 0,
  "add_quoter_nickname": true
}
```

在以上配置项中：

- `group_at_probability`: 群聊中回复消息时at对方的概率。取值范围0~1，0每次都不@对方，1每次都@对方；
- `add_quoter_nickname`: 是否在群聊中开启识别对方身份的功能。值为`true`时会将对方的微信昵称添加到对话内容中，然后COW会使用`xxx对你说：原来的对话内容`向后端模型发起查询请求，以便模型识别到对方的身份。