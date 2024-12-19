import random
import smtplib

from django.core.cache import cache
from django.core.mail import send_mail

from authenticate.models import User
from config import settings


def generate_random_activation_code() -> int:
    random_number = random.randint(100000, 999999)

    return random_number


def save_generated_activation_code(cache_key, email) -> int or None:
    try:
        user_id = User.objects.get(email=email).id
        activation_code = generate_random_activation_code()
        cache.set(f'{cache_key}_{user_id}', activation_code, timeout=60*5) # 5 minutes
        return activation_code

    except User.DoesNotExist:
        return None


def check_activation_code(cache_key, email, activation_code) -> bool:
    try:
        user_id = User.objects.get(email=email).id
        saved_activation_code = cache.get(f'{cache_key}_{user_id}')
        if int(saved_activation_code) == int(activation_code):
            return True
        else:
            return False

    except User.DoesNotExist:
        return False


def send_activation_code(cache_key, email):
    activation_code = save_generated_activation_code(cache_key, email)
    print("activation_code", activation_code)

    subject = 'User activation code'
    message = f'Your activation code: {activation_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
