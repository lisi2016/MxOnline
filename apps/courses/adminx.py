#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : adminx.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/25 025 下午 02:39

import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['id', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time']
    search_fields = ['id', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time']


class LessonAdmin(object):
    """
    course__name：通过双下划线方式表示course表的name字段
    """
    list_display = ['id', 'name', 'course', 'add_time']
    search_fields = ['id', 'name']
    list_filter = ['name', 'course__name', 'add_time']


class VideoAdmin(object):
    list_display = ['id', 'name', 'lesson', 'add_time']
    search_fields = ['id', 'name']
    list_filter = ['name', 'lesson__name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['id', 'name', 'course', 'download', 'add_time']
    search_fields = ['id', 'name', 'download']
    list_filter = ['name', 'course__name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
