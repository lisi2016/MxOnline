#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : mixin_utils.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 11/18 018 下午 03:13
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    登录验证函数
    """

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
