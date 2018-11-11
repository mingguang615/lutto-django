from django.conf.urls import url
from django.urls import path
from .import views
app_name='course'
urlpatterns = [


    # path('getUserById/<str:myid>', views.getUserById, name='getUserById'),
    url(r'^$',views.index,name='index'),
    # 查询课程
    url(r'search/(?P<index>.*)/(?P<cname>.*)/',views.search,name='search'),
    # 首页显示课程
    url(r'getcourse/',views.getCourse,name='getCourse'),
    # 计算页码
    url(r'pageacount/(?P<con>.*)/',views.pagecount,name='pagecount'),
    # 课程首页
    url(r'getcoursefenlei/',views.getcoursefenlei,name='getcoursefenlei'),

    # 课程分类页
    url(r'getcoursebytypeid/(?P<index>.*)/(?P<tid>.*)/',views.getCourseByTypeid,name='getCourseByTypeid'),
    # 根据课程类型id计算页码
    url(r'pageacountbytid/(?P<con>.*)/',views.pagecountbytid,name='pagecount'),

    # 课程详情页 获取课程信息
    url(r'getcourseinfobyid/',views.getCourseInfoById,name='getCourseInfoById'),
    # 课程详情页 添加课程
    url(r'addcourse/', views.addCourse, name='addCourse'),
    # 课程详情页 获取课程包含动作信息
    url(r'getactionbycid/(?P<cid>.*)/',views.getActionByCid,name='getActionByCid'),
    # 课程详情页 获取课程评论信息
    url(r'getcoursecomment/',views.getCourseComment,name='getCourseComment'),
    # 课程详情页 获取热门课程评论信息
    url(r'gethotcoursecomment/',views.getHotCourseComment,name='getHotCourseComment'),
    #删除评论
    url(r'deloursecomment/',views.delCourseComment,name='delCourseComment'),
    #删除回复
    url(r'delcoursereply/',views.delCourseReply,name='delCourseReply'),
    # 课程详情页 回复评论信息
    url(r'replycomment/',views.replyComment,name='replyComment'),

]