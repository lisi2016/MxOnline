#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : adminx.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/25 025 下午 03:54

import xadmin

from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ['id', 'name', 'mobile', 'course_name', 'add_time']
    search_fields = ['id', 'name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['id', 'user', 'course', 'comments', 'add_time']
    search_fields = ['id', 'user', 'course', 'comments']
    list_filter = ['user__username', 'course__name', 'comments', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['id', 'user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['id', 'user', 'fav_id', 'fav_type']
    list_filter = ['user__username', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['id', 'user', 'message', 'has_read', 'add_time']
    search_fields = ['id', 'user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['id', 'user', 'course', 'add_time']
    search_fields = ['id', 'user', 'course']
    list_filter = ['user__username', 'course__name', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)