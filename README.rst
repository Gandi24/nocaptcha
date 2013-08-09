=========
NoCaptcha
=========

No bots with no CAPTCHA. Easy and fast way to secure your Django forms without
using the damned, hated by everyone CAPTCHA.

Initial Actions
===============

Include nocaptcha in your settings' installed apps::

    INSTALLED_APPS = (
        ...
        'nocaptcha',
        ...
    )

Typical Usage
=============

Include nocaptcha in your form. Add secret password, that would be used in MD5
hash and ``min_time`` value -- the shortest time within which it is possible
to fill your form::

    from nocaptcha.forms import NoCaptchaForm

    class ContactForm(NoCaptchaForm, forms.Form):
        secret_password = "NoCaptcha rocks!"
        min_time = 5
        name = forms.CharField(label="Name")
        message = forms.CharField(label="Message", widget=forms.Textarea)


Benefits
========

From now on all the field names in your form will be encoded into
a ``md5(timestamp + fieldname + secret_password)``.  The timestamp field will
be created with the timestamp of the page's initial GET. If the form is posted
in less than ``min_time``, an error will is raised.  There are a few honeypots
with tempting names like "name" or "password" added to the form and hidden
with ``display: none`` style. If any of them are filled, an error will be
raised. The honeypots are selected from the list of honeypots in random order.

With those changes, the chance that a bot would automatically pass through
your form is reduced to zero. So stop using the damned, hated by everyone
CAPTCHA. Use nocaptcha.

Requirements
============

    Django >= 1.1.1
