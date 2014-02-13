from django import forms
from django.forms.widgets import Input, HiddenInput
import time
import hashlib
from random import sample, randint, shuffle
from django.core.exceptions import ValidationError

class HiddenWidget(Input):
    is_hidden = True
    def __init__(self, *args, **kwargs):
        super(HiddenWidget, self).__init__(*args, **kwargs)
        self.attrs.update({'style' : 'display: none'})

class Honeypot(forms.Field):
    widget = HiddenWidget
    def __init__(self, *args, **kwargs):
        super(Honeypot, self).__init__(required=False, *args, **kwargs)

    def clean(self, value):
        value = super(Honeypot, self).clean(value)
        if value:
            raise forms.ValidationError("Please, fill the form again.") 

class CharFieldHoneypot(forms.CharField, Honeypot):
    pass

class EmailFieldHoneypot(forms.EmailField, Honeypot):
    pass

def generate_clean_subfield(klass, new_fieldname):
    def clean_subfield():
        data = klass.cleaned_data.get(new_fieldname)
        if not data:
            raise ValidationError("This field is required.")
        klass.cleaned_data[klass.md5_dict[new_fieldname]] = data
        try:
            clean_subfield = getattr(klass, "clean_%s" %klass.md5_dict[new_fieldname])
            return clean_subfield()
        except AttributeError:
            return data
    return clean_subfield

class NoCaptchaForm(forms.Form):
    randomize_honeypots = True
    min_time = 5
    secret_password = ""

    honeypots = {'name': CharFieldHoneypot(),
                 'message': CharFieldHoneypot(),
                 'email': EmailFieldHoneypot(),
                 'login': CharFieldHoneypot(),
                 'password': CharFieldHoneypot(),
                 'city': CharFieldHoneypot()}

    def clean_timestamp(self):
        timestamp = self.cleaned_data['timestamp']
        if time.time() - timestamp < self.min_time:
            raise forms.ValidationError("Please, fill the form again.")
        return timestamp

    def __init__(self, data=None, *args, **kwargs):
        super(NoCaptchaForm, self).__init__(*args, **kwargs)
        self.md5_dict = {}
        keyOrder = []

        self.data = data or {}
        if self.data:
            prefixed_name_timestamp = self.add_prefix('timestamp')
            self.creation_time = self.data.get(prefixed_name_timestamp)
        else:
            self.creation_time = time.time()

        for fieldname, field in self.fields.items():
            m = hashlib.md5()
            m.update(str(self.creation_time))
            m.update(fieldname)
            m.update(self.secret_password)
            new_fieldname = m.hexdigest()
            self.fields[new_fieldname] = field
            self.md5_dict[new_fieldname] = fieldname
            keyOrder.append(new_fieldname)
            del self.fields[fieldname]

            clean_subfield = generate_clean_subfield(self, new_fieldname)
            clean_subfield.__name__ = "clean_%s" %new_fieldname
            setattr(self, clean_subfield.__name__, clean_subfield)

        self.fields['timestamp'] = forms.FloatField(widget=HiddenInput)
        self.fields['timestamp'].initial = self.creation_time
        keyOrder.append('timestamp')

        if self.randomize_honeypots:
            honeypots = sample(self.honeypots, randint(2, len(self.honeypots)))
        else:
            honeypots = self.honeypots

        for honeypot in honeypots:
            self.fields[honeypot] = self.honeypots[honeypot]
            keyOrder.insert(randint(0, len(keyOrder)), honeypot)
        self.fields.keyOrder = keyOrder
