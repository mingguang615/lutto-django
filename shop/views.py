from user import models as user_models
from utils.shop import *
from collections import OrderedDict
import json, math
from django.http import HttpResponse, response, JsonResponse
from . import models
from django.db.models import Count
from utils.token import *
import datetime, time
from django.forms import model_to_dict
from user.models import UserInfo


# Create your views here.
def index(request):
    pass


# 商城搜索
def search(request):
    try:
        name = request.GET.get('name')
        index = request.GET.get('index')
        # 每页显示的商品个数
        pagesize = 20
        if index:
            index = int(index)
        else:
            index = 1
        # print(name)
        G = []
        if name:
            good = list(
                models.Goods.objects.filter(name__icontains=name)[pagesize * (index - 1):pagesize * index].values(
                    'kucun', 'name', 'intergal', 'gooddesc', 'goodbrand__name', 'goodclass__name', 'id'))
            if good:
                for g in good:
                    ss = {
                        "goods_kuncun": g['kucun'],
                        "goods_name": g['name'],
                        "goods_intergal": g['intergal'],
                        "goods_gooddesc": g['gooddesc'],
                        "good_class_name": g['goodclass__name'],
                        "goods_id": g['id'],
                        "goods_band_name": g['goodbrand__name']
                    }
                    G.append(ss)
                    goods = Greatgoods(G)
            else:
                pass
            good = list(
                models.GoodClass.objects.filter(name__icontains=name)[pagesize * (index - 1):pagesize * index].values(
                    'goods__kucun', 'goods__name', 'goods__intergal', 'goods__gooddesc', 'goods__goodbrand__name',
                    'name', 'goods__id'))
            if good:
                print(good)
                for g in good:
                    ss = {
                        "goods_kuncun": g['goods__kucun'],
                        "goods_name": g['goods__name'],
                        "goods_intergal": g['goods__intergal'],
                        "goods_gooddesc": g['goods__gooddesc'],
                        "good_class_name": g['name'],
                        "goods_id": g['goods__id'],
                        "goods_band_name": g['goods__goodbrand__name']
                    }
                    G.append(ss)
                    goods = Greatgoods(G)
            else:
                pass
            good = list(
                models.GoodBrand.objects.filter(name__icontains=name)[pagesize * (index - 1):pagesize * index].values(
                    'goods__kucun', 'goods__name', 'goods__intergal', 'goods__gooddesc', 'name',
                    'goods__goodclass__name', 'goods__id'))
            if good:
                for g in good:
                    ss = {
                        "goods_kuncun": g['goods__kucun'],
                        "goods_name": g['goods__name'],
                        "goods_intergal": g['goods__intergal'],
                        "goods_gooddesc": g['goods__gooddesc'],
                        "good_class_name": g['goods__goodclass__name'],
                        "goods_id": g['goods__id'],
                        "goods_band_name": g['name']
                    }
                    G.append(ss)
                goods = Greatgoods(G)
            else:
                pass
        else:
            good = list(models.Goods.objects.filter()[pagesize * (index - 1):pagesize * index].values('kucun', 'name',
                                                                                                      'intergal',
                                                                                                      'gooddesc',
                                                                                                      'goodbrand__name',
                                                                                                      'goodclass__name',
                                                                                                      'id'))
            if good:
                for g in good:
                    ss = {
                        "goods_kuncun": g['kucun'],
                        "goods_name": g['name'],
                        "goods_intergal": g['intergal'],
                        "goods_gooddesc": g['gooddesc'],
                        "good_class_name": g['goodclass__name'],
                        "goods_id": g['id'],
                        "goods_band_name": g['goodbrand__name']
                    }
                    G.append(ss)
                    goods = Greatgoods(G)
        return HttpResponse(json.dumps(Greatgoods(G), ensure_ascii=False))
    except Exception as ex:
        print(ex)


