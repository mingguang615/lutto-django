from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.forms import model_to_dict
import json
# from utils import token as toto
from utils import token as toto
from user.models import AddCourse
from user.models import UserInfo
from action.models import CourseAction
from action.models import ActionLibrary
from user import models as user_models
from course import models as course_models
from . import models
from datetime import datetime

# Create your views here.


def index(request):
    pass


def getCourse(request):
    try:
        course = list(
            course_models.Course.objects.all().values('id', 'name', 'consume_total', 'minute_avg', 'machine__name',
                                                      'picture__url'))
        return HttpResponse(json.dumps(course[0:20], ensure_ascii=False))
        # return JsonResponse({"code":"200"})
    except Exception as ex:
        return JsonResponse({"code": "404"})


# 搜索课程
def search(request, index, cname):
    # 获取类型为tid的全部对象
    pagesize = 12
    index = int(index)
    start = pagesize * (index - 1)
    end = pagesize * index

    if cname:
        courses = models.Course.objects.order_by('-useraddcount').filter(name__icontains=cname)[start:end].values('id', 'name', 'day',
                                                                                        'type__type_name',
                                                                                        'level__level', 'picture__url')
    else:
        courses = models.Course.objects.order_by('-useraddcount').all()[start:end].values('id', 'name', 'day', 'type__type_name', 'level__level',
                                                                'picture__url')
    print(courses)

    # # 遍历每个对象
    for c in courses:

        c["useradd"] = AddCourse.objects.filter(course_id=c["id"]).count()
        parts = models.CourseTrainPart.objects.filter(course_id=c["id"]).values('bodypart__bodypart')
        bodys = []
        for part in parts:
            bodys.append(part['bodypart__bodypart'])
        c["trainbody"] = bodys
        # course_list.append(c_dict)
    # print(course_list)

    return HttpResponse(json.dumps(list(courses), ensure_ascii=False))


# 计算页码
def pagecount(request, con):
    try:
        if con:
            len = models.Course.objects.filter(name__icontains=con).count()
            print(len)
        else:
            len = models.Course.objects.all().count()
            print(len)
        return JsonResponse({"acount": len})
    except Exception as ex:
        return JsonResponse({"code": "500"})


# 获取课程类型
def getcoursefenlei(request):
    # 获取课程类型全部queryset对象
    types = models.CourseType.objects.all()
    # 新建list对数据封装
    types_list = []
    # 遍历每个对象
    for t in types:
        # 将每个对象转换为字典类型
        t_dict = model_to_dict(t)
        # 获取外键关联的url
        t_dict['picture_url'] = models.CoursePicture.objects.filter(id=t.picture_id).values('url')[0]['url']
        # 为字典添加key值
        t_dict['nums'] = models.Course.objects.filter(type_id=t.id).count()
        types_list.append(t_dict)

    return HttpResponse(json.dumps(types_list, ensure_ascii=False))


# 通过课程类型id获取课程
def getCourseByTypeid(request, index, tid):
    # 获取类型为tid的全部对象
    pagesize = 6
    index = int(index)
    start = pagesize * (index - 1)
    end = pagesize * index

    courses = models.Course.objects.filter(type_id=tid)[start:end].values('id', 'name', 'day', 'type__type_name',
                                                                          'level__level', 'picture__url')
    course_list = []
    # 遍历每个对象
    for c in courses:
        c["useradd"] = AddCourse.objects.filter(course_id=c["id"]).count()
        parts = models.CourseTrainPart.objects.filter(course_id=c["id"]).values('bodypart__bodypart')
        bodys = []
        for part in parts:
            bodys.append(part['bodypart__bodypart'])
        c["trainbody"] = bodys
        # # 将每个对象转换为字典类型
        # c_dict = model_to_dict(c)
        # # 获取该类型课程数目
        # c_dict["course_nums"] = courses.count()
        # # 获取该类型课程名称
        # c_dict["type"] = courses.values('type__type_name')[0]['type__type_name']
        # # 获取该类型课程数目
        # c_dict["level"] = courses.values('level__level')[0]['level__level']
        # # 获取该类型课程数目
        # c_dict["picture"] = courses.values('picture__url')[0]['picture__url']
        # # 获取该类型课程数目
        # c_dict["useradd"] = AddCourse.objects.filter(course_id=c.id).count()
        # parts = models.CourseTrainPart.objects.filter(course_id=c.id).values('bodypart__bodypart')
        # bodys = []
        # for part in parts:
        #     bodys.append(part['bodypart__bodypart'])
        # c_dict["trainbody"] = bodys
        # course_list.append(c_dict)
    # print(course_list)
    # print(courses)
    return HttpResponse(json.dumps(list(courses), ensure_ascii=False))


