from django.shortcuts import render
import json
from django.http import HttpResponse, response, JsonResponse
from . import models
from django.forms import model_to_dict
from action import models as action_models
from course import models as course_models
from course.models import Machine


# Create your views here.
def index(request):
    pass


# 获取动作等级
def getactionlevel(request):
    try:
        # 获取课程类型全部queryset对象
        types = models.ActionLevel.objects.all().values('level')
        # 新建list对数据封装
        # types_list = []
        # # 遍历每个对象
        # for t in types:
        #     # 将每个对象转换为字典类型
        #     t_dict = model_to_dict(t)
        #     # 获取外键关联的url
        #     t_dict['picture_url'] = models.CoursePicture.objects.filter(id=t.picture_id).values('url')[0]['url']
        #     # 为字典添加key值
        #     t_dict['nums'] = models.Course.objects.filter(type_id=t.id).count()
        #     types_list.append(t_dict)

        return HttpResponse(json.dumps(list(types), ensure_ascii=False))
    except Exception as ex:
        print(ex)


# 获取动作肌肉
def getactionpart(request):
    try:
        # 获取动作肌肉
        name = models.Muscle.objects.all().values('name')

        return HttpResponse(json.dumps(list(name), ensure_ascii=False))
    except Exception as ex:
        print(ex)


# 获取动作器材
def getactionmachine(request):
    try:
        # 获取课程类型全部queryset对象
        machine = Machine.objects.all().values('name')

        return HttpResponse(json.dumps(list(machine), ensure_ascii=False))
    except Exception as ex:
        print(ex)


#         搜索动作
def search(request):
    try:
        conditions = {}
        con = json.loads(request.body)
        pagesize = 12
        index = int(con['index'])
        start = pagesize * (index - 1)
        end = pagesize * index
        if con['searchcontent']:
            conditions["name__regex"] = con['searchcontent']
        if con['levelcon']:
            conditions["level__level"] = con['levelcon']
        if con['musclecon']:
            conditions["muscle__name"] = con['musclecon']
        if con['machinecon']:
            conditions["machine__name"] = con['machinecon']
        # if  con['searchcontent']:
        # actions=models.ActionLibrary.objects.filter(name__contains=con['searchcontent'])[start:end].values('id','name','info','level__level','muscle__name','picture__url')
        # print(conditions)
        actions = models.ActionLibrary.objects.filter(**conditions)[start:end].values('id', 'name', 'info',
                                                                                      'level__level', 'machine__name','muscle__name', 'picture__url')

        # print(actions)
        return HttpResponse(json.dumps(list(actions), ensure_ascii=False))
    except Exception as ex:
        return JsonResponse({"code": "500"})


# 计算动作个数
def Acount(request):
    try:
        conditions = {}
        con = json.loads(request.body)
        if con['searchcontent'] or con['levelcon'] or con['musclecon'] or con['machinecon']:

            # print('here')
            if con['searchcontent']:
                conditions["name__regex"] = con['searchcontent']
            if con['levelcon']:
                conditions["level__level"] = con['levelcon']
            if con['musclecon']:
                conditions["muscle__name"] = con['musclecon']
            if con['machinecon']:
                conditions["machine__name"] = con['machinecon']
            # print(conditions)
            acount = models.ActionLibrary.objects.filter(**conditions).count()
        else:
            acount = models.ActionLibrary.objects.filter().count()

        # if name:
        #     len = action_models.ActionLibrary.objects.filter(name__icontains=name).count()
        #     print(len)
        # else:
        #     len = action_models.ActionLibrary.objects.all().count()
        #     print(len)
        # print(acount)
        return JsonResponse({"acount": acount})
    except Exception as ex:
        return JsonResponse({"code": "500"})


def getactionbyid(request):
    try:
        resurt = []
        action_id = request.GET.get('id')
        action = list(
            action_models.ActionLibrary.objects.filter(id=action_id).values('name', 'info', 'times', 'level__level',
                                                                            'machine__name', 'muscle__name'))
        muscle_picture_url = list(action_models.ActionMusclePicture.objects.filter(action_id=action_id).values('url'))
        if not muscle_picture_url:
            muscle_picture_url=[{'url':'https://w2.dwstatic.com/yy/ojiastoreimage/1479463387706_am_'}]
        action_picture = list(action_models.ActionLibrary.objects.filter(id=action_id).values('picture__url'))
        if not action_picture:
            action_picture=[{'url':'https://w2.dwstatic.com/yy/ojiastoreimage/6f36380e9c3478913497538d77846575.jpg'}]

        jibendongzuo_picture = list(action_models.ActionYaolingtu.objects.filter(action_id=action_id).values('url'))
        if not jibendongzuo_picture:
            jibendongzuo_picture=[{'url':'https://w2.dwstatic.com/yy/ojiastoreimage/6f36380e9c3478913497538d77846575.jpg'}]

        print(action_picture)
        ss = {
            "name": action[0]['name'],
            "info": action[0]['info'],
            "times": action[0]['times'],
            "level": action[0]['level__level'],
            "machine_name": action[0]['machine__name'],
            "muscle_name": action[0]['muscle__name'],
            "action_picture": action_picture[0]['picture__url'],
        }
        muscle_url = []
        for muscle in muscle_picture_url:
            muscle_url.append(muscle['url'])
        ss['muscle_url'] = muscle_url
        # jibendongzuo_picture = []
        # for jiben in jibendongzuo_picture:
        #     jibendongzuo_picture.append(jiben['url'])

        ss['jibendongzuo_picture'] = jibendongzuo_picture


        resurt.append(ss)
        return HttpResponse(json.dumps(resurt, ensure_ascii=False))
        # return JsonResponse({"code":"200"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code":"500"})
