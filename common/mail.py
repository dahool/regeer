from django.conf import settings 
from django.core.mail import SMTPConnection

def send_mass_mail_em(email_message_list, fail_silently=False, auth_user=None,
                   auth_password=None):
    connection = SMTPConnection(username=auth_user, password=auth_password,
                                fail_silently=fail_silently)
    return connection.send_messages(email_message_list)