# 商城分页
def account(request):
    name = request.GET.get('name')
    try:
        if name:
            len1 = models.Goods.objects.filter(name__icontains=name).aggregate(
                len1=Count('id'))
            len2 = models.GoodClass.objects.filter(name__icontains=name).aggregate(
                len2=Count('goods__id'))
            len3 = models.GoodBrand.objects.filter(name__icontains=name).aggregate(
                len3=Count('goods__id'))
            len = (len1['len1']) + (len2['len2']) + (len3['len3'])
        else:
            len4 = models.Goods.objects.filter(name__icontains=name).aggregate(
                len4=Count('id'))
            len = len4['len4']
        return JsonResponse({"acount": len})
    except Exception as ex:
        return JsonResponse({"code": "500"})


# 添加购物车
def addGoodToCar(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            res = openToken(r['token'])
            if res:
                uu = list(
                    user_models.AddGood.objects.filter(user_id=res['user_id'], good_id=r['good_id']).values('num'))
                if uu:
                    new_num = uu[0]['num'] + r['num']
                    user_models.AddGood.objects.filter(user_id=res['user_id'], good_id=r['good_id']).update(num=new_num)
                else:
                    user_id = res['user_id']
                    ss = {
                        "good_id": r['good_id'],
                        "user_id": user_id,
                        "num": r['num']
                    }
                    user_models.AddGood.objects.create(**ss)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "206"})
        except Exception as ex:
            print('this is addGoodToCar')
            print(ex)
            return JsonResponse({"code": "500"})


# 更新用户购物车中的商品数量
def updataGoodNum(request):
    if request.method == 'POST':  # post请求方式
        try:
            # 获取前端请求的数据
            data = json.loads(request.body)
            # 解析token
            res = openToken(data['token'])
            if res:
                # 判断是不是正整数,以及输入的数字是否大于1
                if str(data["num"]).isdigit() and int(data["num"]) > 1:
                    new_num = int(data["num"])
                else:
                    new_num = 1
                # 更新用户购物车中商品数量
                user_models.AddGood.objects.filter(user_id=res['user_id'], good_id=data['good_id']).update(num=new_num)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "206"})
        except Exception as ex:
            print('this is updataGoodNum')
            print(ex)
            return JsonResponse({"code": "500"})


