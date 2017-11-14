#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : urls.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/30 030 下午 05:13
from django.conf.urls import url, include

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),  # 授课机构列表
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),  # 授课机构用户咨询
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),  # 授课机构机构首页
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),  # 授课机构机构课程
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),  # 授课机构机构介绍
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),  # 授课机构机构讲师
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),  # 授课机构机构收藏
]
