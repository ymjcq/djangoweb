from celery.decorators import task
from celery.utils.log import get_task_logger
from usersysterm.emails import send_help_email,send_pwd_email

logger=get_task_logger(__name__)

@task(name="send_help_email_task")
def send_help_email_task(toemail,u):
	logger.info('send register or confirm email')
	return send_help_email(toemail,u)

@task(name="send_pwd_email_task")
def send_pwd_email_task(toemail,u):
	logger.info('send change pwd email')
	return send_pwd_email(toemail,u)