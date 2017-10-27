# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    """
    重写登录验证逻辑
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 交集用'|'，并集用','
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    """
    用户激活
    """

    def get(self, request, active_code):
        email_record = EmailVerifyRecord.objects.filter(code=active_code)
        if email_record:
            for record in email_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, "login.html")
        return render(request, "active_fail.html")


class ResetView(View):
    """
    找回密码
    """

    def get(self, request, reset_code):
        email_record = EmailVerifyRecord.objects.filter(code=reset_code)
        if email_record:
            for record in email_record:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
            return render(request, "login.html")
        return render(request, "active_fail.html")


class ModifyPwdView(View):
    """
    修改密码
    """
    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        email = request.POST.get("email", "")
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": u"两次输入的密码不一致。"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        return render(request, "password_reset.html",
                      {"email": email, "modify_pwd_form": modify_pwd_form, "msg": u"请修正上面的错误。"})


# Create your views here.
class RegisterView(View):
    """
    用户注册视图
    """

    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": u"邮箱已经被注册。"})

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        return render(request, "register.html", {"register_form": register_form, "msg": u"请修正上面的错误。"})


class LoginView(View):
    """
    用户登录视图
    """

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)  # 用户和密码通过则返回modle对象，否则返回None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                return render(request, "login.html", {"msg": u"用户还未激活，请登陆注册邮箱激活。"})
            return render(request, "login.html", {"msg": u"用户名或密码错误。"})
        return render(request, "login.html", {"login_form": login_form, "msg": u"请修正上面的错误。"})


class ForgetPwdView(View):
    """
    找回密码视图
    """

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "forgetpwd.html", {"msg": u"邮件已发送，请注意查收。"})
        return render(request, "forgetpwd.html", {"forget_form": forget_form, "msg": u"请修正上面的错误。"})
