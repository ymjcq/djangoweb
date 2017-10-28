from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from .forms import LoginForm,EditProfileForm,PostForm,CommentForm,RegisterForm,PwdForm,PwdEmailForm,EmailChangeForm
from .models import Post,Comment,UserExtend
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# Create your views here.
#首页
def index(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))
            login(request,user)
            return redirect('user',username=user.username)
    elif request.method=='GET':
        form=LoginForm()
    show_heat=bool(request.COOKIES.get('show_heat',1))
    if show_heat:
        posts_list=Post.objects.all().order_by('-readcount')
    else:
        posts_list=Post.objects.all().order_by('-timestamp')
    paginator=Paginator(posts_list,10)
    page=request.GET.get('page')
    try:
        posts_page=paginator.page(page)
    except PageNotAnInteger:
        posts_page=paginator.page(1)
    except EmptyPage:
        posts_page=paginator.page(paginator.num_pages)
    return render(request,'usersysterm/index.html',{'form':form,'posts_page':posts_page,'show_heat':show_heat,})
#用户页面
def user(request,username):
    user=get_object_or_404(User,username=username)
    benren='false'
    following='false'
    if not request.user.is_anonymous():
        if request.user==user:
            benren='true'
        if request.user.userextend.is_following(user):
            following='true'
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=Post(title=form.cleaned_data['title'],body=form.cleaned_data['body'],author=user)
            post.save()
            return redirect('user',username=username)
    else:
        form=PostForm()
    show_followed=True
    if request.user.is_authenticated():
        show_followed=bool(request.COOKIES.get('show_followed',None))
#下次直接定义自己的User列表，这样太费内存了。
    if show_followed:
        followed_num=user.userextend.mingxing.all()
        posts=[]
        for i in followed_num:
            posts.extend(i.userlink.post_set.all())
    else:
        posts=Post.objects.filter(author=user)
    paginator=Paginator(posts,10)
    page=request.GET.get('page')
    try:
        posts_page=paginator.page(page)
    except PageNotAnInteger:
        posts_page=paginator.page(1)
    except EmptyPage:
        posts_page=paginator.page(paginator.num_pages)
    data={'user':user,'form':form,'posts_page':posts_page,
          'benren':benren,'following':following,
          'mingshu':user.userextend.mingxing.all().count(),
          'fenshu':user.userextend.fensi.all().count(),
          'show_followed':show_followed
          }
    return render(request,'usersysterm/user.html',data)
#普通用户编辑资料
@login_required
def edit_profile(request):
    current_user=request.user
    if request.method=='POST':
        form=EditProfileForm(request.POST,request.FILES)
        if form.is_valid():
            current_user.first_name=form.cleaned_data['first_name']
            current_user.last_name=form.cleaned_data['last_name']
            current_user.userextend.location=form.cleaned_data['location']
            current_user.userextend.about_me=form.cleaned_data['about_me']
            touxiang1=form.cleaned_data['touxiang']
            
            if touxiang1 is not None:
                current_user.userextend.touxiang=touxiang1
                current_user.userextend.touxiang_set=True
            current_user.save()
            return redirect('user',username=current_user.username)
    else:
        data={'first_name':current_user.first_name,
              'last_name':current_user.last_name,
              'location':current_user.userextend.location,
              'about_me':current_user.userextend.about_me}
        form=EditProfileForm(data)
    return render(request,'usersysterm/edit_profile.html',{'user':current_user,'form':form})
#编辑文章
@login_required
def edit_post(request,number):
    post=Post.objects.filter(id=number).first()
    current_user=request.user
    if current_user !=post.author:
        abort(403)
    if request.method =='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post.title=form.cleaned_data['title']
            post.body=form.cleaned_data['body']
            post.save()
            return redirect('user',username=current_user.username)
    else:
        data={'title':post.title,'body':post.body}
        form=PostForm(data)
    return render(request,'usersysterm/edit_post.html',{'form':form,'post':post,'current_user':current_user})
#删除文章
@login_required
def delete_post(request,number):
    post=Post.objects.filter(id=number).first()
    if request.user==post.author:
        post.delete()
    return redirect('user',username=request.user.username)

#关注的实现
@login_required
def follow(request,username):
    user=User.objects.filter(username=username).first()
    current_user=request.user
    if user is None:
        messages.add_message(request,messages.INFO,'用户不存在')
    if current_user.userextend.is_following(user):
        return redirect('user',username=current_user.username)
    current_user.userextend.follow(user)
    return redirect('user',username=username)