# 删除商品
def delGood(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            res = openToken(data['token'])
            if res:
                for good in data["good_list"]:
                    user_models.AddGood.objects.filter(user_id=res['user_id'], good_id=good).delete()
                    # if result:
                    #     user_models.AddGood.objects.filter(good_id=r['good_id']).delete()
                return JsonResponse({"code": "207"})
                # else:
                #     return JsonResponse({"code": "412"})
            else:
                return JsonResponse({"code": "411"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 获取商品详情
def getGoodById(request):
    try:
        good_id = request.GET.get('gid')
        goods = []
        good = list(
            models.Goods.objects.filter(id=good_id).values('kucun', 'name', 'intergal', 'gooddesc', 'goodbrand__name',
                                                           'goodclass__name'))
        goods_comments = models.GoodComment.objects.filter(good_id=good_id).aggregate(goods_comment=Count('content'))[
            'goods_comment']
        url = list(models.GoodPicture.objects.filter(good_id=good_id).values('url', 'size'))
        # 商品图片
        url_size_1 = []
        # 商品详情图片
        url_size_3 = []
        for u in url:
            if u:
                if u['size'] == '1':
                    url_size_1.append(u)
                else:
                    url_size_3.append(u)
        url1 = []
        url3 = []
        for i in range(len(url_size_1)):
            url1.append(url_size_1[i]['url'])
        for j in range(len(url_size_3)):
            url3.append(url_size_3[j]['url'])
        G = good[0]['gooddesc']
        good_name = G.split('@')
        aa = []
        for g in good_name:
            if g:
                if '店铺' in g or '价位' in g:
                    pass
                else:
                    aa.append(g)
        ss = {
            "name": good[0]['name'],
            "good_kucun": good[0]['kucun'],
            "intergal": good[0]['intergal'],
            "gooddesc": aa,
            "goodbrand_name": good[0]['goodbrand__name'],
            "goodclass_name": good[0]['goodclass__name'],
            "url_size_1": url1,
            "url_size_3": url3,
            "comment_num": goods_comments
        }
        goods.append(ss)
        return HttpResponse(json.dumps(goods, ensure_ascii=False))
    except Exception as ex:
        print('this is getGoodById')
        print(ex)
        return JsonResponse({"code": "500"})


# 获取商城的商品信息
def GoodIndex(request):
    try:
        goods = []
        good = list(
            models.Goods.objects.all().values('name', 'intergal', 'gooddesc', 'goodbrand__name', 'goodclass__name',
                                              'id'))
        for i in range(0, len(good)):
            goods_id = good[i]['id']
            res = list(models.GoodPicture.objects.filter(good=goods_id, size='1').values('good_id', 'url'))
            b = OrderedDict()
            for item in res:
                b.setdefault(item['good_id'], {**item, })
            b = list(b.values())
            goods_comment = models.GoodComment.objects.filter(good_id=goods_id).aggregate(
                goods_comment=Count('content'))
            ss = {
                "name": good[i]['name'],
                "intergla": good[i]['intergal'],
                "good_url": b[0]['url'],
                "goodbrand_name": good[i]['goodbrand__name'],
                "goodclass_name": good[i]['goodclass__name'],
                "good_id": good[i]['id'],
                "good_comment": goods_comment['goods_comment']
            }
            goods.append(ss)
        return HttpResponse(json.dumps(goods, ensure_ascii=False))
    except Exception as ex:
        print(ex)


# 显示评论
def GetGoodComment(request):
    try:
        COMMENT = []
        good_id = request.GET.get('gid')
        # 从评论表里查找good_id对应的评论
        comment = list(
            models.GoodComment.objects.filter(good_id=good_id).values('content', 'id', 'good_id', 'user_id', 'likes',
                                                                      'time'))
        for o in comment:
            user_id = o['user_id']

            user = list(user_models.UserInfo.objects.filter(user_id=user_id).values('name', 'icon__icon_url'))
            for u in user:
                name = u['name']
                icon_url = u['icon__icon_url']
            time = str(o['time'])
            tt = time.split('+')[0]
            import time
            time_array = time.strptime(tt, "%Y-%m-%d %H:%M:%S")
            timestamp = time.mktime(time_array)
            old_time = int(timestamp) + 28800
            now_time = int(time.time())
            time = now_time - old_time
            min = math.ceil(time / 60)
            if min < 60:
                comment_time = str(min) + '分之前'
            else:
                hour = math.ceil(min / 60)
                if hour < 24:
                    comment_time = str(hour) + '小时前'
                else:
                    day = math.ceil(hour / 24)
                    if day <= 3:
                        comment_time = str(day) + '天前'
                    else:
                        comment_time = tt.split(' ')[0]
            ss = {
                "content": o['content'],
                "comment_id": o['id'],
                "good_id": o['good_id'],
                "user_id": o['user_id'],
                "likes": o['likes'],
                "time": comment_time,
                "name": name,
                "icon_url": icon_url
            }
            print(ss)
            COMMENT.append(ss)
        return HttpResponse(json.dumps(COMMENT, ensure_ascii=False))
    except Exception as ex:
        print('this is GetGoodComment')
        print(ex)
        return JsonResponse({"code": "500"})


# # 商品评论
def GoodComment(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r["token"]  # token
            data = r['content']  # 商品评论内容
            good_id = r['good_id']  # 商品id
            order_id = r["order_id"]  # 订单id
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res = openToken(token)
            if res:
                ss = {
                    "user_id": res['user_id'],
                    "good_id": good_id,
                    "content": data,
                    "time": dt
                }
                models.GoodComment.objects.create(**ss)
                models.Order.objects.filter(id=order_id).update(status=4)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "210"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 回复二楼
def ShopReply(request):
    if request.method == 'POST':
        try:
            # 需要 评论id 评论内容 toke
            data = json.loads(request.body.decode('utf-8'))
            content = data['content']
            comment_id = int(data['comment_id'])
            token = data['token']
            res = openToken(token)
            # result=models.AddCourse.objects.filter(course_id=course_id,user_id=res['user_id']).values()
            if res:
                addcomment = {
                    'comment_id': comment_id,
                    'user_id': res['user_id'],
                    'content': content,
                }
                models.ShopCommentReply.objects.create(**addcomment)
                # print(res['user_id'])
                return JsonResponse({"code": "225"})
            else:
                return JsonResponse({"code": "411"})

        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 删除商品评论
def DelComment(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = request.META.get("HTTP_TOKEN")
            comment_id = r['comment_id']
            res = openToken(token)
            if res:
                user_id = res['user_id']
                comment = models.GoodComment.objects.filter(user_id=user_id, id=comment_id)
                if comment:
                    models.GoodComment.objects.filter(user_id=user_id, id=comment_id).delete()
                else:
                    return JsonResponse({"code": "418"})
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "211"})
        except Exception as ex:
            return JsonResponse({"code": "500"})


# 收藏商品
def LoveGood(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r['token']
            res = openToken(token)
            print(res)
            if res:
                p = len(r['good_id'])
                print(p)
                user_id = res['user_id']
                j = 0
                while j < p:
                    love = models.loveGood.objects.filter(good_id=r['good_id'][j], user_id=res["user_id"]).values()
                    if love:
                        pass
                    else:
                        ss = {
                            "user_id": user_id,
                            "good_id": r['good_id'][j]
                        }
                        models.loveGood.objects.create(**ss)
                        return JsonResponse({"code": "212"})
                    j = j + 1
                else:
                    return JsonResponse({"code": "417"})
            else:
                return JsonResponse({"code": "411"})

        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 商品评论点赞
def likeComment(request):
    try:
        r = json.loads(request.body)
        token = r['token']
        comment_id = r['comment_id']
        res = openToken(token)
        if res:
            # 判断，有没有这条评论，若没有返回425
            comment = models.GoodComment.objects.filter(id=comment_id).values()
            if comment:
                # 判断，是否已经点过赞，若已点过赞，就取消点赞
                result = models.ShopCommentLike.objects.filter(comment_id=comment_id, user_id=res['user_id']).values()
                if result:
                    models.ShopCommentLike.objects.filter(comment_id=comment_id, user_id=res['user_id']).delete()
                    likenum = list(models.GoodComment.objects.filter(id=comment_id).values('likes'))
                    res = likenum[0]['likes'] - 1
                    # 将评论的总点赞数-1
                    models.GoodComment.objects.filter(id=comment_id).update(likes=res)
                    return JsonResponse({"code": "214"})
                else:
                    ss = {
                        'comment_id': comment_id,
                        'user_id': res['user_id'],
                    }
                    models.ShopCommentLike.objects.create(**ss)
                    likenum = list(models.GoodComment.objects.filter(id=comment_id).values('likes'))
                    res = likenum[0]['likes'] + 1
                    # 将评论的总点赞数+1
                    models.GoodComment.objects.filter(id=comment_id).update(likes=res)
                    return JsonResponse({"code": "215"})
            else:
                return JsonResponse({"code": "425"})
        else:
            return JsonResponse({"code": "411"})
    except Exception as ex:
        print('this is likeComment')
        print(ex)
        return JsonResponse({"code": "500"})


# 生成订单
def OrderGood(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            orders = []
            token = data['token']
            res = openToken(token)
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if res:
                for gid in data['goods']:
                    ss = {
                        "user_id": res['user_id'],
                        "good_id": gid["good_id"],
                        "status": 1,
                        "time": dt,
                        "goodcounts": gid["good_num"],
                        "total": gid['total']
                    }
                    # 添加商品到订单表中
                    order = models.Order.objects.create(**ss)
                    # 删除用户添加到购物车的商品
                    user_models.AddGood.objects.filter(good_id=gid["good_id"], user_id=res['user_id']).delete()
                    orders.append(order.id)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "217", "order_id": orders})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 用户完成交易
def DealOrder(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r['token']
            res = openToken(token)
            if res:
                for order in r['order_id']:
                    # 查询用户的积分余额
                    intergal = list(user_models.Intergral.objects.filter(user_id=res['user_id']).values('intergral'))
                    user_intergal = int(intergal[0]['intergral'])
                    # 获得商品的总价
                    total = list(models.Order.objects.filter(id=order).values('total', 'goodcounts', 'good_id'))
                    order_intergal = total[0]['total']
                    # 判断用户的积分余额，有没有能力交易
                    if user_intergal < order_intergal:
                        return JsonResponse({"code": "427"})
                    else:
                        new_intergal = user_intergal - order_intergal
                        # 交易完成后，更新用户的积分余额
                        user_models.Intergral.objects.filter(user_id=res['user_id']).update(intergral=new_intergal)
                        # 查询商品的库存
                        kk = list(models.Goods.objects.filter(id=total[0]['good_id']).values('kucun'))
                        old_kucun = kk[0]['kucun']
                        new_kucun = int(old_kucun) - int(total[0]['goodcounts'])
                        # 判断库存是否充足
                        if new_kucun >= 0:
                            models.Goods.objects.filter(id=total[0]['good_id']).update(kucun=new_kucun)
                            # 查看订单的状态，若是未付款，则将未付款状态改成已付款，若已付款，再生成一次订单，并且状态为已付款
                            status = list(models.Order.objects.filter(id=order).values('status'))
                            if status[0]['status'] == 1:
                                models.Order.objects.filter(id=order).update(status=2)
                                models.Order.objects.filter(id=order).update(addressid=r['address_id'])
                            else:
                                order = list(models.Order.objects.filter(id=order).values())
                                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                ss = {
                                    "user_id": res['user_id'],
                                    "status": 2,
                                    "good_id": order[0]['good_id'],
                                    "goodcounts": order[0]['goodcounts'],
                                    "total": order[0]['total'],
                                    "time": dt,
                                    "addressid": r['address_id']
                                }
                                models.Order.objects.create(**ss)
                        else:
                            return JsonResponse({"code": "432"})
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "219"})
        except Exception as ex:
            print(ex)
            print('this is dealorder')
            return JsonResponse({"code": "500"})


# 查看所有订单（个人中心）
def GetAllOrder(request):
    if request.method == 'POST':
        try:
            ORDER = []
            r = json.loads(request.body)
            token = r['token']
            res = openToken(token)
            if res:
                order = list(models.Order.objects.filter(user_id=res['user_id']).values().order_by('-time'))
                if order:
                    for o in order:
                        rr = list(
                            models.GoodPicture.objects.filter(good=o['good_id'], size='1').values('good_id', 'url'))
                        b = OrderedDict()
                        for item in rr:
                            b.setdefault(item['good_id'], {**item, })
                        b = list(b.values())
                        good = list(models.Goods.objects.filter(id=o['good_id']).values('name'))
                        time = str(o['time'])
                        tt = time.split(' ')[0]
                        good_price = list(models.Goods.objects.filter(id=o['good_id']).values("intergal"))
                        ss = {
                            "good_id": o['good_id'],
                            "good_intergal": good_price[0]["intergal"],  # 商品所需积分
                            "order_id": o['id'],
                            "order_time": tt,
                            "order_status": o['status'],
                            "order_goodcounts": o['goodcounts'],
                            "order_total": o['total'],
                            "good_name": good[0]['name'],
                            "good_url": b[0]['url']
                        }
                        ORDER.append(ss)
                else:
                    return JsonResponse({"code": "426"})
            else:
                return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps(ORDER, ensure_ascii=False))
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 获取订单ID
def GetOrderById(request):
    if request.method == 'POST':
        try:
            ORDER = []
            r = json.loads(request.body)
            token = r['token']
            res = openToken(token)
            if res:
                for order in r['order_id']:
                    order = list(models.Order.objects.filter(user_id=res['user_id'], id=order).values())
                    if order:
                        for o in order:
                            rr = list(
                                models.GoodPicture.objects.filter(good=o['good_id'], size='1').values('good_id', 'url'))
                            b = OrderedDict()
                            for item in rr:
                                b.setdefault(item['good_id'], {**item, })
                            b = list(b.values())
                            good = list(models.Goods.objects.filter(id=o['good_id']).values('name'))
                            ss = {
                                "order_id": o['id'],
                                "order_time": str(order[0]["time"]).split("+")[0],
                                "order_status": o['status'],
                                "order_goodcounts": o['goodcounts'],
                                "order_total": o['total'],
                                "good_name": good[0]['name'],
                                "good_url": b[0]['url']
                            }
                            ORDER.append(ss)
                    else:
                        return JsonResponse({"code": "426"})
            else:
                return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps(ORDER, ensure_ascii=False))
        except Exception as ex:
            print(ex)
            print('this is getorderbyid')
            return JsonResponse({"code": "500"})


