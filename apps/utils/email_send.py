#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File    : email_send.py
# @author  : Jaxon
# @software: PyCharm
# @datetime: 10/27 027 上午 10:58
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def generate_random_str(random_length=10):
    random_str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        random_str += chars[random.randint(0, length)]
    return random_str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    random_str = generate_random_str(20)
    email_record.code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title, email_body = "", ""
    if send_type == "register":
        email_title, email_body = (
            u"慕学在线网注册激活链接",
            u"请将链接复制到浏览器访问以便激活你的账号完成注册：http://127.0.0.1:8000/active/{0}".format(random_str)
        )
        send_count = 0
        while send_count < 3:
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
            if send_status:
                break
            send_count += 1

    elif send_type == "forget":
        email_title, email_body = (
            u"慕学在线网密码重置链接",
            u"请将链接复制到浏览器访问以便重置你的账号密码：http://127.0.0.1:8000/reset/{0}".format(random_str)
        )
        send_count = 0
        while send_count < 3:
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
            if send_status:
                break
            send_count += 1