#取消关注的实现
@login_required
def unfollow(request,username):
    user=User.objects.filter(username=username).first()
    current_user=request.user
    if user is None:
        messages.add_message(request,messages.ERROR,'用户不存在')
    if not current_user.userextend.is_following(user):
        return redirect('user',username=current_user.username)
    current_user.userextend.unfollow(user)
    return redirect('user',username=username)
#粉丝视图
def followers(request,username):
    user=User.objects.get(username=username)
    current_user=request.user
    following='false'
    benren='false'
    followed='false'
    if user is None:
        messages.add_message(request,messages.ERROR,'用户不存在')
        return redirect('index',username=request.user.username)
    if not current_user.is_anonymous():
        if current_user == user:
            benren='true'
        if current_user.userextend.is_following(user):
            following='true'
        if user.userextend.is_following(current_user):
            followed='true'
    follower_list=user.userextend.fensi.all()
    paginator=Paginator(follower_list,10)
    page=request.GET.get('page')
    try:
        follower_page=paginator.page(page)
    except PageNotAnInteger:
        follower_page=paginator.page(1)
    except EmptyPage:
        follower_page=paginator.page(paginator.num_pages)
    data={'user':user,'current_user':current_user,'follower_page':follower_page,
          'following':following,'benren':benren,'mingcount':user.userextend.mingxing.all().count(),
          'fencount':user.userextend.fensi.all().count()}
    return render(request,'usersysterm/follower.html',data)
#关注视图
def followed_by(request,username):
    user=User.objects.get(username=username)
    current_user=request.user
    following='false'
    benren='false'
    followed='false'
    if user is None:
        messages.add_message(request,messages.ERROR,'用户不存在')
        return redirect('index',username=request.user.username)
    if not current_user.is_anonymous():
        if current_user == user:
            benren='true'
        if current_user.userextend.is_following(user):
            following='true'
        if user.userextend.is_following(current_user):
            followed='true'
    followed_list=user.userextend.mingxing.all()
    paginator=Paginator(followed_list,10)
    page=request.GET.get('page')
    try:
        followed_page=paginator.page(page)
    except PageNotAnInteger:
        followed_page=paginator.page(1)
    except EmptyPage:
        followed_page=paginator.page(paginator.num_pages)
    data={'user':user,'current_user':current_user,'followed_page':followed_page,
          'following':following,'benren':benren,'mingcount':user.userextend.mingxing.all().count(),
          'fencount':user.userextend.fensi.all().count()}
    return render(request,'usersysterm/followed.html',data)
#用户页查看所有的文章
@login_required
def show_self(request):
    resp=HttpResponseRedirect(reverse('user',args=[request.user.username]))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp
#用户页查看关注的文章
@login_required
def show_followed(request):
    resp=HttpResponseRedirect(reverse('user',args=[request.user.username]))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp
#首页最热文章
def show_heat(request):
    resp=HttpResponseRedirect(reverse('index'))
    resp.set_cookie('show_heat','1',max_age=30*24*60*60)
    return resp
#首页最新文章
def show_last(request):
    resp=HttpResponseRedirect(reverse('index'))
    resp.set_cookie('show_heat','',max_age=30*24*60*60)
    return resp
#文章的固定链接
def post(request,number):
    post=Post.objects.filter(id=number).first()
    current_user=request.user
    following='false'
    followed='false'
    post.readcount+=1
    post.save()
    if not current_user.is_anonymous():
        if current_user.userextend.is_following(post.author):
            following='true'
        if post.author.userextend.is_following(current_user):
            followed='true'
    if request.method =='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=Comment.objects.create(body=form.cleaned_data['body'],post=post,author=request.user)
            comment.save()
            return redirect('post',number=post.id)
    else:
        form=CommentForm()
    comment_list=post.comment_set.all()
    paginator=Paginator(comment_list,10)
    page=request.GET.get('page')
    try:
        comment_page=paginator.page(page)
    except PageNotAnInteger:
        comment_page=paginator.page(1)
    except EmptyPage:
        comment_page=paginator.page(paginator.num_pages)
    data={'post':post,'form':form,'comment_page':comment_page,
          'current_user':current_user,'following':following,'followed':followed,
          'mingcount':post.author.userextend.mingxing.all().count(),
          'fencount':post.author.userextend.fensi.all().count()}
    return render(request,'usersysterm/post.html',data)
#发送邮件辅助函数,并非视图函数
def send_help_email(toemail,token):
    url1=reverse('confirm',args=[token])
    confirmurl="127.0.0.1:8000"+url1
    msg='<h3>欢迎加入学习笔记</h3><p>请您复制打开下面的连接确认邮箱，激活账户!</p><p>%s</p>' % confirmurl
    send_mail('请您确认邮件','',settings.EMAIL_FROM,[toemail],html_message=msg)