# 通过课程类型id获取课程数目
def pagecountbytid(request, con):
    print(con)
    try:
        if con:
            len = models.Course.objects.filter(type_id=con).count()
            print(len)
        else:
            len = models.Course.objects.all().count()
            print(len)
        return JsonResponse({"acount": len})
    except Exception as ex:
        return JsonResponse({"code": "500"})


# 根据课程id获取课程信息

def getCourseInfoById(request):
    # 获取类型为tid的全部对象
    try:
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        cid = int(data['cid'])
        courses = models.Course.objects.filter(id=cid)
        course_list = []
        for course in courses:
            course_dict = model_to_dict(course)
            course_dict["picture"] = courses.values('picture__url')[0]['picture__url']
            course_dict["level"] = courses.values('level__level')[0]['level__level']
            course_dict["picture"] = courses.values('picture__url')[0]['picture__url']
            course_dict["machine"] = courses.values('machine__name')[0]['machine__name']
            course_dict['type_name'] = courses.values('type__type_name')[0]['type__type_name']
            course_dict["add_flag"] = False
            if data['headers']['token']:
                token = data['headers']['token']
                res = toto.openToken(token)
                if res:
                    result = AddCourse.objects.filter(course_id=cid, user_id=res['user_id'])
                    if result:
                        course_dict["add_flag"] = True

            course_dict["useradd"] = AddCourse.objects.filter(course_id=cid).count()
            parts = models.CourseTrainPart.objects.filter(course_id=cid).values('bodypart__bodypart')
            bodys = []
            for part in parts:
                bodys.append(part['bodypart__bodypart'])
            course_dict["trainbody"] = bodys
            course_list.append(course_dict)
        # print(course_list)

        return HttpResponse(json.dumps(course_list, ensure_ascii=False))
    except Exception as ex:
        print(ex)


# 根据课程id 获取动作信息
def getActionByCid(request, cid):
    # 获取类型为tid的全部对象
    course = models.Course.objects.filter(id=cid)[0]
    # 将queryset对象转化为字典类型
    course_dict = model_to_dict(course)
    # 获取课程天数
    daymax = CourseAction.objects.filter(course_id=cid).latest('day_num').day_num
    # courses = CourseAction.objects.filter(course_id=cid,day_num=1).values('action__name','action__times','action')
    days = []
    # 获取每天的动作信息
    for i in range(1, int(daymax) + 1):
        actions = CourseAction.objects.filter(course_id=cid, day_num=i).values('action__id', 'action__name',
                                                                               'action__times', 'action__picture__url')
        # 将每天的动作集合放到days
        days.append(list(actions))
    course_dict['days'] = days
    return JsonResponse(course_dict)
    # return HttpResponse(json.dumps(action_list, ensure_ascii=False))


