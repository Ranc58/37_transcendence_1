from factory import faker, django as django_factory
from django.contrib.auth.models import User


LOCALE = 'en_GB'


class UserFactory(django_factory.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = faker.Faker('first_name', locale=LOCALE)
    first_name = faker.Faker('first_name', locale=LOCALE)
    last_name = faker.Faker('last_name', locale=LOCALE)
    email = faker.Faker('ascii_safe_email', locale=LOCALE)
    password = faker.Faker('password', locale=LOCALE)
