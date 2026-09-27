from django.forms import (
    ModelForm,
    TextInput,
    NumberInput,
    Textarea,
    Select,
    FileInput,
    DateTimeInput,
)

from main.models import Education, Experience


class EducationForm(ModelForm):
    class Meta:
        model = Education

        # Field yang dapat diisi atau diubah pengguna melalui form.
        fields = [
            "institution",
            "degree",
            "year",
            "graduation_year",
        ]

        labels = {
            "institution": "Institusi",
            "degree": "Gelar / Program Studi",
            "year": "Tahun",
            "graduation_year": "Tahun Lulus",
        }

        # Widget digunakan untuk memberikan placeholder dan batasan input
        # agar pengisian data lebih jelas bagi pengguna.
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
            "graduation_year": NumberInput(
                attrs={
                    "placeholder": "2028",
                    "min": 1900,
                    "max": 2100,
                }
            ),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience

        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Judul",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "Thumbnail",
            "started_at": "Mulai",
            "ended_at": "Selesai",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Contoh: BEM Fasilkom UI",
                    "maxlength": 255,
                }
            ),

            "description": Textarea(
                attrs={
                    "placeholder": "Jelaskan pengalaman ini...",
                    "rows": 5,
                }
            ),

            "category": Select(),

            "thumbnail": FileInput(),

            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }