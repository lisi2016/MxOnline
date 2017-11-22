#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : urls.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 11/21 021 下午 02:32
from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCaptchaView, UpdateEmailView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),  # 个人信息
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),  # 头像上传
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),  # 修改密码(个人中心)
    url(r'^send_captcha/$', SendEmailCaptchaView.as_view(), name="send_captcha"),  # 发送邮箱验证码
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),  # 修改邮箱
]
