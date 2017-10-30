from django.core.mail import send_mail,EmailMessage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import loader

#发送邮件辅助函数
def send_help_email(toemail,u):
    token=u.userextend.generate_confirmation_token()
    url1=reverse('confirm',args=[token])
    confirmurl="127.0.0.1:8000"+url1
    html_content=loader.render_to_string('usersysterm/email_confirm_template.html',{'confirmurl':confirmurl})
    msg=EmailMessage('请您确认邮件',html_content,settings.EMAIL_HOST_USER,[toemail])
    msg.content_subtype='html'
    msg.send()
  
	
#发送密码改动邮件
def send_pwd_email(toemail,u):
    token=u.userextend.generate_confirmation_token()
    url1=reverse('change_pwd',args=[token])
    confirmurl="127.0.0.1:8000"+url1
    html_content=loader.render_to_string('usersysterm/email_pwd.html',{'confirmurl':confirmurl})
    msg=EmailMessage('请您确认邮件',html_content,settings.EMAIL_HOST_USER,[toemail])
    msg.content_subtype='html'
    msg.send()