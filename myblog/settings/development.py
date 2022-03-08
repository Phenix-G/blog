from datetime import timedelta

from .base import *

env.read_env(BASE_DIR / ".env.development")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Token',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# 发送Email配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 发邮件的smtp服务器地址
EMAIL_HOST = 'smtp.163.com'  # 可以查看你使用那个服务，就是对应的哪个服务器地址
EMAIL_PORT = 25  # 端口号固定

# 发送邮件的邮箱
EMAIL_HOST_USER = env('EMAIL_HOST_USER')  # 你的邮箱名字
# 邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  # 你设置的授权码
# 收件人看到的发件人
EMAIL_FROM = env('EMAIL_FROM')


# Celery settings
# 配置celery时区，默认时UTC。
if USE_TZ:
    timezone = TIME_ZONE

# celery配置redis作为broker。redis有16个数据库，编号0~15，这里使用第1个。
broker_url = 'redis://127.0.0.1:6379/5'

# 设置存储结果的后台
result_backend = 'redis://127.0.0.1:6379/6'

# 可接受的内容格式
accept_content = ["json"]
# 任务序列化数据格式
task_serializer = "json"
# 结果序列化数据格式
result_serializer = "json"
