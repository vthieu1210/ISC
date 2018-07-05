from django import forms

class CategoryForm(forms.Form):
    name = forms.CharField(required=True)
    title = forms.CharField(required=False)
    path = forms.CharField(required=True)

class TaskForm(forms.Form):
    subject = forms.CharField(max_length=4000, help_text='4000 characters max.')
    start_date = forms.CharField(max_length=50, help_text='50 characters max.')
    due_date = forms.CharField(max_length=50, help_text='50 characters max.')
    done = forms.IntegerField(required=False)
    status = forms.CharField(max_length=50, help_text='50 characters max.')
    assignee = forms.CharField(max_length=50, help_text='50 characters max.')
    department = forms.CharField(max_length=50, help_text='50 characters max.')
    tracker = forms.CharField(max_length=50, help_text='50 characters max.')
    complexity = forms.IntegerField()
    estimated_time = forms.IntegerField()
    spent_time = forms.IntegerField(required=False)
    actual_end_date = forms.CharField(required=False, max_length=50, help_text='50 characters max.')
    project = forms.CharField(max_length=50, help_text='50 characters max.')

    def clean(self):
        if not self.cleaned_data['spent_time']:
            self.cleaned_data['spent_time'] = ''
        if not self.cleaned_data['done']:
            self.cleaned_data['done'] = ''
