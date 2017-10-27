#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : forms.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/26 026 下午 02:20
from django import forms

from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    """
    用户注册表单
    """
    email = forms.EmailField(required=True, max_length=30)
    password = forms.CharField(required=True, min_length=6, max_length=20)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误。"})


class LoginForm(forms.Form):
    """
    用户登录表单
    """
    username = forms.CharField(required=True, max_length=30)
    password = forms.CharField(required=True, min_length=6, max_length=20)


class ForgetForm(forms.Form):
    """
    找回密码表单
    """
    email = forms.EmailField(required=True, max_length=30)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误。"})


class ModifyPwdForm(forms.Form):
    """
    重置密码表单
    """
    password1 = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)