#发送密码改动邮件,不是视图函数。
def send_pwd_email(toemail,token):
    url1=reverse('change_pwd',args=[token])
    confirmurl="127.0.0.1:8000"+url1
    msg='<h3>更改密码</h3><p>请您复制打开下面的连接，修改密码！</p><p>%s</p>' % confirmurl
    send_mail('更改密码','',settings.EMAIL_FROM,[toemail],html_message=msg)
#注册用户
def register(request):
    if request.method =='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            s=User.objects.create_user(username=form.cleaned_data['username'],
                                      email=form.cleaned_data['email'],
                                      password=form.cleaned_data['password'])
            s.save()
            s.userextend.follow(s)
            user=authenticate(username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))
            token=user.userextend.generate_confirmation_token()
            send_help_email('2313064696@qq.com',token)
            messages.success(request,'一封确认邮件已发往您的邮箱!请您一个小时内确认。')
            login(request,user)
            return redirect('user',username=form.cleaned_data['username'])
    elif request.method =='GET':
        form=RegisterForm()
    posts_page=Post.objects.all()[:15]
    return render(request,'usersysterm/register.html',{'form':form,'posts_page':posts_page})

#确认用户账户
@login_required
def confirm(request,token):
    if request.user.userextend.confirmed:
	    return redirect('user',username=request.user.username)
    if request.user.userextend.confirm(token):
        messages.success(request,'您已成功激活了账户！')
    else:
        messages.error(request,'确认邮件已过期，请您重新发送确认邮件！')
    return redirect('user',username=request.user.username)
#重新发送邮件
@login_required
def resend_confirm(request):
    token=request.user.userextend.generate_confirmation_token()
    send_help_email('2313064696@qq.com',token)
    messages.success(request,'一封确认邮件已经发往您的邮箱，请您一个小时内确认。')
    return redirect('user',username=request.user.username)
	
#退出登录
@login_required
def log_out(request):
    logout(request)
    return redirect('index')
#删除评论
@login_required
def del_comment(request,number):
    comment=Comment.objects.filter(id=number).first()
    post=comment.post
    if request.user == post.author or  request.user == comment.author:
        comment.delete()
    return redirect('post',post.id)
#修改密码
def change_pwd(request,token):
    
    if request.method == 'POST':
        s=Serializer(settings.SECRET_KEY)
        data=s.loads(token)
        id=data.get('confirm')
        current_user=User.objects.filter(pk=id).first()
        form=PwdForm(request.POST)
        if form.is_valid():
            if current_user.check_password(form.cleaned_data.get('password2')):
                messages.error(request,'与原密码相同，请重新输入.')
                return redirect('change_pwd')
            current_user.set_password(form.cleaned_data.get('password2'))
            current_user.save()
            user=authenticate(username=current_user.username,password=form.cleaned_data.get('password2'))
            login(request,user)
            messages.success(request,'密码更改成功!')
            return redirect('user',username=current_user.username)
    else:
        form=PwdForm()
    return render(request,'usersysterm/change_pwd.html',{'form':form,'token':token})

#向邮箱发修改密码指令
def pwd_email(request):
    if request.method =='POST':
        form=PwdEmailForm(request.POST);
        if form.is_valid():
            current_user=User.objects.filter(email=form.cleaned_data.get('email')).first()
            if current_user and current_user.userextend.confirmed:
                token=current_user.userextend.generate_confirmation_token()
                send_pwd_email('2313064696@qq.com',token)
                messages.success(request,'请到您的邮箱打开连接更改密码。')
                return render(request,'usersysterm/pwd_email.html',{'form':form})
            else:
                messages.error(request,'没有用户使用该邮箱！或者该邮箱没有激活，请您重新输入。')
                return render(request,'usersysterm/pwd_email.html',{'form':form})
    else:
        form=PwdEmailForm()
    return render(request,'usersysterm/pwd_email.html',{'form':form})
#修改邮箱 
@login_required
def change_email(request):
    if request.method =='POST':
        form=EmailChangeForm(request.POST)
        if form.is_valid():
            request.user.userextend.confirmed=False
            request.user.email=form.cleaned_data.get('email2')
            request.user.save()
            token=request.user.userextend.generate_confirmation_token()
            send_help_email('2313064696@qq.com',token)
            messages.success(request,'一封激活邮箱的邮件已发往您的邮箱')
            return redirect('user',username=request.user.username)
    else:
        form=EmailChangeForm()
    return render(request,'usersysterm/change_email.html',{'form':form})
#定义错误页面
def page_not_found(request):
	return render_to_response('usersysterm/404.html')

def page_error(request):
	return render_to_response('usersysterm/500.html')
        
    
    
        
    
        
    
            
            
            
