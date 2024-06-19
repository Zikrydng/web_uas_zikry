from django.shortcuts import render, get_object_or_404
from berita.models import Artikel, Kategori

def home(request):
    template_name = "halaman/index.html"
    kategori_nama = request.GET.get('kategori')
    
    if kategori_nama == "None" or not kategori_nama:
        data_artikel = Artikel.objects.all()
        menu_aktif = "ALL"
    else:
        get_kategori = Kategori.objects.filter(nama=kategori_nama)
        print(get_kategori)
        if get_kategori.exists():
            data_artikel = Artikel.objects.filter(kategori=get_kategori.first())
            menu_aktif = get_kategori.first().nama
        else:
            data_artikel = []
            menu_aktif = "ALL"
    
    data_kategori = Kategori.objects.all()
    context = {
        'title': 'Selamat datang',
        'data_artikel': data_artikel,
        'data_kategori': data_kategori,
        'menu_aktif': menu_aktif
    }
    return render(request, template_name, context)

def about(request):
    template_name = "halaman/about.html"
    context = {
        'title': 'Selamat datang di halaman about',
        'umur': 20,
    }
    return render(request, template_name, context)

def contact(request):
    template_name = "halaman/contact.html"
    context = {
        'title': 'Selamat datang di halaman contact',
        'umur': 20,
    }
    return render(request, template_name, context)

def detail_artikel(request, slug):
    artikel = get_object_or_404(Artikel, slug=slug)
    template_name = 'halaman/detail_artikel.html'
    context = {
        'title': artikel.judul,
        'artikel': artikel
    }
    return render(request, template_name, context)
