#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : urls.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 11/15 015 上午 10:42
from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, VideoPlayView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),  # 课程列表
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),  # 课程详情
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),  # 课程章节
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comment"),  # 课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_comment"),  # 添加课程评论
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),  # 视频播放页
]
