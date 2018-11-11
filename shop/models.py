from django.db import models


# Create your models here.
class GoodBrand(models.Model):
    name = models.CharField(max_length=50)


class GoodClass(models.Model):
    name = models.CharField(max_length=50)


class Goods(models.Model):
    name = models.CharField(max_length=300)
    intergal = models.CharField(max_length=50)
    goodbrand = models.ForeignKey(to='GoodBrand', to_field='id', on_delete=models.CASCADE)
    goodclass = models.ForeignKey(to='GoodClass', to_field='id', on_delete=models.CASCADE)
    gooddesc = models.CharField(max_length=500, null=True)
    kucun = models.CharField(max_length=50, null=True)


class GoodPicture(models.Model):
    url = models.CharField(max_length=255)
    good = models.ForeignKey(to='Goods', to_field='id', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, null=True)


class GoodComment(models.Model):
    content = models.CharField(max_length=1000)
    good = models.ForeignKey(to='Goods', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)
    firscomment = models.CharField(max_length=500, null=True)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)


# 用户收藏商品表
class loveGood(models.Model):
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)
    good = models.ForeignKey(to='Goods', to_field='id', on_delete=models.CASCADE)


# 订单表
class Order(models.Model):
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)
    good = models.ForeignKey(to='Goods', to_field='id', on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    goodcounts = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    addressid=models.IntegerField(null=True)


# 商品评论点赞表
class ShopCommentLike(models.Model):
    comment = models.ForeignKey(to='GoodComment', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)


# 商品评论回复表
class ShopCommentReply(models.Model):
    comment = models.ForeignKey(to='GoodComment', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)  # 课程评论点赞表
    time = models.DateTimeField(auto_now_add=True)
