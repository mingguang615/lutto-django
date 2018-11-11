from django.db import models


# Create your models here.
class User(models.Model):
    telephone = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    regist_time = models.DateTimeField(auto_now_add=True)
    # icon=models.CharField(max_length=50,default='user.png')


class Sex(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=255,null=True)


class Icon(models.Model):
    icon_url = models.CharField(max_length=254)

class UserInfo(models.Model):
    name = models.CharField(max_length=50, null=True)
    icon=models.ForeignKey(to='Icon',to_field='id',on_delete=models.CASCADE,default=1)
    height = models.CharField(max_length=50,null=True)
    width = models.CharField(max_length=50, null=True)
    birth = models.DateField( null=True)
    note1 = models.CharField(max_length=50, null=True)
    note2 = models.CharField(max_length=50, null=True)
    sex = models.ForeignKey(to='Sex',to_field='id',on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE,default=1)
    qinming=models.CharField(max_length=50, null=True)
    qiandaodays=models.IntegerField(default=0,null=True)
    qiandaotime=models.CharField(max_length=50,null=True)


class Intergral(models.Model):
    user=models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE)
    intergral = models.CharField(max_length=50)

class Address(models.Model):
    province=models.CharField(max_length=50,null=True)
    city=models.CharField(max_length=50,null=True)
    area=models.CharField(max_length=50,null=True)
    detailaddress=models.CharField(max_length=50,null=True)
    user=models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE)
    recievename=models.CharField(max_length=50,null=True)
    telephone=models.CharField(max_length=50,null=True)
    youbian=models.CharField(max_length=50,null=True)


class AddCourse(models.Model):
    course=models.ForeignKey(to='course.Course',to_field='id',on_delete=models.CASCADE)
    user=models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE)

# 购物车表
class AddGood(models.Model):
    good = models.ForeignKey(to='shop.Goods', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    num=models.IntegerField(default=0)
    checked=models.CharField(max_length=20,null=True)


# 用户注册暂存信息
class registertemp(models.Model):
    telephone = models.CharField(max_length=20)
    validate = models.CharField(max_length=20)
    expiretime = models.BigIntegerField()
