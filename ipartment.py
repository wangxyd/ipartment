# encoding:utf-8

import json
import os
import random

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *
from config import global_config

@plugins.register(
    name="iPartment",
    desire_priority=88,
    hidden=True,
    desc="爱情公寓专享插件。",
    version="1.0",
    author="空心菜",
)
class iPartment(Plugin):
    def __init__(self):
        super().__init__()
        try:
            # load config
            conf = super().load_config()
            if not conf:
                raise Exception("[iPartment] config.json not found")
            self.group_at_probability = conf.get('group_at_probability', 1)
            self.add_quoter_nickname = conf.get('add_quoter_nickname', False)
            if self.group_at_probability < 1:
                self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
                logger.info("[iPartment] group_at_probability is on.")
            else:
                logger.info("[iPartment] group_at_probability is off because of group_at_probability>=1.")
            if self.add_quoter_nickname:
                self.handlers[Event.ON_DECORATE_REPLY] = self.on_decorate_reply
                logger.info("[iPartment] add_quoter_nickname is on.")
            else:
                logger.info("[iPartment] add_quoter_nickname is off.")
            logger.info("[iPartment] inited")
        except Exception as e:
            logger.warn("[iPartment] init failed, ignore.")
            raise e

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [ContextType.TEXT]:
            return
        content = e_context["context"].content
        logger.debug("[iPartment] on_handle_context. content: %s" % content)
        # 群聊中识别对方身份，并在提示词开头添加”xxx对你说：“
        if self.add_quoter_nickname and e_context["context"].get("isgroup", False):
            actual_user_nickname = e_context["context"]["msg"].actual_user_nickname
            add_prefix = f"{actual_user_nickname}对你说："
            content = add_prefix + content
            logger.debug(f"[iPartment] {add_prefix} have been added.")
        if e_context["context"].content != content:
            e_context["context"].content = content

    def on_decorate_reply(self, e_context: EventContext):
        if e_context["reply"].type != ReplyType.TEXT:
            return
        logger.debug("[iPartment] on_decorate_reply.")
        # 回复消息时随机at
        try:
            need_at = True if random.random() < self.group_at_probability else False
            if not need_at:
                e_context["context"]["no_need_at"] = True
            logger.debug(f"[iPartment] no_need_at is {not need_at}.")
        except Exception as e:
            logger.debug(f"[iPartment] error occurred: {e}.")

    def get_help_text(self, **kwargs):
        return "爱情公寓专享插件。"
