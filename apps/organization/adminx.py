#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : adminx.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/25 025 下午 03:34

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['id', 'name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-map-marker'


class CourseOrgAdmin(object):
    """
    ordering：排序
    readonly_fields：设置字段只读
    relfield_style：在其它表中的外键以ajax方式加载
    list_editable：列表页支持编辑
    """
    list_display = ['name', 'desc', 'tag', 'click_nums', 'fav_nums', 'students', 'course_nums', 'image',
                    'address', 'city', 'add_time']
    search_fields = ['id', 'name', 'desc', 'tag', 'click_nums', 'fav_nums', 'image', 'address']
    list_filter = ['name', 'desc', 'tag', 'click_nums', 'fav_nums', 'image', 'address', 'city__name', 'add_time']
    model_icon = 'fa fa-university'
    ordering = ['-click_nums']
    readonly_fields = ['students', 'course_nums', 'click_nums', 'fav_nums']
    relfield_style = 'fk-ajax'
    list_editable = ['desc', 'tag']
    style_fields = {'detail': 'ueditor'}


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                    'fav_nums', 'add_time']
    search_fields = ['id', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['name', 'org__name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                   'fav_nums', 'add_time']
    model_icon = 'fa fa-graduation-cap'
    readonly_fields = ['click_nums', 'fav_nums']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
