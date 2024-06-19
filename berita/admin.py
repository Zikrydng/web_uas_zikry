from django.contrib import admin
from berita.models import Kategori, Artikel  # Gunakan huruf kapital 'Kategori'

admin.site.register(Kategori)  # Gunakan 'Kategori' untuk registrasi admin

class ArtikelAdmin(admin.ModelAdmin):
    list_display = ['judul', 'kategori', 'author']
    search_fields = ['judul']

admin.site.register(Artikel, ArtikelAdmin)
