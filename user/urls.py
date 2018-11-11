from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    # 登陆
    url(r'login/', views.login, name='login'),
    # 注册
    url(r'regist/', views.regist, name='regist'),

    # path('getUserById/<str:myid>', views.getUserById, name='getUserById'),
    url(r'^getUser\w*/(?P<myid>\d+)', views.getUserById, name='getUserById'),
    url(r'^$', views.index, name='index'),
    url(r'change/', views.changePassword, name='changePassword'),
    # url(r'chuserinfo/',views.ChangeUserInfo,name='ChangeUserInfo'),
    url(r'upuser/', views.UpUser, name='UpUser'),
    url(r'useraddress/', views.UserAddress, name='UserAddress'),
    url(r'deladdress/', views.delAddress, name='delAddress'),
    url(r'getuserinfobytel/', views.GetNameByTel, name='GetNameByTel'),
    url(r'getaddress/', views.GetAddress, name='GetAddress'),
    url(r'upload/', views.upload, name='upload'),
    # 七牛云
    url(r'qiniutoken/', views.qiniuToken, name='qiniuToken'),
    url(r'getaction/', views.Getaction, name='Getaction'),
    url(r'delaction/', views.DelAction, name='DelAction'),

    url(r'getlove/', views.GetLove, name='GetLove'),

    url(r'dellove/', views.DelLove, name='DelLove'),
    # 用户签到获取积分接口
    url(r'qiandao/', views.QianDao, name='QianDao'),
    url(r'upicon/', views.upIcon, name='upIcon'),
    url(r'sendcode/', views.SendCode, name='SendCode'),
    url(r'checkcode/', views.CheckCode, name='CheckCode'),

    url(r'gettadd/', views.GetUserAddress, name='GetUserAddress'),
    # 用户确认收货
    url(r'shouhuo/', views.ShouHuo, name='ShouHuo'),

    # 给课程添加评论
    url(r'addcoursecomment/', views.addCourseComment, name='addCourseComment'),
    # 给评论点赞
    url(r'likecoursecomment/', views.likeCourseComment, name='likeCourseComment'),
    # url(r'getlove/', views.GetLoveGood, name='GetLoveGood'),
]
