from django.forms import (
    ModelForm,
    TextInput,
    NumberInput,
    Textarea,
    Select,
    FileInput,
    DateTimeInput,
)

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from main.models import Education, Experience


class EducationForm(ModelForm):
    class Meta:
        model = Education

        # Field yang digunakan untuk menerima dan memvalidasi data pendidikan
        # dari input pengguna sebelum disimpan ke database.

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

    # Sanitasi dilakukan di sisi server agar tag HTML dari input pengguna
    # tidak ikut disimpan sebagai bagian dari data pendidikan.
    def clean_institution(self):
        institution = strip_tags(
            self.cleaned_data["institution"]
        ).strip()

        if not institution:
            raise ValidationError(
                "Institusi tidak boleh kosong atau hanya berisi tag HTML."
            )

        return institution


    # Menghapus tag HTML dari nama gelar atau program studi
    # sebelum data diproses lebih lanjut.
    def clean_degree(self):
        degree = strip_tags(
            self.cleaned_data["degree"]
        ).strip()

        if not degree:
            raise ValidationError(
                "Gelar / Program Studi tidak boleh kosong atau hanya berisi tag HTML."
            )

        return degree


    # Data tahun dibersihkan dari tag HTML dan spasi berlebih
    # untuk menjaga konsistensi data yang disimpan.
    def clean_year(self):
        year = strip_tags(
            self.cleaned_data["year"]
        ).strip()

        if not year:
            raise ValidationError(
                "Tahun tidak boleh kosong atau hanya berisi tag HTML."
            )

        return year

    def clean_graduation_year(self):
        graduation_year = self.cleaned_data.get(
            "graduation_year"
        )

        if graduation_year is not None:
            if graduation_year < 1900 or graduation_year > 2100:
                raise ValidationError(
                    "Tahun lulus harus berada antara 1900 dan 2100."
                )

        return graduation_year


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


    # Sanitasi server-side memastikan input tidak hanya bergantung
    # pada validasi atau escaping di sisi frontend.
    def clean_title(self):
        title = strip_tags(
            self.cleaned_data["title"]
        ).strip()

        if not title:
            raise ValidationError(
                "Judul experience tidak boleh hanya berisi tag HTML."
            )

        return title


    # Tag HTML dihapus dari deskripsi sebelum disimpan
    # sehingga input pengguna tidak dapat menyisipkan markup HTML berbahaya.
    def clean_description(self):
        return strip_tags(
            self.cleaned_data["description"]
        ).strip()