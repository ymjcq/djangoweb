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
    url(r'^deletecomment(?P<number>[0-9]+)/$',views.del_comment,name='delete_comment'),
    url(r'^changepwd/(?P<token>[a-z_A-Z-.+0-9]+)$',views.change_pwd,name='change_pwd'),
    url(r'^pwdemail/$',views.pwd_email,name='pwd_email'),
    url(r'^changeemail/$',views.change_email,name='change_email'),
	url(r'^showheat/$',views.show_heat,name='show_heat'),
	url(r'^showlast/$',views.show_last,name='show_last'),
	url(r'^confirm/(?P<token>[a-z_A-Z-.+0-9]+)/$',views.confirm,name='confirm'),
	url(r'^resendconfirm/$',views.resend_confirm,name='resend_confirm'),
    ]
    
    
