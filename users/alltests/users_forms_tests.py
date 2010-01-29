from django.test import TestCase

class RegistrationFormTests(TestCase):
    def test_user_submits_valid_form(self):
        form_data = {'name': 'Adnan',
                     'email': 'empty@gmail.com',
                     'password': 'empty'}
        from users.forms import RegistrationForm
        form = RegistrationForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(form.cleaned_data)
        self.assertEquals(form.cleaned_data.get('name'), form_data['name'])
        self.assertEquals(form.cleaned_data.get('email'), form_data['email'])
        self.assertEquals(form.cleaned_data.get('password'), form_data['password'])
        
    def test_user_submits_empty_form(self):
        form_data = {'name': '',
                     'email': '',
                     'password': ''}
        from users.forms import RegistrationForm
        form = RegistrationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('name'))
        self.assertTrue(form.errors.get('email'))
        self.assertTrue(form.errors.get('password'))
        
    def test_user_submits_invalid_data(self):
        form_data = {'name': 'Adnan',
                     'email': 'nonemail',
                     'password': '1234'}
        from users.forms import RegistrationForm
        form = RegistrationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertFalse(form.errors.get('name'))
        self.assertTrue(form.errors.get('email'))
        self.assertFalse(form.errors.get('password'))
        
class LoginFormTests(TestCase):
    def test_user_submits_valid_data(self):
        form_data = {'email': 'empty@gmail.com',
                     'password': 'empty'}
        from users.forms import LoginForm
        form = LoginForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(form.cleaned_data)
        self.assertEquals(form.cleaned_data.get('email'), form_data['email'])
        self.assertEquals(form.cleaned_data.get('password'), form_data['password'])
        
    def test_user_submits_empty_form(self):
        form_data = {'email': '',
                     'password': ''}
        from users.forms import LoginForm
        form = LoginForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('email'))
        self.assertTrue(form.errors.get('password'))
        
    def test_user_submits_invalid_data(self):
        form_data = {'email': 'empty@',
                     'password': 'empty'}
        from users.forms import LoginForm
        form = LoginForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('email'))