# 查看购车的商品
def GetCart(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            if 'token' in r.keys():
                GOOD = []
                TT = r['token']
                res = openToken(TT)
                print(res)
                if res:
                    good = list(user_models.AddGood.objects.filter(user_id=res['user_id']).values('good_id'))
                    print(good)
                    if good:
                        for i in range(len(good)):
                            good_id = good[i]['good_id']
                            goods = list(
                                models.Goods.objects.filter(id=good_id, addgood__user_id=res['user_id']).values('kucun',
                                                                                                                'name',
                                                                                                                'intergal',
                                                                                                                'gooddesc',
                                                                                                                'goodbrand__name',
                                                                                                                'goodclass__name',
                                                                                                                'id',
                                                                                                                'addgood__num',
                                                                                                                'addgood__checked'))
                            urls = list(
                                models.GoodPicture.objects.filter(good_id=good_id, size=1).values('url', 'good_id'))
                            b = OrderedDict()
                            for item in urls:
                                b.setdefault(item['good_id'], {**item, })
                            b = list(b.values())
                            ss = {
                                "good_id": good_id,
                                "good_url": b[0]['url'],
                                "good_name": goods[0]['name'],
                                "good_intergal": goods[0]['intergal'],
                                "good_num": goods[0]['addgood__num'],
                                "checked": goods[0]["addgood__checked"]
                            }
                            GOOD.append(ss)
                    else:
                        return JsonResponse({"code": "423"})
                else:
                    return JsonResponse({"code": "411"})
            else:
                return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps({"code": "213", "goods": GOOD}, ensure_ascii=False))
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})


