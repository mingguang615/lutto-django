from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
import json
from user import models
from utils.userlogin import *
from utils.token import *
from utils import token as toto
from qiniu import Auth, put_file, etag
import qiniu.config
import time
from collections import OrderedDict
import uuid
import random
from course import models as course_models
from shop import models as shop_models
# from datetime import datetime, timedelta
import datetime
from .miaodi import *
from course.models import CourseComment
from course.models import CourseCommentLike

def index(request):
    # return render(request,'user_index.html')
    return HttpResponse('i am index')


def getUserById(request, myid):
    # return HttpResponse('i am login'+myid)
    url = reverse('user:index', kwargs={"id": myid})
    # print(url)
    return redirect(url)


# 用户登陆
def login(request):
    if request.method == "POST":
        user = json.loads(request.body)
        # 调用登录方法
        res = login_ser(user)
        resp = JsonResponse(res)
        # print(res)
        if res['code'] == '201':
            token = makeToken(res['telephone'], res['user_id'])
            resp['token'] = token
            resp["Access-Control-Expose-Headers"] = "token"
            return resp
        else:
            print("this is login")
            return JsonResponse(res)


# 用户注册
def regist(request):
    if request.method == "POST":
        try:
            newuser = json.loads(request.body)
            # 调用注册方法
            res = regist_ser(newuser)
            if res and res['code'] == '203':
                resp = JsonResponse(res)
                token = makeToken(res['telephone'], res['id'])
                resp['token'] = token
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
            else:
                return JsonResponse(res, safe=False)
        except Exception as ex:
            print('this is regist')
            print(ex)
            return JsonResponse({"code": "500"})


# 修改密码
def changePassword(request):
    try:
        if request.method == "POST":
            user = json.loads(request.body)
            print(user)
            # 调用修改密码方法
            res = change_password(user)
            print(res)
            if res and res['code'] == '204':
                print(res)
                resp = JsonResponse(res)
                print(res)
                token = makeToken(res['id'], res['telephone'])
                print(token)
                resp['token'] = token
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
            else:
                return JsonResponse(res, safe=False)
    except Exception as ex:
        print('this is changePassword')
        print(ex)
        return JsonResponse({"code": "500"})


# 完善用户个人信息
def UpUser(request):
    try:
        if request.method == "POST":
            r = json.loads(request.body)
            token = r['headers']['token']
            res = toto.openToken(token)
            if res:
                user_id = res['user_id']
                ss = {
                    "name": r['name'],
                    "height": r['height'],
                    "width": r['width'],
                    "birth": r['birth'],
                    "sex_id": r['sex'],
                    "user_id": user_id,
                    "qinming": r['qianming']
                }
                # 先判断用户有没有基本信息，有就替换，没有用就直接添加
                res = models.UserInfo.objects.filter(user_id=user_id).values()
                if res:
                    models.UserInfo.objects.filter(user_id=user_id).update(**ss)
                else:
                    models.UserInfo.objects.create(**ss)
            else:
                return JsonResponse({"code": "411"})
        return JsonResponse({"code": "201"})
    except Exception as ex:
        print('this is UpUser')
        print(ex)
        return JsonResponse({"code": "500"})


# 添加用户地址
def UserAddress(request):
    if request.method == 'POST':
        try:
            address = json.loads(request.body)
            token = address['headers']['token']
            if token:
                res = openToken(token)
                print(res)
                if res:
                    user_id = res['user_id']
                    print(user_id)
                    ss = {
                        "user_id": user_id,
                        "province": address['province'],
                        "city": address['city'],
                        "area": address['area'],
                        "detailaddress": address['detailaddress'],
                        "telephone": address['telephone'],
                        "youbian": address['youbian'],
                        "recievename": address['recievename']
                    }
                    models.Address.objects.create(**ss)

                    return JsonResponse({"code": "202"})
                else:
                    return JsonResponse({"code": "411"})
            else:
                return JsonResponse({"code": "411"})
        except Exception as ex:
            print('this is UserAddress')
            print(ex)
            return JsonResponse({"code": "500"})


