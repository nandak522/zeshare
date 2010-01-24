from django.shortcuts import render_to_response
from django.template import RequestContext
from django.test import TestCase, Client

language_choices = (('py','Python'),
                    ('sql', 'SQL'),
                    ('js', 'Javascript'),
                    ('html', 'HTML')) 

def response(request, template, context, status_code=200):
    return render_to_response(template, context, context_instance=RequestContext(request))

def print_json(queryset):
    from django.core.serializers import serialize
    print serialize("json", queryset, indent=4)
    
class TestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
    def tearDown(self):
        del self.client