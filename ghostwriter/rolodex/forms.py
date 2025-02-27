"""This contains all of the forms for the Rolodex application."""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper

from .models import (Client, Project, ClientContact, ProjectAssignment,
    ClientNote, ProjectNote)


class ClientCreateForm(forms.ModelForm):
    """Form used with the ClientCreate CreateView in models.py to allow
    excluding fields.
    """
    class Meta:
        """Metadata for the model form."""
        model = Client
        exclude = ('codename',)
        widgets = {
                    'name': forms.TextInput(attrs={'size': 55}),
                    'short_name': forms.TextInput(attrs={'size': 55}),
                    'note': forms.Textarea(attrs={'cols': 55})
                   }

    def __init__(self, *args, **kwargs):
        """Override the `init()` function to set some attributes."""
        super(ClientCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'SpecterOps, Inc.'
        self.fields['short_name'].widget.attrs['placeholder'] = 'SpecterOps'
        self.fields['note'].widget.attrs['placeholder'] = \
            'SpecterOps was founded in 2017 and ...'
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.field_class = \
            'h-100 justify-content-center align-items-center'


class ProjectCreateForm(forms.ModelForm):
    """Form used with the ProjectCreate CreateView in models.py to allow
    excluding fields.
    """
    class Meta:
        """Metadata for the model form."""
        model = Project
        exclude = ('operator', 'codename')
        widgets = {
                    'client': forms.HiddenInput(),
                    'slack_channel': forms.TextInput(attrs={'size': 55}),
                    'note': forms.Textarea(attrs={'cols': 55}),
                  }

    def __init__(self, *args, **kwargs):
        """Override the `init()` function to set some attributes."""
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['placeholder'] = 'mm/dd/yyyy'
        self.fields['start_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['start_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['end_date'].widget.attrs['placeholder'] = 'mm/dd/yyyy'
        self.fields['end_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['end_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['slack_channel'].widget.attrs[
            'placeholder'] = '#client-rt-2019'
        self.fields['note'].widget.attrs['placeholder'] = \
            'This project is intended to assess ...'
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.field_class = \
            'h-100 justify-content-center align-items-center'

    def clean_end_date(self):
        """Clean and sanitize user input."""
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        # Check if end_date comes before the start_date
        if end_date < start_date:
            raise ValidationError(_('Invalid date: The provided end date '
                                    'comes before the start date'))
        # Return the cleaned data
        return end_date


class ClientContactCreateForm(forms.ModelForm):
    """Form used with the FindingCreate CreateView in views.py to allow
    excluding fields.
    """
    class Meta:
        """Metadata for the model form."""
        model = ClientContact
        exclude = ('last_used_by', 'burned_explanation')
        widgets = {
                    'client': forms.HiddenInput(),
                    'name': forms.TextInput(attrs={'size': 55}),
                    'job_title': forms.TextInput(attrs={'size': 55}),
                    'email': forms.TextInput(attrs={'size': 55}),
                    'phone': forms.TextInput(attrs={'size': 55}),
                    'note': forms.Textarea(attrs={'cols': 55})
                   }

    def __init__(self, *args, **kwargs):
        """Override the `init()` function to set some attributes."""
        super(ClientContactCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs[
            'placeholder'] = 'Name to appear in reports'
        self.fields['email'].widget.attrs[
            'placeholder'] = 'info@specterops.io'
        self.fields['phone'].widget.attrs[
            'placeholder'] = '(###) ###-####'
        self.fields['job_title'].widget.attrs[
            'placeholder'] = 'A role/title to appear in reports'
        self.fields['note'].widget.attrs[
            'placeholder'] = 'Additional notes on the contact'
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.field_class = \
            'h-100 justify-content-center align-items-center'


class AssignmentCreateForm(forms.ModelForm):
    """Form used with the AssignmentCreate CreateView in models.py."""
    class Meta:
        """Metadata for the model form."""
        model = ProjectAssignment
        fields = ('__all__')
        widgets = {
                    'project': forms.HiddenInput()
                  }

    def __init__(self, *args, **kwargs):
        """Override the `init()` function to set some attributes."""
        super(AssignmentCreateForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['placeholder'] = 'mm/dd/yyyy'
        self.fields['start_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['end_date'].widget.attrs['placeholder'] = 'mm/dd/yyyy'
        self.fields['end_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['note'].widget.attrs[
            'placeholder'] = 'This assignment is only for 3 of the 4 weeks ...'
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.field_class = \
            'h-100 justify-content-center align-items-center'

    def clean(self):
        """Override `clean()` to do some additional checks with the
        hidden field.
        """
        cleaned_data = self.cleaned_data
        project = cleaned_data['project']
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if project:
            # Check if assignment dates are within the project date range
            if start_date < project.start_date:
                raise ValidationError(_('Invalid date: The provided start '
                                        'date comes before the start of this '
                                        'project, {}'.
                                        format(project.start_date)))
            if end_date > project.end_date:
                raise ValidationError(_('Invalid date: The provided end date '
                                        'comes after the end of this project'
                                        ', {}'.format(project.end_date)))

    def clean_end_date(self):
        """Clean and sanitize user input."""
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        # Check if end_date comes before the start_date
        if end_date < start_date:
            raise ValidationError(_('Invalid date: The provided end date '
                                    'comes before the start date'))
        # Return the cleaned data
        return end_date


class ClientNoteCreateForm(forms.ModelForm):
    """Form used with the ClientNote CreateView in models.py."""
    class Meta:
        """Metadata for the model form."""
        model = ClientNote
        fields = ('__all__')
        widgets = {
                    'timestamp': forms.HiddenInput(),
                    'operator': forms.HiddenInput(),
                    'client': forms.HiddenInput(),
                  }

    def __init__(self, *args, **kwargs):
        """Override the `init()` function to set some attributes."""
        super(ClientNoteCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.field_class = \
            'h-100 justify-content-center align-items-center'
        self.helper.form_show_labels = False


class ProjectNoteCreateForm(forms.ModelForm):
    """Form used with the ProjectNote CreateView in models.py."""
    class Meta:
        """Metadata for the model form."""
        model = ProjectNote
        fields = ('__all__')
        widgets = {
                    'timestamp': forms.HiddenInput(),
                    'operator': forms.HiddenInput(),
                    'project': forms.HiddenInput(),
                  }

    def __init__(self, *args, **kwargs):
        """Override the `init()` function to set some attributes."""
        super(ProjectNoteCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.field_class = \
            'h-100 justify-content-center align-items-center'
        self.helper.form_show_labels = False
