# coding:utf8

from flask_mail import Message
from exts import mail


# receivers: 字符串或者数组
def send_mail(subject, receivers, body=None, html=None):
    assert receivers
    if not body and not html:
        return False

    # receivers如果是字符串，转换成数组
    if isinstance(receivers, str) or isinstance(receivers, unicode):
        receivers = [receivers]

    msg = Message(subject=subject, recipients=receivers, body=body, html=html)
    try:
        mail.send(msg)
    except:
        return False
    return True





























