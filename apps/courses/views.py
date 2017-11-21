# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q
import json

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.
class CourseListView(View):
    """
    课程列表
    """

    def get(self, request):
        search_keywords = request.GET.get('keywords', '')
        sort = request.GET.get('sort', '')  # 获取Get的参数

        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))

        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'sort': sort,
            'all_courses': courses,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 相关课程推荐
        tag = course.tag
        relate_courses = None
        if tag:
            relate_courses = Course.objects.filter(tag=tag).exclude(id=course.id).order_by("-click_nums")[:1]

        # 判断课程收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                course_fav_status = "已收藏"
            else:
                course_fav_status = "收藏"
        else:
            course_fav_status = "登录后收藏"

        # 判断课程机构收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                org_fav_status = "已收藏"
            else:
                org_fav_status = "收藏"
        else:
            org_fav_status = "登录后收藏"

        return render(request, "course-detail.html", {
            'course': course,
            'relate_courses': relate_courses,
            'course_fav_status': course_fav_status,
            'org_fav_status': org_fav_status,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        # 查询用户和课程是否关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 相关用户课程推荐
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 多条件还可以这么玩
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        course_resources = CourseResource.objects.filter(course=course)  # 还可以这么玩，厉害厉害
        return render(request, 'course-video.html', {
            'course': course,
            'relate_courses': relate_courses,
            'course_resources': course_resources,
        })


class CommentsView(LoginRequiredMixin, View):
    """
    课程评论
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        # 查询用户和课程是否关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 相关用户课程推荐
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 多条件还可以这么玩
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        course_resources = CourseResource.objects.filter(course=course)
        course_comments = CourseComments.objects.filter(course=course).order_by("-add_time")[:20]

        return render(request, 'course-comment.html', {
            'course': course,
            'relate_courses': relate_courses,
            'course_resources': course_resources,
            'course_comments': course_comments,
        })


class AddCommentsView(View):
    """
    添加课程评论
    """

    def post(self, request):
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")

        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type="application/json")

        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功。'}), content_type="application/json")
        return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败。'}), content_type="application/json")


class VideoPlayView(View):
    """
    视频播放页面
    """

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        # 查询用户和课程是否关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 相关用户课程推荐
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 多条件还可以这么玩
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        course_resources = CourseResource.objects.filter(course=course)  # 还可以这么玩，厉害厉害
        return render(request, 'course-play.html', {
            'course': course,
            'relate_courses': relate_courses,
            'course_resources': course_resources,
            'video': video,
        })
