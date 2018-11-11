from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from shop import models as shop_models
from course import models as course_models
from collections import OrderedDict
import json
def index(request):
    try:
        # 调用get_index_page获取首页中的数据
        res = list(shop_models.GoodPicture.objects.filter(size='1').values('url','good_id','good__name','good__intergal'))
        # print(res)
        b = OrderedDict()
        for item in res:
            b.setdefault(item['good_id'], {**item, })
        b = list(b.values())
        # print(b[0:20])
        # return HttpResponse(json.dumps(b[0:8],ensure_ascii=False))
        return HttpResponse(json.dumps(b[0:8],ensure_ascii=False))
    except Exception as ex:
        print(ex)
        # 获取数据失败时返回401
        return JsonResponse({"code":"401"})
