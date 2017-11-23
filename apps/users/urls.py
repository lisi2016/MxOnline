#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : urls.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 11/21 021 下午 02:32
from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCaptchaView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),  # 个人信息
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),  # 头像上传
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),  # 修改密码(个人中心)
    url(r'^send_captcha/$', SendEmailCaptchaView.as_view(), name="send_captcha"),  # 发送邮箱验证码
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),  # 修改邮箱
    url(r'^my_course/$', MyCourseView.as_view(), name="my_course"),  # 我的课程（个人中心）
    url(r'^my_fav/org/$', MyFavOrgView.as_view(), name="my_fav_org"),  # 我收藏的机构（个人中心）
    url(r'^my_fav/teacher/$', MyFavTeacherView.as_view(), name="my_fav_teacher"),  # 我收藏的讲师（个人中心）
    url(r'^my_fav/course/$', MyFavCourseView.as_view(), name="my_fav_course"),  # 我收藏的课程（个人中心）
    url(r'^my_message/$', MyMessageView.as_view(), name="my_message"),  # 我的消息（个人中心）
]
