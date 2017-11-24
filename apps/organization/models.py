# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市名称")
    desc = models.CharField(max_length=200, verbose_name=u"城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    detail = UEditorField(verbose_name=u"机构描述", width=600, height=300, imagePath="organizations/ueditor/",
                          filePath="organizations/ueditor/", default="")
    category = models.CharField(max_length=10, choices=(("pxjg", u"培训机构"), ("gr", u"个人"), ("gx", u"高校")),
                                default="pxjg", verbose_name=u"机构类别")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    image = models.ImageField(upload_to="organization/%Y/%m", verbose_name=u"封面图")
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    tag = models.CharField(default='', max_length=10, verbose_name=u"机构标签")
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        # 统计教师数量
        return self.teacher_set.all().count()

    def get_classic_course(self):
        # 取经典课程
        return self.course_set.all().order_by('-students')[:2]

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名称")
    work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"工作职位")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    age = models.IntegerField(default=18, verbose_name=u"年龄")
    image = models.ImageField(default='', upload_to="teacher/%Y/%m", verbose_name=u"头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        return self.course_set.all().count()

    def get_hot_course(self):
        # 取招牌课程
        return self.course_set.all().order_by('-students')[:1]

    def __unicode__(self):
        return self.name
