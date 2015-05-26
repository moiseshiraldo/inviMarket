from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django import forms

from inviMarket.models import Profile, Website, SiteEdition, Offer, Chain

class RegisterForm(UserCreationForm):
    """
    Defines the user registration form

    """
    username = forms.RegexField(
        label=_('Username'),
        max_length=30,
        regex=r'^[\w.+-]+$',
        help_text= _("Required. 30 characters or fewer. Letters, digits and "
                     "./+/-/_ only."),
        error_messages={
          'invalid': _("This value may contain only letters, numbers and "
                       "./+/-/_ characters.")
        }
    )
    email = forms.EmailField(required = True)
    first_name = forms.CharField(label = _('Name'), required = True,
                                 max_length=30)

    class Meta:
        model = User
        fields=("username","email","first_name","last_name",
                "password1","password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if (username.startswith(".") or username.endswith(".") or
                ".." in username):
            raise forms.ValidationError(
                _("This value may not start with, end with or contain two "
                  "consecutive '.'"),
                code="invalid",
            )
        else:
            try:
                User._default_manager.get(username=username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError(
                _('A user with that username already exists.'))

    def clean_email(self):
        # Checks that the email is not duplicate
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email = email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_('A user with that email already exists.'))

    def save(self, commit = True):
        # Stores the user in the database
        user = super(RegisterForm, self).save(commit = False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.is_active = False
            user.save()
            return user

class CategoryForm(forms.Form):
    """
    Defines the search by category form

    """
    categories = forms.MultipleChoiceField(choices = Website.CAT,
      widget = forms.CheckboxSelectMultiple(), required = False, label='')


class TypeForm(forms.Form):
    """
    Defines the search by type form

    """
    types= forms.MultipleChoiceField(choices = Website.WTYPE,
      widget = forms.CheckboxSelectMultiple(), required=False, label='')

class OrderByForm(forms.Form):
    """
    Defines the order by form

    """
    CHOICES = (
      ('PO', _('Popularity')),
      ('CA', _('Category')),
      ('TY', _('Type')),
      ('RE', _('Requested invites')),
      ('OF', ('Offered invites')),
    )
    order = forms.ChoiceField(choices=CHOICES, widget = forms.Select(),
                              label=_('Order by'))

class OfferForm(forms.ModelForm):
    """
    Defines the invite offer form

    """
    error_messages = {
        'number_mismatch': _("The number of invites to donate can't be greater "
                             "than the total offered number."),
    }
    number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'max': settings.MAX_OFFERS, 'min': 0,}),
        validators=[MaxValueValidator(settings.MAX_OFFERS),
                    MinValueValidator(0)]
    )
    to_donate = forms.IntegerField(
        widget=forms.NumberInput(attrs={'max': settings.MAX_OFFERS, 'min': 0,}),
        validators=[MaxValueValidator(settings.MAX_OFFERS),
                    MinValueValidator(0)]
    )

    class Meta:
        model = Offer
        fields = ("number", "to_donate", "referral")
        labels = {
            'referral': _('Referral link'),
        }

    def clean_to_donate(self):
        number = self.cleaned_data.get("number")
        to_donate = self.cleaned_data.get("to_donate")
        if number and to_donate > number:
            raise forms.ValidationError(
                self.error_messages['number_mismatch'],
                code='number_mismatch',
            )
        return to_donate

    def save(self, commit=True):
        offer = super(OfferForm, self).save(commit=False)
        offer.number = self.cleaned_data["number"]
        offer.to_donate = self.cleaned_data["to_donate"]
        offer.referral = self.cleaned_data["referral"]
        if commit:
            offer.save()
        return offer

class TradeForm(forms.Form):
    """
    Defines a multiple choice form for trade searching and proposing

    """
    sites = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                      required=False)

    def __init__(self, choices, label, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
        self.fields['sites'].choices = choices
        self.fields['sites'].label = label

class ShowDonationsForm(forms.Form):
    """
    Defines the show donations/all form

    """
    CHOICES = (
        ('ALL', _('All')),
        ('DON', _('Donations')),
    )
    show = forms.ChoiceField(choices=CHOICES, required=False, label=_('Show'))

class CommentsForm(forms.Form):
    """
    Defines a text-area form for trade comments

    """
    comments = forms.CharField(max_length=400, widget=forms.Textarea(),
                               required=False)

class TradeFilter(forms.Form):
    """
    Defines a multiple choice form for user's trades searching

    """
    CHOICES = (
        ('RE', _('Received')),
        ('SE', _('Sent')),
        ('AC', _('Accepted')),
    )
    status = forms.MultipleChoiceField(choices=CHOICES,
                                       widget = forms.CheckboxSelectMultiple(),
                                       label=_('Status'),
                                       required=False,
                                       )

class EditionForm(forms.ModelForm):
    """
    Defines the form for editing sites or proposing new ones

    """

    class Meta:
        model = SiteEdition
        fields = ("name", "url", "refvalidator", "email_domain", "description",
                  "source", "lang", "webType", "category", "active", "comments")
        labels = {
            'name': _('Name') + '*',
            'url': 'URL' + '*',
            'refvalidator': _('Referral validator'),
            'email_domain': _('Mail domain'),
            'description': _('Description'),
            'source': _('Source'),
            'lang': _('Language') + '*',
            'webType': _('Type') + '*',
            'category': _('Category') + '*',
            'active': _('Active'),
            'comments': _('Comments'),
        }


class ConfigForm(forms.ModelForm):
    """
    Defines the profile configuration form

    """
    first_name = forms.CharField(label = _('Name'), required = True,
                                 max_length=30)
    class Meta:
        model = Profile
        fields = ("avatar", "first_name", "lang", "notify")

    def save(self, commit=True):
        profile = super(ConfigForm, self).save(commit=True)
        profile.user.first_name = self.cleaned_data["first_name"]
        profile.user.save()
        return profile

class ChainForm(forms.ModelForm):
    """
    A form that creates a referral chain

    """
    jumps = forms.IntegerField(
        widget=forms.NumberInput(attrs={'max': 3, 'min': '1',}),
        validators=[MaxValueValidator(3), MinValueValidator(1)],
        label="Referrals to jump"
    )
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput,
                               required=False)

    class Meta:
        model = Chain
        fields = ("jumps",)

    def save(self, commit=True):
        chain = super(ChainForm, self).save(commit=False)
        chain.password = self.cleaned_data["password"]
        chain.jumps = self.cleaned_data["jumps"]
        if commit:
            chain.save()
        return chain

class PasswordForm(forms.Form):
    """
    A simple password form

    """
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)