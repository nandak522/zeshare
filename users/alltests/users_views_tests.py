from utils import TestCase
from django.core.urlresolvers import reverse as url_reverse
from users.models import UserProfile

class UserSignupTests(TestCase):
    def test_valid_usersignup(self):
        form_data = {'name': 'Some Empty User',
                     'email': 'emptyuser@gmail.com',
                     'password': 'abc123'}
        response = self.client.post(path=url_reverse('users.views.view_register'),
                         data=form_data)
        self.assertRedirects(response,
                             expected_url=url_reverse('quest.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        userprofile = UserProfile.objects.latest()
        self.assertTrue(userprofile)
        self.assertEquals(userprofile.email, form_data['email'])

    def test_invalid_usersignup(self):
        form_data = {'name': '',
                     'email': 'emptyuser@',
                     'password': 'abc123'}
        response = self.client.post(path=url_reverse('users.views.view_register'),
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        context = response.context[0]
        form = context.get('form')
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('name'))
        self.assertTrue(form.errors.get('email'))
        self.assertFalse(form.errors.get('password'))

class UserLoginTests(TestCase):
    fixtures = ['UserLoginTests.json']
    
    def test_valid_userlogin(self):
        form_data = {'email': 'emptyuser@gmail.com',
                     'password': 'abc123'}
        response = self.client.post(path=url_reverse('users.views.view_login'),
                                    data=form_data)
        self.assertRedirects(response,
                             expected_url=url_reverse('quest.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        response = self.client.get(url_reverse('quest.views.view_homepage'))
        self.assertEquals(response.context[0].get('user').email, form_data['email'])

    def test_invalid_userlogin(self):
        for email in ('invalidemailaddress', 'nonexistantuser@gmail.com'):
            response = self.client.post(path=url_reverse('users.views.view_login'),
                                        data={'email': email, 'password': 'abc123'})
            self.assertTrue(response)
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'login.html')
            context = response.context[0]
            form = context.get('form')
            self.assertTrue(form.errors)
            self.assertTrue(form.errors.get('email'))