# 删除用户地址
def delAddress(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            # print(r)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                # 先检查有没有地址，没有返回413
                result = models.Address.objects.filter(id=r['id']).values_list()
                if result:
                    models.Address.objects.filter(id=r['id']).delete()
                    return JsonResponse({"code": "208"})
                else:
                    return JsonResponse({"code": "413"})
            else:
                return JsonResponse({"code": "411"})
        except Exception as ex:
            print('this is delAddress')
            print(ex)
            return JsonResponse({"code": "500"})


# 签到
def QianDao(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                qiandao = list(
                    models.UserInfo.objects.filter(user_id=res['user_id']).values('qiandaotime', 'qiandaodays'))
                dt = datetime.datetime.now().strftime("%Y-%m-%d")
                if qiandao[0]['qiandaotime']:
                    if qiandao[0]['qiandaotime'] == dt:
                        return JsonResponse({"code": "428"})
                    else:
                        models.UserInfo.objects.filter(user_id=res['user_id']).update(qiandaotime=dt,
                                                                                      qiandaodays=(qiandao[0][
                                                                                                       'qiandaodays'] + 1))
                        jf = list(models.Intergral.objects.filter(user_id=res['user_id']).values('intergral'))
                        jifen = jf[0]['intergral']
                        user_jifen = int(jifen) + 5
                        models.Intergral.objects.filter(user_id=res['user_id']).update(intergral=user_jifen)
                else:
                    # 如果未签到，将签到状态改为2 累计签到天数+1，并且给用户积分+5
                    models.UserInfo.objects.filter(user_id=res['user_id']).update(qiandaotime=dt,
                                                                                  qiandaodays=(qiandao[0][
                                                                                                   'qiandaodays'] + 1))
                    jf = list(models.Intergral.objects.filter(user_id=res['user_id']).values('intergral'))
                    jifen = jf[0]['intergral']
                    user_jifen = int(jifen) + 5
                    models.Intergral.objects.filter(user_id=res['user_id']).update(intergral=user_jifen)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "220"})
        except Exception as ex:
            print('this is QianDao')
            print(ex)
            return JsonResponse({"code": "500"})


# 用户确认收货
def ShouHuo(request):
    if request.method=='POST':
        try:
            r=json.loads(request.body)
            token=r['token']
            res=openToken(token)
            if res:
                order=list(shop_models.Order.objects.filter(user_id=res['user_id'],status=2,id=r['order_id']).values())
                if order:
                    shop_models.Order.objects.filter(user_id=res['user_id'],status=2,id=r['order_id']).update(status=3)
                else:
                    return JsonResponse({"code":"433"})
            else:
                return JsonResponse({"code":"411"})
            return JsonResponse({"code":"224"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code":"500"})



# 得到用户基本信息
def GetNameByTel(request):
    try:
        if request.method == "POST":
            r = json.loads(request.body)
            token = r['headers']['token']
            res = openToken(token)
            # import datetime
            # dt = datetime.datetime.now().strftime("%Y-%m-%d")
            if res:
                user_id = res['user_id']

                name = list(models.UserInfo.objects.filter(user_id=user_id).values('name', 'sex', 'height', 'width',
                                                                                   'icon__icon_url', 'birth', 'qinming',
                                                                                   'qiandaodays',
                                                                                   'user__intergral__intergral'))

                if name[0]['birth']:

                    from datetime import datetime
                    user_year = str(name[0]['birth']).split('-')[0]
                    now_year = str(datetime.now()).split('-')[0]
                    age = int(now_year) - int(user_year)
                else:
                    age = None
                userinfo = []
                ss = {
                    "name": name[0]['name'],
                    "sex": name[0]['sex'],
                    "height": name[0]['height'],
                    "width": name[0]['width'],
                    "icon_url": name[0]['icon__icon_url'],
                    "age": age,
                    "qianming": name[0]['qinming'],
                    "qiandaodays": name[0]['qiandaodays'],
                    "intergral": name[0]['user__intergral__intergral']
                }
                userinfo.append(ss)
                return HttpResponse(json.dumps(userinfo, ensure_ascii=False))
                # else:
                #     return JsonResponse({"code": "415"})
            else:
                return JsonResponse({"code": "411"})
    except Exception as ex:
        print('this is GetNameByTel')
        print(ex)
        return JsonResponse({"code": "500"})


# 查看用户地址
def GetAddress(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r['headers']['token']
            address = []  # 默认用户的地址为空
            if token:
                # 校验token
                res = openToken(token)
                if res:
                    # 根据用户id去查询用户添加的地址信息
                    address = list(models.Address.objects.filter(user_id=res['user_id']).values())
                    # 获取的地址为空时，返回错误代码419,用户为添加地址
                    if not address:
                        return JsonResponse({"code": "419"})
                else:
                    return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps({"code": "249", "data": address}, ensure_ascii=False))
        except Exception as ex:
            print('this is GetAddress')
            print(ex)
            return JsonResponse({"code": "500"})


# 七牛云token
def qiniuToken(request):
    try:
        r = request.GET.get('name')
        access_key = 'Ib28fQUwpKMw82G4NNw-TAdDooGGrRWOdadnuamM'
        secret_key = 'evfP2KZpTRrP3rqO39I7Sc5n18_QxCbvFgSuArxc'
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = 'lotto'
        # 上传到七牛后保存的文件名
        file = r
        key = str(uuid.uuid4()) + '.' + file.split('.')[-1]
        # 生成上传 Token，可以指定过期时间等 一天
        token = q.upload_token(bucket_name, key, 3600)
        return JsonResponse({"token": token, "filename": key})

    except Exception as ex:
        print('this is qiniuToken')
        print(ex)
        return JsonResponse({"code": "500"})


# 用户自定义更换头像
def randomIcon(request):
    allicon = models.Icon.objects.all().values_list('icon_url')
    # 随机数据库icon表中的用户头像
    usericon = list(allicon)[random.randint(0, len(allicon))][0]
    return JsonResponse({"userIcon": usericon})


# 用户上传头像（保存头像文件名称）（更改用户头像）
def upIcon(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            # print(r)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                ss = {
                    "icon_url": r['url']
                }
                # 将拿到的url存入数据库，并且获得的头像的id
                models.Icon.objects.create(**ss)
                urll = list(models.Icon.objects.filter(icon_url=r['url']).values('id'))
                url = urll[0]['id']
                # print(url)
                # 将用户信息表中得到头像id换成用户上传的url_id
                models.UserInfo.objects.filter(user_id=res['user_id']).update(icon_id=url)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "221"})
        except Exception as ex:
            print('this is upIcon')
            print(ex)
            return JsonResponse({"code": "500"})


