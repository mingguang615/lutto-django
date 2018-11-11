from user import models
import datetime
from utils.mimi import *
from utils.token import *


# from django.http import /, response, JsonResponse


def login_ser(user):
    print('this is utils login_ser')
    try:
        userpassword = list(
            models.User.objects.filter(telephone=user['telephone']).values('password', 'id', 'telephone'))
        if len(userpassword) == 0:
            result = {"code": "405"}  # 用户不存在
        elif jiemi(user['password'], userpassword[0]['password']):

            result = {
                'code': '201',
                'user_id': userpassword[0]['id'],
                'telephone': userpassword[0]['telephone']
            }
        else:
            result = {'code': '402'}  # 密码错误
    except Exception as ex:
        result = {
            'code': '500'
        }
    return result


def regist_ser(newuser):
    print('this is utils regist_ser')
    try:
        telephone = newuser['telephone']
        password = newuser['password']
        passwords = newuser['passwords']

        if password == passwords:
            user = models.User.objects.filter(telephone=newuser['telephone']).values()

            if len(user):
                return {'code': '408'}  # 该用户已存在
            else:
                import datetime
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user = {
                    "telephone": telephone,
                    "password": jiami(password),
                    "regist_time": dt
                }
                res = models.User.objects.create(**user)
                id = models.User.objects.filter(telephone=telephone).values('id')
                ss = {
                    "intergral": 0,
                    "user_id": id[0]['id']
                }
                models.Intergral.objects.create(**ss)
                bb = {
                    "user_id": id[0]['id'],
                    "icon_id": 1
                }
                models.UserInfo.objects.create(**bb)
                if res:

                    return {'code': '203', 'id': id[0]['id'], 'telephone': user['telephone']}
                else:
                    return {'code': '500'}  # 代码错了傻屌
        else:
            return {'code': '407'}  # 两次密码不一致

    except Exception as ex:
        print(ex)


def change_password(user):
    print('this is utils changepassword')
    try:
        token = user['headers']['token']
        newpassword = user['password']
        r = openToken(token)
        if r:
            user_id = r['user_id']
            password = models.User.objects.filter(id=user_id).values('password', 'telephone')
            old_password = password[0]['password']
            tel = password[0]['telephone']
            if jiemi(newpassword, old_password):
                return {"code": "409"}
            else:
                res = models.User.objects.filter(id=user_id).update(password=jiami(newpassword))
                return {
                    "code": "204",
                    "id": user_id,
                    "telephone": tel
                }
        else:
            return {"code": 411}
    except Exception as ex:
        return {"code": "500"}
