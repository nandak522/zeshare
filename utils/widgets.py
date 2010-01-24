from django import forms
from django.utils.safestring import mark_safe

class Textarea(forms.Textarea):
    class Media:
        js = ('/site_media/js/tiny_mce.js',)
        
    def __init__(self, attrs=None):
        self.attrs = {'class': 'advanceeditor'}
        if attrs: self.attrs.update(attrs)
        super(Textarea, self).__init__(attrs)
        
    def render(self, name, value, attrs=None):
        rendered = super(Textarea, self).render(name, value, attrs)
        return rendered + mark_safe(u'''
        <script type="text/javascript">;
        tinyMCE.init({
            mode: "textareas",
            theme: "advanced",
            plugins: "advhr,table,emotions,media,insertdatetime,directionality",
            theme_advanced_toolbar_align: "left",
            theme_advanced_toolbar_location: "top",
            theme_advanced_buttons1:"bold,italic,underline,strikethrough,sub,sup,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,f
            theme_advanced_buttons2:"bullist,numlist,outdent,indent,ltr,rtl,separator,link,unlink,anchor,image,separator,table,insertdate,inserttime,advh
            theme_advanced_buttons3: "",
            content_css: "images/style.css",
            height: "350px",
            width: "653px"});
        </scrip>; 
        ''')    