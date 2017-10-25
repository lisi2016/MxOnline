#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : adminx.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/25 025 下午 03:34

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['id', 'name', 'desc', 'add_time']
    search_fields = ['id', 'name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['id', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['id', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'address']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city__name', 'add_time']


class TeacherAdmin(object):
    list_display = ['id', 'name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                    'fav_nums', 'add_time']
    search_fields = ['id', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['name', 'org__name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                   'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