def upload(requset):
    if requset.method == 'POST':
        try:
            user_id = requset.POST.get('userid')
            print(user_id)
            file = requset.FILES.get('usericon')
            fname = str(uuid.uuid4()) + '.' + file.name.split('.')[1]
            with open(fname, 'wb+') as fp:
                for c in file.chunks():
                    fp.write(c)
            return JsonResponse({"code": "200"})
        except Exception as ex:
            return JsonResponse({"code": "500"})


# 查询用户收藏的课程
def Getaction(request):
    if request.method == 'POST':
        try:
            courses = []
            r = json.loads(request.body)
            token = r['headers']['token']
            # 解析token
            res = openToken(token)
            # 判断能否解析token若解析失败返回411
            if res:
                user_id = res['user_id']
                # 根据用户id查询用户添加的课程id
                courseid = list(models.AddCourse.objects.filter(user_id=user_id).values('course_id'))
                # 判断能否找到课程id若找不到，返回466
                if courseid:
                    for i in range(len(courseid)):
                        course_id = courseid[i]['course_id']
                        # 通过课程id查询课程的详细信息
                        course = course_models.Course.objects.filter(id=course_id).values('name', 'level__level',
                                                                                          'picture__url',
                                                                                          'type__type_name',
                                                                                          'machine__name', 'id').first()
                        courses.append(course)
                else:
                    return JsonResponse({"code": "466"})
            else:
                return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps(courses, ensure_ascii=False))
        except Exception as ex:
            print('this is Getaction')
            print(ex)
            return JsonResponse({"code": "555"})





