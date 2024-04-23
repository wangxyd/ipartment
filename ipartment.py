# encoding:utf-8

import re
import random

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *

@plugins.register(
    name="iPartment",
    desire_priority=88,
    hidden=True,
    desc="爱情公寓剧本专享插件。",
    version="1.2",
    author="空心菜",
)
class iPartment(Plugin):
    def __init__(self):
        super().__init__()
        try:
            # 加载配置
            conf = super().load_config()
            if not conf:
                raise Exception("[iPartment] config.json not found")
            # 优化引用消息
            self.reply_reference_query = conf.get('reply_reference_query', False)
            if self.reply_reference_query:
                logger.info("[iPartment] reply_reference_query is on.")
            else:
                logger.info("[iPartment] reply_reference_query is off.")
            # 识别对方身份
            self.add_quoter_nickname = conf.get('add_quoter_nickname', False)
            if self.add_quoter_nickname:
                logger.info("[iPartment] add_quoter_nickname is on.")
            else:
                logger.info("[iPartment] add_quoter_nickname is off.")
            if self.add_quoter_nickname or self.reply_reference_query:
                self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            # 群聊中机器人回复消息时@对方的概率
            self.group_at_probability = conf.get('group_at_probability', 1)
            if self.group_at_probability < 1:
                self.handlers[Event.ON_DECORATE_REPLY] = self.on_decorate_reply
                logger.info("[iPartment] group_at_probability is on.")
            else:
                logger.info("[iPartment] group_at_probability is off because of group_at_probability>=1.")
            logger.info("[iPartment] inited")
        except Exception as e:
            logger.warn("[iPartment] init failed, ignore.")
            raise e

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [ContextType.TEXT]:
            return
        content = e_context["context"].content
        logger.debug("[iPartment] on_handle_context. content: %s" % content)
        try:
            # 优化引用消息
            if self.reply_reference_query and "」\n- - - - - - -" in content:
                content = re.sub(r'」\n(- ){6,}-', '」\n前面「」中的内容是引用的消息，新的问题是：', content)
                logger.debug(f"[iPartment] reference query have been modified.")
            # 识别对方身份，并在提示词开头添加”xxx对你说：“
            # if self.add_quoter_nickname and e_context["context"].get("isgroup", False):
            if self.add_quoter_nickname:
                actual_user_nickname = e_context["context"]["msg"].actual_user_nickname or e_context["context"]["msg"].other_user_nickname
                add_prefix = f"{actual_user_nickname}对你说："
                # 确保修改操作的幂等性
                if not content.startswith(add_prefix):
                    content = add_prefix + content
                    logger.debug(f"[iPartment] {add_prefix} have been added.")
            if e_context["context"].content != content:
                e_context["context"].content = content
        except Exception as e:
            logger.warn(f"[iPartment] error occurred: {e}.")

    def on_decorate_reply(self, e_context: EventContext):
        if e_context["reply"].type != ReplyType.TEXT:
            return
        logger.debug("[iPartment] on_decorate_reply.")
        # 设置群聊中机器人回复消息时@对方的概率
        try:
            need_at = True if random.random() < self.group_at_probability else False
            if not need_at:
                e_context["context"]["no_need_at"] = True
            logger.debug(f"[iPartment] no_need_at is {not need_at}.")
        except Exception as e:
            logger.warn(f"[iPartment] error occurred: {e}.")

    def get_help_text(self, **kwargs):
        return "爱情公寓剧本专享插件。"
