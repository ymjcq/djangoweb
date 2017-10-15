from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$',views.user,name='user'),
    url(r'^editprofile/$',views.edit_profile,name='edit_profile'),
    url(r'^editpost/(?P<number>[0-9]+)/$',views.edit_post,name='edit_post'),
    url(r'^deletepost/(?P<number>[0-9]+)/$',views.delete_post,name='delete_post'),
    url(r'^follow/(?P<username>[A-Za-z0-9]+)/$',views.follow,name='follow'),
    url(r'^unfollow/(?P<username>[A-Za-z0-9]+)/$',views.unfollow,name='unfollow'),
    url(r'^followers/(?P<username>[A-Za-z0-9]+)/$',views.followers,name='followers'),
    url(r'^followed/(?P<username>[A-Za-z0-9]+)/$',views.followed_by,name='followed_by'),
    url(r'^post/(?P<number>[0-9]+)/$',views.post,name='post'),
    url(r'^register/$',views.register,name='register'),
    url(r'^showfollowed/$',views.show_followed,name='show_followed'),
    url(r'^showself/$',views.show_self,name='show_self'),
    url(r'^logout/$',views.log_out,name='log_out'),
    url(r'^deletecomment(?P<number>[0-9]+)/$',views.del_comment,name='del_comment'),
    url(r'^changepwd/$',views.change_pwd,name='change_pwd'),
    ]
    
    
