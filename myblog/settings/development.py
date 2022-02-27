import environ

from .base import *

env = environ.Env()
env.read_env(BASE_DIR / ".env.development")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}

# 邮箱正则表达式
REGEX_EMAIL = r"^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$"

# 发送邮件配置
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = True
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 465
# 发送邮件的邮箱
EMAIL_HOST_USER = "chris_guoc@163.com"
EMAIL_HOST_PASSWORD = "IIPXCHVYYTYSZCON"
# 收件人看到的发件人
EMAIL_FROM = "Chris Blog <chris_guoc@163.com>"