# 获取课程最新评论信息
def getCourseComment(request):
    try:
        if request.method == "POST":
            # 获取课程类型全部queryset对象
            data = json.loads(request.body.decode('utf-8'))
            # 获取token
            token = data['headers']['token']
            res = toto.openToken(token)
            # 获取课程id
            cid = data['cid']
            comments = models.CourseComment.objects.order_by('-time').filter(course_id=cid)
            # 新建list对数据封装
            comment_list = []
            # 遍历每个对象
            for c in comments:
                # 将每个对象转换为字典类型
                c_dict = model_to_dict(c)
                c_dict['id'] = models.CourseComment.objects.filter(id=c.id).values('id')[0]['id']
                c_dict['time'] = str(models.CourseComment.objects.filter(id=c.id).values('time')[0]["time"])[0:19]
                c_dict['like'] = models.CourseCommentLike.objects.filter(comment_id=c.id).count()
                c_dict['replynum'] = models.CourseCommentReply.objects.filter(comment_id=c.id).count()
                c_dict['deletecomment_flag'] = False
                c_dict['like_flag'] = False
                if res:
                    flag = models.CourseComment.objects.filter(id=c.id, user_id=res['user_id']).count()
                    flag1 = models.CourseCommentLike.objects.filter(comment_id=c.id, user_id=res['user_id']).count()
                    if flag1:
                        c_dict['like_flag'] = True
                    if flag:
                        c_dict['deletecomment_flag'] = True

                c_dict['username'] = UserInfo.objects.filter(user_id=c.user_id).values('name')[0]['name']
                c_dict['icon'] = UserInfo.objects.filter(user_id=c.user_id).values('icon__icon_url')[0][
                    'icon__icon_url']
                reply_list = []
                reply = models.CourseCommentReply.objects.order_by('-time').filter(comment_id=c.id)
                for r in reply:
                    r_dict = model_to_dict(r)
                    r_dict['time'] = str(models.CourseCommentReply.objects.filter(id=r.id).values('time')[0]["time"])[0:19]
                    r_dict['username'] = UserInfo.objects.filter(user_id=r.user_id).values('name')[0]['name']
                    r_dict['icon'] = UserInfo.objects.filter(user_id=r.user_id).values('icon__icon_url')[0][
                        'icon__icon_url']
                    r_dict['content'] = models.CourseCommentReply.objects.filter(id=r.id).values('content')[0][
                        'content']
                    c_dict['reply_flag'] = False
                    r_dict['deletereply_flag'] = False

                    if res:
                        flag = models.CourseCommentReply.objects.filter(comment_id=c.id, user_id=res['user_id']).count()
                        flag1 = models.CourseCommentReply.objects.filter(id=r.id, comment_id=r.comment_id,
                                                                         user_id=res['user_id']).count()
                        if flag:
                            c_dict['reply_flag'] = True
                        if flag1:
                            r_dict['deletereply_flag'] = True
                    reply_list.append(r_dict)
                c_dict['commnetreply'] = reply_list
                comment_list.append(c_dict)
            print(comment_list)
            return HttpResponse(json.dumps(comment_list, ensure_ascii=False))
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "404"})


# 获取热门课程评论信息
def getHotCourseComment(request):
    try:
        if request.method == "POST":
            # 获取课程类型全部queryset对象
            data = json.loads(request.body.decode('utf-8'))
            cid = data['cid']
            token = data['headers']['token']
            res = toto.openToken(token)
            # 解析token
            # 判断是否登录
            # models.CourseCommentLike.objects.filter('comment_id').count()
            comments = models.CourseComment.objects.order_by('-likes').filter(course_id=cid)
            # 新建list对数据封装
            comment_list = []
            # 遍历每个对象
            for c in comments:
                # 将每个对象转换为字典类型
                c_dict = model_to_dict(c)
                c_dict['id'] = models.CourseComment.objects.filter(id=c.id).values('id')[0]['id']
                c_dict['time'] = models.CourseComment.objects.filter(id=c.id).values('time').values('time')[0][
                    'time'].strftime('%Y-%m-%d %H:%I:%S')
                c_dict['like'] = models.CourseCommentLike.objects.filter(comment_id=c.id).count()
                c_dict['replynum'] = models.CourseCommentReply.objects.filter(comment_id=c.id).count()
                c_dict['deletecomment_flag'] = False
                c_dict['like_flag'] = False
                if res:
                    flag = models.CourseComment.objects.filter(id=c.id, user_id=res['user_id']).count()
                    flag1 = models.CourseCommentLike.objects.filter(comment_id=c.id, user_id=res['user_id']).count()
                    if flag1:
                        c_dict['like_flag'] = True
                    if flag:
                        c_dict['deletecomment_flag'] = True

                c_dict['username'] = UserInfo.objects.filter(user_id=c.user_id).values('name')[0]['name']
                c_dict['icon'] = UserInfo.objects.filter(user_id=c.user_id).values('icon__icon_url')[0][
                    'icon__icon_url']
                reply_list = []
                reply = models.CourseCommentReply.objects.order_by('-time').filter(comment_id=c.id)
                for r in reply:
                    r_dict = model_to_dict(r)
                    r_dict['time'] = models.CourseCommentReply.objects.filter(id=r.id).values('time').values('time')[0][
                        'time'].strftime('%Y-%m-%d %H:%I:%S')
                    r_dict['username'] = UserInfo.objects.filter(user_id=r.user_id).values('name')[0]['name']
                    r_dict['icon'] = UserInfo.objects.filter(user_id=r.user_id).values('icon__icon_url')[0][
                        'icon__icon_url']
                    r_dict['content'] = models.CourseCommentReply.objects.filter(id=r.id).values('content')[0][
                        'content']
                    c_dict['reply_flag'] = False
                    r_dict['deletereply_flag'] = False

                    if res:
                        flag = models.CourseCommentReply.objects.filter(comment_id=c.id, user_id=res['user_id']).count()
                        flag1 = models.CourseCommentReply.objects.filter(id=r.id, comment_id=r.comment_id,
                                                                         user_id=res['user_id']).count()
                        if flag:
                            c_dict['reply_flag'] = True
                        if flag1:
                            r_dict['deletereply_flag'] = True
                    reply_list.append(r_dict)
                c_dict['commnetreply'] = reply_list
                comment_list.append(c_dict)
            return HttpResponse(json.dumps(comment_list[0:3], ensure_ascii=False))
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "404"})


