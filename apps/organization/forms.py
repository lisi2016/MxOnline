#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : forms.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/30 030 下午 04:53
from django import forms
import re

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    """
    授课机构-我要学习（用户咨询）
    """

    class Meta:
        model = UserAsk  # 指定模型
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码合法性
        :return:
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        raise forms.ValidationError(u"手机号码非法。", code="mobile_invalid")
