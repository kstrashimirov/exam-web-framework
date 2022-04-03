from django import forms

from travel.common.helpers import BootstrapFormMixin
from travel.web.models import Country, Resort, Review


class CreateCountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Country Name', }),
            'banner': forms.TextInput(attrs={'placeholder': 'Banner'}),
        }


class DeleteCountryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Country
        fields = '__all__'


class CreateResortForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Resort
        fields = ('name', 'type', 'description', 'image', 'price', 'country')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Resort Name',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Description'
                }
            ),
            'image': forms.TextInput(
                attrs={
                    'placeholder': 'Image From the Resort'
                }
            ),
        }


class DeleteResortForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Resort
        fields = '__all__'


class EditResortForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.label_suffix = ''

    class Meta:
        model = Resort
        fields = '__all__'


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'grade', 'description', 'resort')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Short Description',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Description'
                }
            ),
        }
