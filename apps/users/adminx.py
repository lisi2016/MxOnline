#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : adminx.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/25 025 下午 12:07

import xadmin

from .models import EmailVerifyRecord, Banner


class EmailVerifyRecordAdmin(object):
    """
    list_display：设置默认显示列
    search_fields：设置搜索字段（若设置了时间日期字段，则搜索时带中文会报错）
    list_filter：添加过滤器（解决没有时间搜索问题）

    """
    list_display = ['id', 'code', 'email', 'send_type', 'send_time']
    search_fields = ['id', 'code', 'email', 'send_type']
    list_filter = ['id', 'code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['id', 'title', 'image', 'url', 'index', 'add_time']
    search_fields = ['id', 'title', 'image', 'url', 'index']
    list_filter = ['id', 'title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
