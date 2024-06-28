from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, email):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('Users must have an phone address')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone=phone,
            email=self.normalize_email(email),
        )

        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, ida, email):
        """
        Creates and saves a staff user with the given email and password.
        """
        if not ida:
            raise ValueError('Users must have an ida address')

        user = self.create_user(
            phone,
            email,
        )
        user.ida = ida
        user.is_staff = True
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            phone,
            email,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user