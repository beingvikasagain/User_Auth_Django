from itsdangerous import URLSafeTimedSerializer
from user_auth import settings
from django.core.mail import send_mail


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt = settings.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=43200):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt = settings.SECURITY_PASSWORD_SALT,
            max_age = expiration
        )
        return email
    except Exception as e:
        return False
    
def send_verification_email(user):
    link = settings.FRONTEND_VERIFY_EMAIL_URL + generate_confirmation_token(user.email)
    subject = "Verify email"
    message = "Hello " + user.first_name + user.last_name + "\n\nPlease click on the following link to verify your email:\n\n" + link
    try:
        email_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False, )
        if not email_sent:
            return False
        return True
    except Exception:
        return False