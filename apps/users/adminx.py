#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : adminx.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/25 025 下午 12:07

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    """
    后台主题配置
    """
    enable_themes = False  # 开启主题功能，True为开启
    use_bootswatch = True  # 支持更多主题，True为开启


class GlobalSettings(object):
    site_title = u"慕学后台管理系统"  # 页面左上角标识及页面title
    site_footer = u"慕学在线网"  # 页面底部的标识
    menu_style = "accordion"  # 设置左侧菜单可折叠


class EmailVerifyRecordAdmin(object):
    """
    list_display：设置默认显示列
    search_fields：设置搜索字段（若设置了时间日期字段，则搜索时带中文会报错）
    list_filter：添加过滤器（解决没有时间搜索问题）

    """
    list_display = ['id', 'code', 'email', 'send_type', 'send_time']
    search_fields = ['id', 'code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['id', 'title', 'image', 'url', 'index', 'add_time']
    search_fields = ['id', 'title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# 进行注册
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
