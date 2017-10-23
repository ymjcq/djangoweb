from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

#用户信息
class UserExtend(models.Model):
    #用户登录信息
    userlink=models.OneToOneField(User,on_delete=models.CASCADE)
    #用户真实信息
    location=models.CharField(max_length=100)
    about_me=models.TextField()
    touxiang=models.ImageField(upload_to="photo",null=True,blank=True,)
    touxiang_set=models.BooleanField(default=False)
    mingxing=models.ManyToManyField('self',through='Follow',symmetrical=False,related_name='fensi')
    


    #关注
    def follow(self,user):
        if not self.is_following(user):
            f=Follow.objects.create(follower=self,followed=user.userextend)
            f.save()
    #取消关注
    def unfollow(self,user):
        f=self.followed_set.filter(followed=user.userextend)
        f.delete()
    #正在关注
    def is_following(self,user):
        if self.followed_set.filter(followed=user.userextend):
            return True
        else:
            return False
    #被关注
    def is_followed_by(self,user):
        if self.follower_set.all().filter(follower=user.userextend):
            return True
        else:
            return False
   

    #获取关注人的文章或观点
    @property
    def followed_posts(self):
        return Post.objects.filter(author==self.user.followed_set,user__follower_set=self.user)
    def __str__(self):
        return self.userlink.username
#Users实例被创建时 UserExtend 同步被创建
@receiver(post_save,sender=User)
def create_user_extend(sender,instance,created,**kwargs):
    if created:
        UserExtend.objects.create(userlink=instance)
@receiver(post_save,sender=User)
def save_user_extend(sender,instance,**kwargs):
    instance.userextend.save()
#关注与粉丝关系表
class Follow(models.Model):
    follower=models.ForeignKey(UserExtend,related_name='followed_set')
    followed=models.ForeignKey(UserExtend,related_name='follower_set')
    timestamp=models.DateTimeField(default=datetime.utcnow())

    def __str__(self):
        return '%s follow %s'%(self.follower.userlink.username,self.followed.userlink.username)

#文章信息
class Post(models.Model):
    title=models.CharField(max_length=100)
    body=models.TextField()
    timestamp=models.DateTimeField(default=datetime.utcnow)
    author=models.ForeignKey(User)
    readcount=models.IntegerField(default=0)
    class Meta:
        verbose_name=u"文章"
    
#评论信息
class Comment(models.Model):
    body=models.TextField()
    timestamp=models.DateTimeField(default=datetime.utcnow())
    post=models.ForeignKey(Post)
    author=models.ForeignKey(User)
