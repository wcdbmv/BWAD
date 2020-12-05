from django.contrib.auth.models import User


class UserBuilder:
    def __init__(self, username):
        self.user = User.objects.create(username=username)

    def with_email(self, email):
        self.user.email = email
        return self

    def with_password(self, password):
        self.user.password = password
        return self

    def build(self):
        return self.user


