#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : adminx.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/25 025 下午 02:39

import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInLine(object):
    model = Lesson
    extra = 0


class CourseResourceInLine(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    """
    inlines：支持相关联信息编辑
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time',
                    'get_zj_nums']
    search_fields = ['id', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time']
    model_icon = 'fa fa-pencil-square'
    readonly_fields = ['click_nums', 'fav_nums']
    ordering = ['-click_nums']
    inlines = [LessonInLine, CourseResourceInLine]
    style_fields = {'detail': 'ueditor'}

    # 过滤显示数据
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 保存课程时统计课程数
    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    """
    inlines：支持相关联信息编辑
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time']
    search_fields = ['id', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time']
    model_icon = 'fa fa-pencil-square'
    readonly_fields = ['click_nums', 'fav_nums']
    ordering = ['-click_nums']
    inlines = [LessonInLine, CourseResourceInLine]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    """
    course__name：通过双下划线方式表示course表的name字段
    """
    list_display = ['name', 'course', 'add_time']
    search_fields = ['id', 'name']
    list_filter = ['name', 'course__name', 'add_time']
    model_icon = 'fa fa-tasks'


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['id', 'name']
    list_filter = ['name', 'lesson__name', 'add_time']
    model_icon = 'fa fa-video-camera'


class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'download', 'add_time']
    search_fields = ['id', 'name', 'download']
    list_filter = ['name', 'course__name', 'download', 'add_time']
    model_icon = 'fa fa-cubes'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
