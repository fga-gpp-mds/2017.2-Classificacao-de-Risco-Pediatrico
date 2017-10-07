# from django.test import TestCase
import pytest
# from apps.users.models import UserManager
# import apps.users.views
# from apps.users.views import RegistrationAdminView
# from factories import PatientFactory
# Create your tests here.

from apps.users.models import Staff


@pytest.mark.django_db
class TestUsers:

    def test_home(self, client):
        response = client.get('/user/')
        assert response.status_code == 200

    def test_login_view(self, client):

        # if this simple test is failing,
        # try running 'python manage.py collectstatic'
        response = client.get('/user/login/')
        assert response.status_code == 200

    def test_logout_view(self, client):
        # TODO: review this test:
        kwargs = {'email': 'email@gmail.com', 'password': '1234asdf'}
        is_logged = client.login(
            username=kwargs["email"],
            password=kwargs["password"])
        assert is_logged is False

    def test_home_receptionist_view(self, client):
        response = client.get('/user/home/receptionist/')
        assert response.status_code == 200

    def test_user_get_full_name(self):
        name = "Carlinhos Cabral"
        user = Staff(name=name)
        assert user.get_full_name() == name

    def test_get_short_name(self):
        name = "Carlinhos"
        user = Staff(name=name)
        assert user.get_short_name() == name

    def test_has_perm(self):
        perm = None
        user = Staff()
        assert user.has_perm(perm) is True

    def test_has_module_perms(self):
        app_name = None
        user = Staff()
        assert user.has_module_perms(app_name) is True

    def test_is_admin(self):
        user_name = Staff(name='Bruno', is_admin=True)
        assert user_name.is_admin is True

    def test_is_not_admin(self):
        user_name = Staff(name='Bruno')
        assert user_name.is_admin is False

    def test__str__(self):
        user_email = Staff(email='bruno@gmail.com')
        assert str(user_email) == 'bruno@gmail.com'
