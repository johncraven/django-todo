from django import forms

from .models import Task


class TaskCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].full_width = True
        self.fields["description"].full_width = True

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "due_on",
            "priority",
        ]
        widgets = {"due_on": forms.DateInput(attrs={"type": "date"})}


class TaskUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].full_width = True
        self.fields["description"].full_width = True

    class Meta:
        model = Task
        fields = [
            "is_complete",
            "title",
            "description",
            "due_on",
            "priority",
        ]
        widgets = {"due_on": forms.DateInput(attrs={"type": "date"})}
