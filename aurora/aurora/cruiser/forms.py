from django import forms


class ExecTask(forms.Form):
    branch = forms.TextField(required=False)