# 更新商品信息
def updataCart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 取到token去解析，解析结果赋值给res
            res = openToken(data["token"])
            print(res)
            # 解析token成功
            if res:
                if data["status"] == "all":
                    user_models.AddGood.objects.filter(user_id=res["user_id"]).update(checked=data["checked"])
                else:
                    user_models.AddGood.objects.filter(user_id=res["user_id"], good_id=data["good_id"]).update(
                        checked=data["checked"])
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "500"})
        return JsonResponse({"code": "201"})


# 查看我的订单（商品）(个人中心)
def GetOrder(request):
    if request.method == 'POST':
        try:
            ORDER = []
            r = json.loads(request.body)
            token = r['token']
            res = openToken(token)
            if res:
                # 先检查用户有没有生成过订单
                order = list(models.Order.objects.filter(user_id=res['user_id'], status=r['good_status']).values())
                if order:
                    for o in order:
                        rr = list(
                            models.GoodPicture.objects.filter(good=o['good_id'], size='1').values('good_id', 'url'))
                        b = OrderedDict()
                        for item in rr:
                            b.setdefault(item['good_id'], {**item, })
                        b = list(b.values())
                        good = list(models.Goods.objects.filter(id=o['good_id']).values('name'))
                        time = str(o['time'])
                        tt = time.split('.' or '+')[0]
                        import time
                        time_array = time.strptime(tt, "%Y-%m-%d %H:%M:%S")
                        timestamp = time.mktime(time_array)
                        old_time = int(timestamp) + 28800
                        now_time = int(time.time())
                        time = now_time - old_time
                        min = math.ceil(time / 60)
                        if min < 60:
                            order_time = str(min) + '分之前'
                        else:
                            hour = math.ceil(min / 60)
                            if hour < 24:
                                order_time = str(hour) + '小时前'
                            else:
                                day = math.ceil(hour / 24)
                                if day <= 3:
                                    order_time = str(day) + '天前'
                                else:
                                    order_time = tt.split(' ')[0]
                        ss = {
                            "order_id": o['id'],
                            "order_time": order_time,
                            "order_status": o['status'],
                            "order_goodcounts": o['goodcounts'],
                            "order_total": o['total'],
                            "good_name": good[0]['name'],
                            "good_url": b[0]['url']
                        }
                        ORDER.append(ss)
                else:
                    return JsonResponse({"code": "426"})
            else:
                return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps(ORDER, ensure_ascii=False))
        except Exception as ex:
            print('this is gettorder')
            print(ex)
            return JsonResponse({"code": "500"})


