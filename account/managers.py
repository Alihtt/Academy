from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, first_name, last_name, password):

        if not phone_number:
            raise ValueError('You must send phone number')
        if not email:
            raise ValueError('You must send email')
        if not first_name:
            raise ValueError('You must send first name')
        if not last_name:
            raise ValueError('You must send last name')

        user = self.model(phone_number=phone_number,
                          email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, first_name, last_name, password):
        user = self.create_user(phone_number, email, first_name, last_name, password)
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user
