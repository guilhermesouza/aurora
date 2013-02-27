from django import forms


class ExecTaskForm(forms.Form):
    branch = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Will be env.branch in fabfile'}))
    comment = forms.CharField(widget=forms.Textarea, required=False)


class UploadFabFileForm(forms.Form):
    file = forms.FileField()