# 删除订单
def DelOrder(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r['token']
            res = openToken(token)
            if res:
                # 先检查用户没有有生成过该订单
                order = models.Order.objects.filter(id=r['order_id'], user_id=res['user_id']).values()
                if order:
                    models.Order.objects.filter(id=r['order_id'], user_id=res['user_id']).delete()
                else:
                    return JsonResponse({"code": "426"})
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "218"})
        except Exception as ex:
            print('this is deforder')
            print(ex)
            return JsonResponse({"code": "500"})


# 显示评论
def GetGoodComment(request):
    try:
        COMMENT = []
        good_id = request.GET.get('gid')
        # 从评论表里查找good_id对应的评论
        comment = list(
            models.GoodComment.objects.filter(good_id=good_id).values('content', 'id', 'good_id', 'user_id', 'likes',
                                                                      'time'))
        if comment:
            for o in comment:
                user_id = o['user_id']
                user = list(user_models.UserInfo.objects.filter(user_id=user_id).values('name', 'icon__icon_url'))
                for u in user:
                    import time
                    name = u['name']
                    icon_url = u['icon__icon_url']
                    old_time = o['time']
                    now_time = datetime.datetime.now()
                    d1 = time.mktime(old_time.timetuple())
                    d2 = time.mktime(now_time.timetuple())
                    pinlun_time = int(d2 - d1)
                    min = math.ceil(pinlun_time / 60)
                    if min < 60:
                        comment_time = str(min) + '分之前'
                    else:
                        hour = math.ceil(min / 60)
                        if hour < 24:
                            comment_time = str(hour) + '小时前'
                        else:
                            day = math.ceil(hour / 24)
                            if day <= 3:
                                comment_time = str(day) + '天前'
                            else:
                                comment_time = str(old_time).split(' ')[0]

                    ss = {
                        "content": o['content'],
                        "comment_id": o['id'],
                        "good_id": o['good_id'],
                        "user_id": o['user_id'],
                        "likes": o['likes'],

                        "time": comment_time,
                        "name": name,
                        "icon_url": icon_url,
                        "replycomment": ""
                    }
                    REPCOMENT = []
                    remcomment = list(
                        models.ShopCommentReply.objects.filter(comment_id=o['id']).values('id', 'user_id', 'time',
                                                                                          'content'))
                    import time
                    for rem in remcomment:
                        reuser = list(
                            user_models.UserInfo.objects.filter(user_id=rem['user_id'], ).values('name',
                                                                                                 'icon__icon_url'))
                        old_time = rem['time']
                        now_time = datetime.datetime.now()
                        d1 = time.mktime(old_time.timetuple())
                        d2 = time.mktime(now_time.timetuple())
                        pinlun_time01 = int(d2 - d1)
                        min = math.ceil(pinlun_time01 / 60)
                        if min < 60:
                            remcomment_time = str(min) + '分之前'
                        else:
                            hour = math.ceil(min / 60)
                            if hour < 24:
                                remcomment_time = str(hour) + '小时前'
                            else:
                                day = math.ceil(hour / 24)
                                if day <= 3:
                                    remcomment_time = str(day) + '天前'
                                else:
                                    remcomment_time = str(old_time).split(' ')[0]
                        bb = {
                            "content": rem['content'],
                            "comment_id": rem['id'],
                            "good_id": o['good_id'],
                            "user_id": rem['user_id'],
                            "time": remcomment_time,
                            "name": reuser[0]['name'],
                            "icon_url": reuser[0]['icon__icon_url']
                        }
                        REPCOMENT.append(bb)
                    ss['replycomment'] = REPCOMENT
                    COMMENT.append(ss)
            # 返回获取到的评论信息
            return HttpResponse(json.dumps({"code": "234", "data": COMMENT}, ensure_ascii=False))
        else:
            # 434评论为空
            return JsonResponse({"code": "434"})
    except Exception as ex:
        print('this is GetGoodComment')
        print(ex)
        return JsonResponse({"code": "500"})