# 删除用户收藏的课程
def DelAction(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                user_id = res['user_id']
                # 根据用户id查询用户添加的课程
                course = list(models.AddCourse.objects.filter(user_id=user_id).values())
                # 判断能都找到对应的课程，若课程为空返回466
                if course:
                    # 根据用户id和对应的课程id删除对应的课程
                    models.AddCourse.objects.filter(user_id=user_id, course_id=r['id']).delete()
                    return JsonResponse({"code": "209"})
                else:
                    return JsonResponse({"code": "466"})
            else:
                return JsonResponse({"code": "411"})
        except Exception as ex:
            print('this is DelAction')
            print(ex)
            return JsonResponse({"code": 500})


# 添加评论
def addComment(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            content = data['content']
            course_id = int(data['cid'])
            data = data['headers']
            token = data['token']
            res = openToken(token)
            # result=models.AddCourse.objects.filter(course_id=course_id,user_id=res['user_id']).values()
            if res:
                addcomment = {
                    'course_id': course_id,
                    'user_id': res['user_id'],
                    'content': content,
                }
                course_models.CourseComment.objects.create(**addcomment)
                # print(res['user_id'])
                return JsonResponse({"code": "210"})
            else:
                return JsonResponse({"code": "没登陆"})

    except Exception as ex:
        print('this is addComment')
        print(ex)
        return JsonResponse({"code": "500"})


# 给评论点赞
def likeComment(request):
    try:
        # if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        commentid = int(data['commentid'])
        data = data['headers']
        token = data['token']
        res = toto.openToken(token)
        if res:
            result = course_models.CourseCommentLike.objects.filter(comment_id=commentid,
                                                                    user_id=res['user_id']).values()
            if result:
                course_models.CourseCommentLike.objects.filter(comment_id=commentid, user_id=res['user_id']).delete()
                likenum = course_models.CourseComment.objects.filter(id=commentid).values('likes')[0]['likes']
                res = likenum - 1
                course_models.CourseComment.objects.filter(id=commentid).update(likes=res)
                return JsonResponse({"code": "410"})
            else:
                addcomment = {
                    'comment_id': commentid,
                    'user_id': res['user_id'],
                }
                course_models.CourseCommentLike.objects.create(**addcomment)
                likenum = course_models.CourseComment.objects.filter(id=commentid).values('likes')[0]['likes']
                res = likenum + 1
                course_models.CourseComment.objects.filter(id=commentid).update(likes=res)

                return JsonResponse({"code": "210"})
        else:
            return JsonResponse({"code": "411"})
    except Exception as ex:
        print('this is likeComment')
        print(ex)
        return JsonResponse({"code": "500"})


# 收藏商品
def GetLove(request):
    if request.method == 'POST':
        try:
            goods = []
            r = json.loads(request.body)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                user_id = res['user_id']
                # print(user_id)
                # 根据用户id查询对应的收藏的商品
                love = list(shop_models.loveGood.objects.filter(user_id=user_id).values('good_id'))
                # print(love)
                # 判断能否找到收藏的商品，若找不到，返回421
                if love:
                    for i in range(len(love)):
                        good_id = love[i]['good_id']
                        # 根据商品id找到URL_size为1的第一张图片
                        good_url = list(
                            shop_models.GoodPicture.objects.filter(good_id=good_id, size=1).values('url', 'good_id',
                                                                                                   'good__name',
                                                                                                   'good__intergal'))
                        # 导入个模块，调用方法是字典可序化，具体什么原理我也不清楚，问伟哥
                        b = OrderedDict()
                        for item in good_url:
                            b.setdefault(item['good_id'], {**item, })
                        b = list(b.values())
                        ss = {
                            "good_id": b[0]['good_id'],
                            "good_name": b[0]['good__name'],
                            "good_intergal": b[0]['good__intergal'],
                            "good_url": b[0]['url']
                        }
                        goods.append(ss)
                else:
                    return JsonResponse({"code": "421"})
            else:
                return JsonResponse({"code": "411"})
            return HttpResponse(json.dumps(goods, ensure_ascii=False))
        except Exception as ex:
            print('this is GetLove')
            print(ex)
            return JsonResponse({"code": "500"})


# 删除收藏的商品
def DelLove(request):
    if request.method == 'POST':
        try:
            r = json.loads(request.body)
            token = r['headers']['token']
            good_id = r['good_id']
            res = openToken(token)
            if res:
                user_id = res['user_id']
                # 根据用户id和相应的商品id查找
                good = shop_models.loveGood.objects.filter(user_id=user_id, good_id=good_id).values()
                # 判断能否找到对应的商品，若不能返回422
                if good:
                    # 根据用户id和相应的商品id删除对应的数据
                    shop_models.loveGood.objects.filter(user_id=user_id, good_id=good_id).delete()
                else:
                    return JsonResponse({"code": "422"})
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "213"})
        except Exception as ex:
            print('this is DelLove')
            print(ex)
            return JsonResponse({"code": "500"})


# 验证验证码
def CheckCode(request):
    if request.method == "POST":
        try:
            r = json.loads(request.body)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                code = r['validate']
                # print(type(code))
                # print(code)
                telephone = r['telephone']
                now_time = time.time()
                # print(now_time)
                # 根据电话找验证码和发送验证码的时间
                cc = list(models.registertemp.objects.filter(telephone=telephone).values('expiretime', 'validate'))
                # print(cc)
                code_time = cc[0]['expiretime']
                CODE = cc[0]['validate']
                # print(type(CODE))
                print(CODE)
                print(now_time)
                print(code_time)
                # 比较发送验证码的时间错和当前时间戳，过期返回429
                if now_time > code_time:
                    return JsonResponse({"code": "429"})
                else:
                    if CODE == code:
                        # 验证成功，将用户的telephone 改成 验证的telephone
                        print(res['user_id'])
                        uu = models.User.objects.filter(id=res['user_id']).update(telephone=telephone)
                        if uu:
                            return JsonResponse({"code": "223", "telephone": telephone})
                        else:
                            return JsonResponse({"code": "431"})
                    else:
                        return JsonResponse({"code": "430"})

            else:
                return JsonResponse({"code": "411"})

        except Exception as ex:
            print('this is CheckCode')
            print(ex)
            return JsonResponse({"code": "500"})


