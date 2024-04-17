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
  "add_quoter_nickname": true,
  "reply_reference_query": true
}
```

在以上配置项中：

- `group_at_probability`: 群聊中回复消息时at对方的概率。取值范围0~1，0每次都不@对方，1每次都@对方；
- `add_quoter_nickname`: 是否在群聊中开启识别对方身份的功能。值为`true`时会将对方的微信昵称添加到对话内容中，然后CoW会使用`xxx对你说：原来的对话内容`向后端模型发起查询请求，以便模型识别对方的身份；
- `reply_reference_query`: 是否回复包含引用的消息。CoW默认忽略引用的消息，值为`true`时会将对话内容中引用消息的标记"」\n- - - - - - -"修改为"前面「」中的内容是引用的消息，新的问题是："，然后CoW会响应引用的信息。

如果您有任何更好的想法或建议，都非常欢迎您积极提出哦~~~