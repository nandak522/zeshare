from utils import TestCase
from users.models import UserProfile
from django.template.defaultfilters import slugify

class UserProfileTests(TestCase):
    fixtures = ['UserProfileTests.json']

    def test_create_userprofile(self):
        data = {'email': 'empty@gmail.com',
                'password': 'emptypassword',
                'name': 'Nanda Kishore'}
        userprofile = UserProfile.objects.create_userprofile(email=data['email'],
                                                             password=data['password'],
                                                             name=data['name'])
        self.assertTrue(userprofile)
        self.assertTrue(userprofile.user)
        self.assertEquals(userprofile.user.get_profile().id, userprofile.id)
        self.assertEquals(userprofile.email, data['email'])
        self.assertTrue(userprofile.user.check_password(data['password']))
        self.assertEquals(userprofile.name, data['name'])
        self.assertEquals(slugify(userprofile.name), userprofile.slug)

    def test_create_duplicate_userprofile(self):
        data = {'email': 'madhav.bnk@gmail.com',
                'password': 'emptypassword',
                'name': 'Nanda Kishore'}
        from users.models import UserProfileAlreadyExistsException
        self.assertRaises(UserProfileAlreadyExistsException,
                          UserProfile.objects.create_userprofile,
                          email=data['email'],
                          password=data['password'],
                          name=data['name'])

    def test_update_userprofile(self):
        data = {'email': 'madhav.bnk@gmail.com',
                'password': 'reallyemptypassword',
                'name': 'Nanda'}
        userprofile = UserProfile.objects.get(email=data['email'])
        password = data['password']
        UserProfile.objects.update_userprofile(userprofile,
                                               email=data['email'],
                                               password=data['password'],
                                               name=data['name'])
        self.assertTrue(userprofile.user.check_password(password))
        self.assertEquals(userprofile.name, data['name'])