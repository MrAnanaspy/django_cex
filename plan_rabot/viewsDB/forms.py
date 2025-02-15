from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _
from .models import Detail


from django import forms
from .models import Detail

class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = '__all__'
        labels = {
            'EAM': 'EAM',
            'addition': 'addition',
            'model': 'model',
        }
