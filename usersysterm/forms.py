from .models import UserExtend,Post,Comment
from django import forms
from django.forms import widgets,fields
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
#建立用户表格
class LoginForm(forms.Form):
    username=fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'用户名'}),
        label='用户名',
        max_length=12,
        min_length=6,
        error_messages={'required':'用户名不为空'}
        )
    password=fields.CharField(
        required=True,
        widget=widgets.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}),
        min_length=6,
        max_length=12,
        label='密码',
        error_messages={'required':'密码不能为空',
                        'min_length':'用户名最少为6个字符',
                        'max_length':'用户名不超过12个字符',},
        )
    
    def clean(self):
        username=self.cleaned_data.get('username')
        pwd=self.cleaned_data.get('password')
        user=User.objects.filter(username=username).first()
        if username and pwd:
            if not user:
                raise ValidationError('用户不存在！')
            if not user.check_password(pwd):
                raise ValidationError('用户或者密码错误！')
#普通用户的资料编辑表单
class EditProfileForm(forms.Form):
    first_name=forms.CharField(
        required=False,
        label='姓氏',
        max_length=4,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'姓氏'}),
        error_messages={'max_length':'不超过4个字符'})
    last_name=forms.CharField(
        required=False,
        label='名字',
        max_length=10,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'名字'}),
        error_messages={'max_length':'不超过10个字符'})
    location=forms.CharField(
        required=False,
        label='地区',
        max_length=50,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'所在城市'}),
        error_messages={'max_length':'不超过50个字符'})
    about_me=forms.CharField(
        required=False,
        label='自我介绍',
        max_length=100,
        widget=widgets.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'介绍一下自己吧'},),
        error_messages={'max_length':'不超过100个字符'})
    touxiang=forms.ImageField(
        label='设置头像',
        required=False,)
#博客文章表单
class PostForm(forms.Form):
    title=forms.CharField(
        label='标题',
        max_length=100,
        required=True,
        min_length=2,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'文章标题'}),
        error_messages={'max_length':'不超过100个字符',
                        'min_length':'不少于2个字符',
                        'required':'标题必填'})
    body=forms.CharField(
        label='正文',
        widget=widgets.Textarea(attrs={'class':'form-control','rows':4,'placeholder':'文章正文',}),)
        
#评论表单
class CommentForm(forms.Form):
    body=forms.CharField(
        max_length='100',
        label='评论',
        error_messages={'max_length':'不超过100个字符',},
        widget=widgets.TextInput(attrs={'class':'form-control'}))

#注册表单
class RegisterForm(forms.Form):
    username=fields.CharField(
        label='用户名',
        max_length=12,
        min_length=6,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'用户名（6-12字符）'}),
        error_messages={'required':'标题不能为空',
                       'min_length':'用户名最少为6个字符',
                       'max_length':'用户名不超过12个字符'},)
    email=fields.EmailField(
        label='邮箱',
        required=True,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}),
        error_messages={'required':'邮箱不能为空',
                        'invalid':'请输入正确的邮箱格式'},)
    password=fields.CharField(
        label='密码',
        widget=widgets.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码,必须包含数字，字母'},render_value=True),
        required=True,
        min_length=6,
        max_length=12,
        validators=[
            RegexValidator(r'((?=.*\d))^.{6,12}$','必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$','必须包含字母'),],
        error_messages={'required':'密码不能为空！',
                        'min_length':'密码最少为6个字符',
                        'max_length':'密码不超过12个字符',},)
    pwd_again=fields.CharField(
        widget=widgets.PasswordInput(attrs={'class':'form-control','placeholder':'请再次输入密码！'},render_value=True),
        required=True,
        label='确认密码',
        error_messages={'required':'请再次输入密码',},
        )
    #查看用户名是否被注册
    def clean_username(self):
        username=self.cleaned_data['username']
        users=User.objects.filter(username=username).count()
        if users:
            raise ValidationError('该用户名已经被使用！')
        return username
    #查看邮箱是否被注册
    def clean_email(self):
        email=self.cleaned_data['email']
        email_count=User.objects.filter(email=email).count()
        if email_count:
            raise ValidationError('该邮箱已注册！')
        return email
    #检查输入两次密码是否一致
    def _clean_new_password2(self):
        password2=self.cleaned_data.get('pwd_again')
        password1=self.cleaned_data.get('password')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('两次密码不一致！')
    def clean(self):
        self._clean_new_password2()

#更改密码表单
class PwdForm(forms.Form):
    username=fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'用户名'}),
        label='用户名',
        max_length=12,
        min_length=6,
        error_messages={'required':'用户名不为空'}
        )
    password=fields.CharField(
        required=True,
        widget=widgets.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}),
        min_length=6,
        max_length=12,
        label='原密码',
        error_messages={'required':'密码不能为空',
                        'min_length':'用户名最少为6个字符',
                        'max_length':'用户名不超过12个字符',},
        )
    password2=fields.CharField(
        required=True,
        widget=widgets.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新密码'}),
        min_length=6,
        max_length=12,
        label='新密码',
        validators=[
            RegexValidator(r'((?=.*\d))^.{6,12}$','必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$','必须包含字母'),],
        error_messages={'required':'密码不能为空',
                        'min_length':'用户名最少为6个字符',
                        'max_length':'用户名不超过12个字符',},)
    password3=fields.CharField(
        required=True,
        widget=widgets.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新密码'}),
        min_length=6,
        max_length=12,
        label='新密码',
        validators=[
            RegexValidator(r'((?=.*\d))^.{6,12}$','必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$','必须包含字母'),],
        error_messages={'required':'密码不能为空',
                        'min_length':'用户名最少为6个字符',
                        'max_length':'用户名不超过12个字符',},)
    #检查原密码是否正确
    def _clean_old_pwd(self):
        username=self.cleaned_data.get('username')
        pwd=self.cleaned_data.get('password')
        user=User.objects.filter(username=username).first()
        if username and pwd:
            if not user:
                raise ValidationError('用户不存在！')
            if not user.check_password(pwd):
                raise ValidationError('用户或者原密码错误！')
    
        
    #核对新密码是否一致
    def _clean_new_password2(self):
        password2=self.cleaned_data.get('password2')
        password3=self.cleaned_data.get('password3')
        if password3 and password2:
            if password3 != password2:
                raise ValidationError('两次密码不一致！')
    #保证新旧密码不同
    def _clean_new_old_pwd(self):
        password2=self.cleaned_data.get('password2')
        user=User.objects.filter(username=self.cleaned_data.get('username')).first()
        if user.check_password(password2):
            raise ValidationError('新旧密码相同！')
    def clean(self):
        self._clean_new_password2()
        self._clean_old_pwd()
        self._clean_new_old_pwd()
    
    
    
            
    

