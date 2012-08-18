from django import forms


class ExecTaskForm(forms.Form):
    branch = forms.CharField(required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False)
