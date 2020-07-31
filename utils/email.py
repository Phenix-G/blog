from django.conf import settings
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer


def send_register_active_email(email):
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 5 * 60)
    info = {'confirm': email}
    token = serializer.dumps(info)
    token = token.decode('utf8')

    # 加密
    url = 'http://127.0.0.1:8000/active/{}'.format(token)

    # todo 发送邮件
    # 邮件主题
    subject = '尚惠欢迎信息'
    # 邮件信息，正文部分
    message = '欢迎'
    # 发送者，直接从配置文件中导入上面配置的发送者
    sender = settings.EMAIL_FROM
    # 接收者的邮箱，是一个列表，这里是前端用户注册时传过来的 email
    receiver = [email]
    # html结构的信息，其中包含了加密后的用户信息token
    html_message = '<a href=' + url + '>' + url + '</a>'
    # 调用Django发送邮件的方法，这里传了5个参数
    send_mail(subject=subject, message=message, from_email=sender, recipient_list=receiver, html_message=html_message)
