from django.db import models


# 动作等级表
class ActionLevel(models.Model):
    level = models.CharField(max_length=50)


# 肌肉表
class Muscle(models.Model):
    name = models.CharField(max_length=50)


# # 动作表
class ActionLibrary(models.Model):
    name = models.CharField(max_length=50, unique=True)
    info = models.CharField(max_length=1000)
    level = models.ForeignKey(to='ActionLevel', to_field='id', on_delete=models.CASCADE)
    machine = models.ForeignKey(to='course.Machine', to_field='id', on_delete=models.CASCADE)
    times = models.CharField(max_length=50)
    muscle = models.ForeignKey(to='Muscle', to_field='id', on_delete=models.CASCADE)
    picture=models.ForeignKey(to='ActionPicture', to_field='id', on_delete=models.CASCADE,default=2)
    note1 = models.CharField(max_length=50, null=True)
    note2 = models.CharField(max_length=50, null=True)
    note3 = models.CharField(max_length=50, null=True)

#动作图片表
class ActionPicture(models.Model):
    url=models.CharField(max_length=255, unique=True)

# 动作要领图
class ActionYaolingtu(models.Model):
    url = models.CharField(max_length=255, unique=True)
    action = models.ForeignKey(to='ActionLibrary', to_field='id', on_delete=models.CASCADE)
    note1 = models.CharField(max_length=50, null=True)
    note2 = models.CharField(max_length=50, null=True)


# 动作肌肉图
class ActionMusclePicture(models.Model):
    url = models.CharField(max_length=255, unique=True)
    action = models.ForeignKey(to='ActionLibrary', to_field='id', on_delete=models.CASCADE)
    note1 = models.CharField(max_length=50, null=True)
    note2 = models.CharField(max_length=50, null=True)


# 课程动作中间表
class CourseAction(models.Model):
    action = models.ForeignKey(to='ActionLibrary', to_field='id', on_delete=models.CASCADE)
    course = models.ForeignKey(to='course.Course', to_field='id', on_delete=models.CASCADE)
    day_num = models.CharField(max_length=50, null=True)
