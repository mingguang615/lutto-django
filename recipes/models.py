from django.db import models


# Create your models here.
# 食物类型表
class FoodType(models.Model):
    name = models.CharField(max_length=50)


# 食物表
class Food(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(to='FoodType', to_field='id', on_delete=models.CASCADE)


# 饮食计划表
class RecipesPlan(models.Model):
    name = models.CharField(max_length=50)
    calorie = models.CharField(max_length=50)
    breakfast = models.CharField(max_length=50, null=True)
    lunch = models.CharField(max_length=50, null=True)
    dinner = models.CharField(max_length=50, null=True)
    info = models.CharField(max_length=255)
    note1 = models.CharField(max_length=50, null=True)
    note2 = models.CharField(max_length=50, null=True)


# 饮食计划，食物，食物类型中间表
class RecipesFood(models.Model):
    plan = models.ForeignKey(to='RecipesPlan', to_field='id', on_delete=models.CASCADE)
    food = models.ForeignKey(to='Food', to_field='id', on_delete=models.CASCADE)
    type = models.ForeignKey(to='FoodType', to_field='id', on_delete=models.CASCADE)
