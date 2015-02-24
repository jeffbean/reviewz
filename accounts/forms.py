#
# forms.py -- Forms for the siteconfig app.
#
# Copyright (c) 2008-2009 Christian Hammond
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class SiteSettingsForm(forms.Form):
    """
    A base form for loading/saving settings for a SiteConfiguration. This is
    meant to be subclassed for different settings pages. Any fields defined
    by the form will be loaded/saved automatically.
    """

    def __init__(self, siteconfig, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.siteconfig = siteconfig
        self.disabled_fields = {}
        self.disabled_reasons = {}

        self.load()

    def load(self):
        """
    Loads settings from the ```SiteConfiguration''' into this form.
    The default values in the form will be the values in the settings.

    This also handles setting disabled fields based on the
    ```disabled_fields''' and ```disabled_reasons''' variables set on
    this form.
    """
        for field in self.fields:
            value = self.siteconfig.get(field)
            self.fields[field].initial = value

            if field in self.disabled_fields:
                self.fields[field].widget.attrs['disabled'] = 'disabled'

    def save(self):
        """
    Saves settings from the form back into the ```SiteConfiguration'''.
    """
        if not self.errors:
            if hasattr(self, "Meta"):
                save_blacklist = getattr(self.Meta, "save_blacklist", [])
            else:
                save_blacklist = []

            for key, value in self.cleaned_data.iteritems():
                if key not in save_blacklist:
                    self.siteconfig.set(key, value)

            self.siteconfig.save()


class ActiveDirectorySettingsForm(SiteSettingsForm):
    auth_ad_domain_name = forms.CharField(
        label=_("Domain name"),
        help_text=_("Enter the domain name to use, (ie. example.com). This "
                    "will be used to query for LDAP servers and to bind to "
                    "the domain."),
        required=True,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_use_tls = forms.BooleanField(
        label=_("Use TLS for authentication"),
        required=False)

    auth_ad_find_dc_from_dns = forms.BooleanField(
        label=_("Find DC from DNS"),
        help_text=_("Query DNS to find which domain controller to use"),
        required=False)

    auth_ad_domain_controller = forms.CharField(
        label=_("Domain controller"),
        help_text=_("If not using DNS to find the DC, specify the domain "
                    "controller(s) here "
                    "(eg. ctrl1.example.com ctrl2.example.com:389)"),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_ou_name = forms.CharField(
        label=_("OU name"),
        help_text=_("Optionally restrict users to specified OU."),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_group_name = forms.CharField(
        label=_("Group name"),
        help_text=_("Optionally restrict users to specified group."),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_search_root = forms.CharField(
        label=_("Custom search root"),
        help_text=_("Optionally specify a custom search root, overriding "
                    "the built-in computed search root. If set, \"OU name\" "
                    "is ignored."),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    auth_ad_recursion_depth = forms.IntegerField(
        label=_("Recursion Depth"),
        help_text=_('Depth to recurse when checking group membership. '
                    '0 to turn off, -1 for unlimited.'),
        required=False,
        widget=forms.TextInput(attrs={'size': '40'}))

    def load(self):
        #can_enable_dns, reason = get_can_enable_dns()

        #if not can_enable_dns:
        #self.disabled_fields['auth_ad_find_dc_from_dns'] = reason


        #can_enable_ldap, reason = get_can_enable_ldap()

        #if not can_enable_ldap:
        #self.disabled_fields['auth_ad_use_tls'] = True
        #self.disabled_fields['auth_ad_group_name'] = True
        #self.disabled_fields['auth_ad_recursion_depth'] = True
        #self.disabled_fields['auth_ad_ou_name'] = True
        #self.disabled_fields['auth_ad_search_root'] = True
        #self.disabled_fields['auth_ad_find_dc_from_dns'] = True
        #self.disabled_fields['auth_ad_domain_controller'] = True

        #self.disabled_reasons['auth_ad_domain_name'] = reason
        super(ActiveDirectorySettingsForm, self).load()

    class Meta:
        title = _('Active Directory Authentication Settings')


class StandardAuthSettingsForm(SiteSettingsForm):
    auth_enable_registration = forms.BooleanField(
        label=_("Enable registration"),
        help_text=_("Allow users to register new accounts."),
        required=False)

    auth_registration_show_captcha = forms.BooleanField(
        label=_('Show a captcha for registration'),
        help_text=mark_safe(
            _('Displays a captcha using <a href="%(recaptcha_url)s">'
              'reCAPTCHA</a> on the registration page. To enable this, you '
              'will need to go <a href="%(register_url)s">here</A> to '
              'register an account and type in your new keys below.')
            % {
                'recaptcha_url': 'http://www.recaptcha.net/',
                'register_url': 'https://admin.recaptcha.net/recaptcha'
                                '/createsite/',
            }),
        required=False)

    recaptcha_public_key = forms.CharField(
        label=_('reCAPTCHA Public Key'),
        required=False,
        widget=forms.TextInput(attrs={'size': '60'}))

    recaptcha_private_key = forms.CharField(
        label=_('reCAPTCHA Private Key'),
        required=False,
        widget=forms.TextInput(attrs={'size': '60'}))

    def clean_recaptcha_public_key(self):
        """Validates that the reCAPTCHA public key is specified if needed."""
        key = self.cleaned_data['recaptcha_public_key'].strip()

        if self.cleaned_data['auth_registration_show_captcha'] and not key:
            raise ValidationError(_('This field is required.'))

        return key

    def clean_recaptcha_private_key(self):
        """Validates that the reCAPTCHA private key is specified if needed."""
        key = self.cleaned_data['recaptcha_private_key'].strip()

        if self.cleaned_data['auth_registration_show_captcha'] and not key:
            raise ValidationError(_('This field is required.'))

        return key

    class Meta:
        title = _('Basic Authentication Settings')