# 回复评论
def replyComment(request):
    try:
        # 需要 评论id 评论内容 token
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            content = data['content']
            comment_id = int(data['comment_id'])
            token = data['headers']['token']
            res = toto.openToken(token)
            # result=models.AddCourse.objects.filter(course_id=course_id,user_id=res['user_id']).values()
            if res:
                addcomment = {
                    'comment_id': comment_id,
                    'user_id': res['user_id'],
                    'content': content,
                    'time':datetime.utcnow()
                }
                print(addcomment)
                models.CourseCommentReply.objects.create(**addcomment)
                # print(res['user_id'])
                return JsonResponse({"code": "210"})
            else:
                return JsonResponse({"code": "没登陆"})

    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "404"})


# 删除课程评论
def delCourseComment(request):
    try:
        # 需要 评论id  token
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            # content = data['content']
            comment_id = int(data['commentid'])
            token = data['headers']['token']
            res = toto.openToken(token)
            if res:
                models.CourseComment.objects.filter(id=comment_id).delete()
                return JsonResponse({"code": "210"})
            else:
                return JsonResponse({"code": "没登陆"})

    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "404"})


# 删除回复
def delCourseReply(request):
    try:
        # 需要 回复id  token
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            # content = data['content']
            replyid = int(data['replyid'])
            token = data['headers']['token']
            res = toto.openToken(token)
            # result=models.AddCourse.objects.filter(course_id=course_id,user_id=res['user_id']).values()
            if res:

                models.CourseCommentReply.objects.filter(id=replyid).delete()
                # print(res['user_id'])
                return JsonResponse({"code": "210"})
            else:
                return JsonResponse({"code": "没登陆"})

    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "404"})


# 添加课程
def addCourse(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            course_id = int(data['cid'])
            token = data['headers']['token']
            # 解析token
            res = toto.openToken(token)
            #
            if res:
                result = user_models.AddCourse.objects.filter(course_id=course_id, user_id=res['user_id']).values()
                addnum = models.Course.objects.filter(id=course_id).values('useraddcount')[0]['useraddcount']
                if result:
                    user_models.AddCourse.objects.filter(course_id=course_id, user_id=res['user_id']).delete()
                    res = addnum - 1
                    models.Course.objects.filter(id=course_id).update(useraddcount =res)
                    return JsonResponse({"code": "410"})
                else:
                    addcourse = {
                        'course_id': course_id,
                        'user_id': res['user_id']
                    }
                    user_models.AddCourse.objects.create(**addcourse)
                    # addnum = models.Course.objects.filter(id=course_id).values('useraddcount')[0]['useraddcount']
                    res = addnum + 1
                    models.Course.objects.filter(id=course_id).update(useraddcount=res)
                    return JsonResponse({"code": "210"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "404"})


def delCourse(request):
    pass
