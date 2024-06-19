from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from berita.models import Kategori, Artikel
from berita.forms import ArtikelForm

def is_operator(user):
    return user.groups.filter(name='Operator').exists()

# Create your views here.
@login_required
def dashboard(request):
    template_name = "dashboard/index.html"
    context = {
        'title': 'Selamat Datang Di Web Saya',
    }
    return render(request, template_name, context)

##################################################Kategori#####################################################
@login_required
@user_passes_test(is_operator, login_url='/')
def kategori_list(request):
    template_name = "dashboard/snippets/kategori/kategori_list.html"
    kategori_ambil = Kategori.objects.all()
    print(kategori_ambil)
    context = {
        'title': 'Halaman Kategori',
        'kategori': kategori_ambil
    }
    return render(request, template_name, context)

@login_required
def kategori_add(request):
    template_name = "dashboard/snippets/kategori/kategori_add.html"
    if request.method == "POST":
        nama_input = request.POST.get('nama_kategori')
        Kategori.objects.create(
            nama=nama_input
        )
        return redirect(reverse('kategori_list'))
    
    context = {
        'title': 'Tambah Kategori',
    }
    return render(request, template_name, context)

@login_required
def kategori_update(request, id_kategori):
    template_name = "dashboard/snippets/kategori/kategori_update.html"
    try:
        kategori = Kategori.objects.get(id=id_kategori)
    except Kategori.DoesNotExist:
        return redirect(reverse('kategori_list'))
    if request.method == "POST":
        nama_input = request.POST.get('nama_kategori')
        kategori.nama = nama_input
        kategori.save()
        return redirect(reverse('kategori_list'))
    context ={
        'title': 'Update Kategori',
        'kategori': kategori,
    }
    return render(request, template_name, context)

@login_required
def kategori_delete(request, id_kategori):
    try:
        Kategori.objects.get(id=id_kategori).delete()
    except Kategori.DoesNotExist:
        pass
    return redirect(reverse('kategori_list'))

##################################################Kategori#####################################################

##################################################Artikel######################################################

@login_required
def artikel(request):
    template_name = "dashboard/artikel.html"
    context = {
        'title': 'Halaman Artikel'
    }
    return render(request, template_name, context)

@login_required
def artikel_list(request):
    template_name = "dashboard/snippets/artikel/artikel_list.html"
    artikel = Artikel.objects.all()
    print(artikel)
    context = {
        'title': 'Daftar Artikel',
        'artikel': artikel,
    }
    return render(request, template_name, context)

@login_required
def artikel_add(request):
    template_name = "dashboard/snippets/artikel/artikel_forms.html"
    if request.method == "POST":
        forms = ArtikelForm(request.POST, request.FILES)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.author = request.user
            pub.save()
            return redirect(reverse('artikel_list'))
        else:
            print(forms.errors)
    forms = ArtikelForm()
    context = {
        'title': 'Tambah Artikel',
        'forms': forms
    }
    return render(request, template_name, context)

@login_required
def artikel_detail(request, id_artikel):
    template_name = "dashboard/snippets/artikel/artikel_detail.html"
    artikel = Artikel.objects.get(id=id_artikel)
    context = {
        'title': 'Detail Artikel',
        'artikel': artikel, 
    }
    return render(request, template_name, context)

from django.urls import reverse

@login_required
def artikel_update(request, id_artikel):
    template_name = "dashboard/snippets/artikel/artikel_forms.html"
    artikel = Artikel.objects.get(id=id_artikel)

    if request.user.groups.filter(name='Operator').exists():
        pass
    elif artikel.author != request.user:
        return redirect('/')

    if request.method == "POST":
        forms = ArtikelForm(request.POST, request.FILES, instance=artikel)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.author = request.user
            pub.save()
            return redirect(reverse('artikel_list'))
        
    forms = ArtikelForm(instance=artikel)
    context = {
        'title': 'Update Artikel',
        'forms': forms
    }
    return render(request, template_name, context)


@login_required
def artikel_delete(request, id_artikel):
    try:
        artikel = Artikel.objects.get(id=id_artikel)
        if request.user.groups.filter(name='Operator').exists():
            pass
        else:
            if artikel.author != request.user:
                return redirect('/')
        artikel.delete()

    except Artikel.DoesNotExist:
        pass
    return redirect(reverse('artikel_list'))
