from django.shortcuts import render_to_response
from django.template import RequestContext
from django.test import TestCase

language_choices = (('py','Python'),
                    ('sql', 'SQL'),
                    ('js', 'Javascript'),
                    ('html', 'HTML')) 

def response(request, template, context):
    return render_to_response(template, context, context_instance=RequestContext(request))

def print_json(queryset):
    from django.core.serializers import serialize
    print serialize("json", queryset, indent=4)

class TestCase(TestCase):
    def tearDown(self):
        del self.client
        
def post_data(request):
    return request.POST.copy()

def get_data(request):
    return request.GET.copy()