from django.views.generic.base import View
from django.template.response import TemplateResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

from contact.models import Contact
from contact.forms import ContactForm
from utils.tools import getIntro


class ContactView(View):
    template = 'contact.html'
    http_method_names = ['get', 'post']
    form = ContactForm
    intro = getIntro(5)

    def get(self, request, *args, **kwargs):
        contact_information = Contact.objects.all()[0]
        form = self.form()

        context = {
            'contact_information': contact_information,
            'contact_form': form,
            'intro': self.intro,
        }

        return TemplateResponse(request, self.template, context)

    def post(self, request, *args, **kwargs):
        contact_information = Contact.objects.all()[0]
        form = self.form(request.POST)
        valid = form.is_valid()

        error_messages = ''
        success_messages = ''

        if valid:
            cleaned_data = form.cleaned_data
            name = cleaned_data['name']
            location = cleaned_data['location']
            from_email = cleaned_data['email']
            message = cleaned_data['comment']

            subject = "Email from %s, %s" % (name, location)

            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, ['19noname19@gmail.com'])
                    success_messages = 'Thanks your email.'
                except BadHeaderError:
                    error_messages = 'Invalid header found.'
            else:
                error_messages = 'Make sure all fields are entered and valid.'

        context = {
            'contact_information': contact_information,
            'contact_form': form,
            'error_messages': error_messages,
            'success_messages': success_messages,
            'intro': self.intro,
        }

        return TemplateResponse(request, self.template, context)