# 发送验证码
def SendCode(request):
    if request.method == "POST":
        try:
            r = json.loads(request.body)
            # print(r)
            token = r['headers']['token']
            res = openToken(token)
            if res:
                telephone = r['telephone']
                print(telephone)
                # 生成随机的四位数
                c = random.randrange(1000, 9999)
                code = str(c)
                # 这个是秒滴里的信息模板
                smsContent = '【乐途运动】您的验证码为{0}，请于{1}分钟内正确输入，如非本人操作，请忽略此短信。'.format(code, 5)
                # 秒滴的一个方法
                sendIndustrySms(telephone, smsContent)
                # 存入数据库的时间加上过期时间
                now_date = (int(time.time()) + 300)
                print(time.time())
                print(now_date)
                telephone1 = list(models.registertemp.objects.filter(telephone=telephone).values())
                # print(telephone1)
                if telephone1:
                    # 如果之前数据库中有过该电话的数据，替换验证码
                    models.registertemp.objects.filter(telephone=telephone).update(validate=code, expiretime=now_date)
                else:
                    ss = {
                        "validate": code,
                        "expiretime": now_date,
                        "telephone": telephone
                    }
                    models.registertemp.objects.create(**ss)
            else:
                return JsonResponse({"code": "411"})
            return JsonResponse({"code": "222"})
        except Exception as ex:
            print('this is SendCode')
            print(ex)
            return JsonResponse({"code""500"})


# 查看用户地址
def GetUserAddress(request):
    if request.method == 'POST':
        try:
            address = []
            r = json.loads(request.body)
            token = r['token']
            res = openToken(token)
            if res:
                add = list(models.Address.objects.filter(user_id=res['user_id'], id=r['address_id']).values())
                ss = {
                    "address_id": add[0]['id'],
                    "province": add[0]['province'],
                    "city": add[0]['city'],
                    "area": add[0]['area'],
                    "detailaddress": add[0]['detailaddress'],
                    "recievename": add[0]['recievename'],
                    "telephone": add[0]['telephone'],
                    "youbian": add[0]['youbian']
                }
                print(ss)
                address.append(ss)
            else:
                return HttpResponse(json.dumps(address, ensure_ascii=False))
            return JsonResponse({"code": "200"})
        except Exception as ex:
            print('this is GetUserAddress')
            print(ex)
            return JsonResponse({"code": "500"})

    # 给课程添加评论


def addCourseComment(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            content = data['content']

            course_id = int(data['cid'])
            data = data['headers']
            token = data['token']
            res = openToken(token)
            if res:
                addcomment = {
                    'course_id': course_id,
                    'user_id': res['user_id'],
                    'content': content,
                    'time':datetime.datetime.now()
                }
                CourseComment.objects.create(**addcomment)
                return JsonResponse({"code": "210"})
            else:
                return JsonResponse({"code": "没登陆"})

    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "404"})

    # 给课程评论点赞


def likeCourseComment(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))

            # print('oooo')
            # print(data)
            commentid = int(data['commentid'])
            # print(commentid)

            # data = data['headers']
            token = data['headers']['token']

            # print(token)
            res = openToken(token)
            # print(res)
            if res:
                result = CourseCommentLike.objects.filter(comment_id=commentid, user_id=res['user_id']).values()
                if result:
                    CourseCommentLike.objects.filter(comment_id=commentid, user_id=res['user_id']).delete()
                    likenum = CourseComment.objects.filter(id=commentid).values('likes')[0]['likes']
                    res = likenum - 1
                    CourseComment.objects.filter(id=commentid).update(likes=res)
                    return JsonResponse({"code": "410"})
                else:
                    addcomment = {
                        'comment_id': commentid,
                        'user_id': res['user_id'],
                    }
                    CourseCommentLike.objects.create(**addcomment)
                    likenum = CourseComment.objects.filter(id=commentid).values('likes')[0]['likes']
                    res = likenum + 1
                    CourseComment.objects.filter(id=commentid).update(likes=res)

                    return JsonResponse({"code": "210"})
            else:
                return JsonResponse({"code": "没登陆"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": "404"})