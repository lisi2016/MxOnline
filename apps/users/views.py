# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course


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
    修改密码(找回密码时)
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

            # 写入注册消息
            user_message = UserMessage()
            user_message.user = user_name
            user_message.message = u"欢迎来到慕学网，这里驻扎有业界大佬，以及大量优秀课程，最后非常感谢您的认可！"
            user_message.save()

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
                    return HttpResponseRedirect(reverse('index'))
                return render(request, "login.html", {"msg": u"用户还未激活，请登陆注册邮箱激活。"})
            return render(request, "login.html", {"msg": u"用户名或密码错误。"})
        return render(request, "login.html", {"login_form": login_form, "msg": u"请修正上面的错误。"})


class LogoutView(View):
    """
    用户登出
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


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


class UserInfoView(LoginRequiredMixin, View):
    """
    个人信息
    """

    def get(self, request):
        return render(request, "usercenter-info.html", {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)  # 若不指定用户则新增记录
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
        return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


class UploadImageView(LoginRequiredMixin, View):
    """
    头像修改
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
        return HttpResponse(json.dumps({'status': 'fail'}), content_type="application/json")


class UpdatePwdView(LoginRequiredMixin, View):
    """
    修改密码(个人中心)
    """

    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': u"两次输入的密码不一致。"}),
                                    content_type="application/json")
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
        return HttpResponse(json.dumps(modify_pwd_form.errors), content_type="application/json")


class SendEmailCaptchaView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse(json.dumps({'email': u"邮箱已经存在。"}), content_type="application/json")

        send_register_email(email, "update_email")
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱（个人中心）
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            request.user.email = email
            request.user.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
        return HttpResponse(json.dumps({'email': u"邮箱或验证码错误。"}), content_type="application/json")


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程（个人中心）
    """

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的机构（个人中心）
    """

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我收藏的讲师（个人中心）
    """

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程（个人中心）
    """

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """

    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = all_messages.filter(has_read=False)
        for all_unread_message in all_unread_messages:
            all_unread_message.has_read = True
            all_unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 5, request=request)
        message_page = p.page(page)
        return render(request, 'usercenter-message.html', {
            'message_page': message_page,
        })


class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banner': all_banner,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html')
    response.status_code = 500
    return response
