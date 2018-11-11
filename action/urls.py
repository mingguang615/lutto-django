from django.conf.urls import url
from django.urls import path
from .import views
app_name='action'
urlpatterns = [


    # path('getUserById/<str:myid>', views.getUserById, name='getUserById'),
    url(r'^$',views.index,name='index'),
    # 搜索动作
    url(r'search/',views.search,name='search'),
    # 搜索动作计数
    url(r'acount/',views.Acount,name='Acount'),
    # 获取动作by动作id
    url(r'getaction/', views.getactionbyid, name='getactionbyid'),
    # 获取动作的所有等级
    url(r'getactionlevel/', views.getactionlevel, name='getactionlevel'),
    # 获取动作训练的所有肌肉
    url(r'getactionpart/', views.getactionpart, name='getactionpart'),
    # 获取训练动作所需所有器材
    url(r'getactionmachine/', views.getactionmachine, name='getactionmachine'),

]