# from django.conf.urls import url
# from django.urls import path
# from .import views
# app_name='shop'
# urlpatterns = [
#
#
#     # path('getUserById/<str:myid>', views.getUserById, name='getUserById'),
#     url(r'^$',views.index,name='index'),
#     url(r'search/',views.search,name='search'),
#     url(r'getgoods/',views.getGoodById,name='getGoodById'),
#     url(r'goods/',views.GoodIndex,name='GoodIndex'),
# ]
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    # path('getUserById/<str:myid>', views.getUserById, name='getUserById'),
    url(r'^$', views.index, name='index'),
    # 商城搜索路由
    url(r'search/', views.search, name='search'),
    # 获取商品详情（商品详情页）
    url(r'getgoods/', views.getGoodById, name='getGoodById'),
    # 获取商城的商品信息
    url(r'goods/', views.GoodIndex, name='GoodIndex'),
    # 添加商品到购物车路由
    url(r'addgood/', views.addGoodToCar, name='addGoodToCar'),
    # 删除购物车的商品
    url(r'delgood/', views.delGood, name='delGood'),
    # 商城分页接口
    url(r'account/', views.account, name='account'),
    # 更新用户购物车中的商品数量
    url(r'upgoodnum/', views.updataGoodNum, name='updataGoodNum'),
    # 立即评价商品接口
    url(r'goodcomment/', views.GoodComment, name='GoodComment'),
    # 获取商品评论
    url(r'getcomment/', views.GetGoodComment, name='GetGoodComment'),
    # 删除评论
    url(r'delcomment/', views.DelComment, name='DelComment'),
    # 收藏商品
    url(r'lovegood/', views.LoveGood, name='LoveGood'),
    # 获取用户购物车中的商品信息
    url(r'getcart/', views.GetCart, name='getcart'),
    # 更新商品选中状态信息
    url(r'updatacart/', views.updataCart, name='updatacart'),
    # 生成订单
    url(r'makeorder/', views.OrderGood, name='OrderGood'),
    # 获取订单ID
    url(r'getorderbyid/', views.GetOrderById, name='GetOrderById'),
    # 用户购买商品完成交易
    url(r'dealorder/', views.DealOrder, name='DealOrder'),
    # 删除订单
    url(r'delorder/', views.DelOrder, name='DelOrder'),
    # 查看我的订单（商品）(个人中心)
    url(r'gettorder/', views.GetOrder, name='GetOrder'),
    # 获取订单id
    url(r'getorderbyid/', views.GetOrderById, name='GetOrderById'),
    # 获取用户所有的订单id
    url(r'getallorder/', views.GetAllOrder, name='GetAllOrder'),
    # 商品回复
    url(r'shopreply/', views.ShopReply, name='ShopReply'),

    url(r'likecomment/', views.likeComment, name='likeComment'),

]
