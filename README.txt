=========
NoCaptcha
=========

No bots with no captcha. Easy and fast way to secure your django forms with no using of damned, hated by everyone captcha.

INITIAL ACCTIONS
================

Include nocaptcha in your settings' installed apps

INSTALLED_APPS = (
	...
	'nocaptcha',
	...
	)

TYPICAL USAGE
=============

Include nocaptcha in your form. Add secret password, that would be used in md5 hash and min_time value - the shortest time, that could be possible to fill your form.

from nocaptcha.forms import NoCaptchaForm

class ContactForm(NoCaptchaForm, forms.Form):
    secret_password = "NoCaptcha rocks!"
    min_time = 5
    name = forms.CharField(label="Name")
    message = forms.CharField(label="Message", widget=forms.Textarea)


BENEFITS
========

From now on all the fieldnames in your form will be encoded into a md5(timestamp + fieldname + secret_password).
The timestamp field will be created with the timestamp of the page initial get. If the form will be posted in less then min_time, the error will be raised.
There will be added a few honeypots with tempting names like "name" or "password" hidden with "display: none" style. If any of them will be filled, the error will be raised. The honeypots are taken as sample from list of honeypots and their order is shuffled.

With these changes, the chance that any bot would automatically pass through your form is minimaised to zero. So stop using tha damn, hated by everyone captcha. Use nocaptcha.

REQUIREMENTS
============

Django >= 1.1.1
