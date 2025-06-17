from django.forms import ModelForm, Textarea

from .models import Task


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "is_complete"]
        # widgets = {
        #     "title": Textarea(),
        # }
