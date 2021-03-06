# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
import json

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course


# Create your views here.
class OrgView(View):
    """
    授课机构视图
    """

    def get(self, request):
        orgs = CourseOrg.objects.all()  # 授课机构
        hot_orgs = orgs.order_by("-click_nums")[:3]  # 热门机构排名
        citys = CityDict.objects.all()  # 城市
        search_keywords = request.GET.get('keywords', '')
        city_id = request.GET.get('city', '')  # 获取Get的城市id
        category = request.GET.get('cg', '')  # 获取Get的机构类别
        sort = request.GET.get('sort', '')  # 获取Get的参数

        # 机构搜索
        if search_keywords:
            orgs = orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        if city_id:
            orgs = orgs.filter(city_id=int(city_id))
        if category:
            orgs = orgs.filter(category=category)
        if sort:
            if sort == "students":
                orgs = orgs.order_by("-students")
            elif sort == "courses":
                orgs = orgs.order_by("-course_nums")

        org_nums = orgs.count()  # 统计机构数

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(orgs, 2, request=request)
        org_page = p.page(page)

        return render(request, "org-list.html", {
            "orgs": org_page,
            "org_nums": org_nums,
            "citys": citys,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """

    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)  # 提交并保存到数据库，commit为True才会保存
            return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
        return HttpResponse(json.dumps({'status': 'fail', 'msg': '提交出错。'}), content_type="application/json")


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_courses = course_org.course_set.all()[:3]  # 通过外键反取课程表数据
        all_teachers = course_org.teacher_set.all()[:1]

        # 判断收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                fav_status = "已收藏"
            else:
                fav_status = "收藏"
        else:
            fav_status = "登录后收藏"
        return render(request, 'org-detail-homepage.html', {
            'current_page': current_page,
            'course_org': course_org,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'fav_status': fav_status
        })


class OrgCourseView(View):
    """
    机构课程
    """

    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()  # 通过外键反取课程表数据

        # 判断收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                fav_status = "已收藏"
            else:
                fav_status = "收藏"
        else:
            fav_status = "登录后收藏"
        return render(request, 'org-detail-course.html', {
            'current_page': current_page,
            'course_org': course_org,
            'all_courses': all_courses,
            'fav_status': fav_status
        })


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                fav_status = "已收藏"
            else:
                fav_status = "收藏"
        else:
            fav_status = "登录后收藏"
        return render(request, 'org-detail-desc.html', {
            'current_page': current_page,
            'course_org': course_org,
            'fav_status': fav_status
        })


class OrgTeacherView(View):
    """
    机构讲师
    """

    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        # 判断收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                fav_status = "已收藏"
            else:
                fav_status = "收藏"
        else:
            fav_status = "登录后收藏"
        return render(request, 'org-detail-teachers.html', {
            'current_page': current_page,
            'course_org': course_org,
            'all_teachers': all_teachers,
            'fav_status': fav_status
        })


class AddFavView(View):
    """
    用户收藏
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type="application/json")

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 记录已经存在，则取消收藏
            exist_records.delete()
            # 减去收藏数
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                if course.fav_nums > 0:
                    course.fav_nums -= 1
                    course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                if course_org.fav_nums > 0:
                    course_org.fav_nums -= 1
                    course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                if teacher.fav_nums > 0:
                    teacher.fav_nums -= 1
                    teacher.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏'}), content_type="application/json")

        # 记录不存在，则收藏
        user_fav = UserFavorite()
        if int(fav_id) > 0 and int(fav_type) > 0:
            user_fav.user = request.user
            user_fav.fav_id = int(fav_id)
            user_fav.fav_type = int(fav_type)
            user_fav.save()
            # 增加收藏数
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums += 1
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums += 1
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums += 1
                teacher.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}), content_type="application/json")
        return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏出错。'}), content_type="application/json")


class TeacherListView(View):
    """
    讲师列表页面
    """

    def get(self, request):
        search_keywords = request.GET.get('keywords', '')
        sort = request.GET.get('sort', '')

        all_teachers = Teacher.objects.all()

        # 讲师搜索
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords) |
                                               Q(work_position__icontains=search_keywords))

        if sort and sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 2, request=request)
        teacher_page = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teachers": teacher_page,
            "sort": sort,
            "sorted_teacher": sorted_teacher,
        })


class TeacherDetailView(View):
    """
    讲师详情页
    """

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        # 判断讲师收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                teacher_fav_status = "已收藏"
            else:
                teacher_fav_status = "收藏"
        else:
            teacher_fav_status = "登录后收藏"

        # 判断课程机构收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                org_fav_status = "已收藏"
            else:
                org_fav_status = "收藏"
        else:
            org_fav_status = "登录后收藏"

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_courses": all_courses,
            "sorted_teacher": sorted_teacher,
            "teacher_fav_status": teacher_fav_status,
            "org_fav_status": org_fav_status,
        })
