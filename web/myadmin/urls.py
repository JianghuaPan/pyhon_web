from django.conf.urls import url,include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$',views.index,name='myhome_index'),
    #添加
    url(r'^user/add/$',views.useradd,name='myadmin_user_add'),
    url(r'^user/list/$',views.userlist,name='mydamin_user_list'),
    url(r'^user/del/([0-9]+)/$',views.userdel,name='mydamin_user_del'),
    url(r'^user/edit/([0-9]+)/$', views.useredit,name="myadmin_user_edit"),

]