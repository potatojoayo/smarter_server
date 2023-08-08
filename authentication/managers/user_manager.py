from django.contrib.auth.base_user import BaseUserManager

from smarter_money.models import Wallet


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, identification,  name, phone, is_active=True, password=None, fcm_token=None):
        if not identification:
            raise ValueError('아이디가 입력되지 않았습니다.')
        user = self.model(
            identification=identification,
            name=name,
            phone=phone,
            is_active=is_active,
            fcm_token=fcm_token
        )
        user.set_password(password)
        user.save(using=self._db)

        Wallet.objects.create(user=user)

        return user

    def create_superuser(self, identification,  name, phone, password=None,):
        user = self.create_user(
            identification=identification,
            name=name,
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

