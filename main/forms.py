from django.forms import ModelForm, TextInput

from main.models import Education


class EducationForm(ModelForm):
    class Meta:
        model = Education

        fields = [
            "institution",
            "degree",
            "year",
        ]

        labels = {
            "institution": "Institusi",
            "degree": "Gelar / Program Studi",
            "year": "Tahun",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 100,
                }
            ),
            "degree": TextInput(
                attrs={
                    "placeholder": "S1 Sistem Informasi",
                    "maxlength": 100,
                }
            ),
            "year": TextInput(
                attrs={
                    "placeholder": "2024 - Present",
                    "maxlength": 20,
                }
            ),
        }