from datetime import date, datetime
from rest_framework.exceptions import ValidationError


def validate_age(request):
    birthdate = request.auth.get('birthdate') if request.auth else None

    if not birthdate:
        raise ValidationError('Enter your birthdate in order to create the product')

    birth_date = datetime.strptime(birthdate, '%Y-%m-%d').date()
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    if age < 18:
        raise ValidationError('You must be 18 years old or above')