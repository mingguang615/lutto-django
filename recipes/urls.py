from django.conf.urls import url
from django.urls import path
from .import views
app_name='recipes'
urlpatterns = [


    # path('getUserById/<str:myid>', views.getUserById, name='getUserById'),
    url(r'^$',views.index,name='index'),
    url(r'search/',views.search,name='search'),
]