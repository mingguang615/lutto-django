from django.db import models


# Create your models here.
# 课程等级
class CourseLevel(models.Model):
    level = models.CharField(max_length=50)


# class course_type(models.Model):
#     pass
# 课程训练身体部位
class BodyPart(models.Model):
    bodypart = models.CharField(max_length=50)


# 课程图片
class CoursePicture(models.Model):
    url = models.CharField(max_length=254, unique=True)


# 训练器材表
class Machine(models.Model):
    name = models.CharField(max_length=255)


# 课程类型表
class CourseType(models.Model):
    type_name = models.CharField(max_length=255)
    picture = models.ForeignKey(to='CoursePicture', to_field='id', on_delete=models.CASCADE)


# 课程表
class Course(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(to="CourseType", to_field="id", on_delete=models.CASCADE, default=1)
    picture = models.ForeignKey(to="CoursePicture", to_field="id", on_delete=models.CASCADE, default=1)
    level = models.ForeignKey(to="CourseLevel", to_field="id", on_delete=models.CASCADE, default=1)
    day = models.CharField(max_length=50, null=True)
    consume_total = models.CharField(max_length=50, null=True)
    machine = models.ForeignKey(to='Machine', to_field='id', on_delete=models.CASCADE, default=1)
    minute_avg = models.CharField(max_length=50, null=True)
    recipes = models.ForeignKey(to='recipes.RecipesPlan', to_field="id", on_delete=models.CASCADE, default=1)
    useraddcount = models.IntegerField(default=0)


# 课程训练身体部位中间表
class CourseTrainPart(models.Model):
    course = models.ForeignKey(to='Course', to_field='id', on_delete=models.CASCADE)
    bodypart = models.ForeignKey(to='BodyPart', to_field='id', on_delete=models.CASCADE)


# 课程点赞表
class CourseLike(models.Model):
    course = models.ForeignKey(to='Course', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)


# 课程评论表
class CourseComment(models.Model):
    course = models.ForeignKey(to='Course', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)


# 课程评论回复表
class CourseCommentReply(models.Model):
    comment = models.ForeignKey(to='CourseComment', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)  # 课程评论点赞表
    time = models.DateTimeField(auto_now_add=True)


class CourseCommentLike(models.Model):
    comment = models.ForeignKey(to='CourseComment', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)
