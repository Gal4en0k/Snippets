from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from MainApp.forms import SnippetForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    form = SnippetForm()
    context = {'pagename': 'Добавление нового сниппета',
               'form': form}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    snippets_count =  Snippet.objects.count()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets' : snippets      ,      
        'snippets_count': snippets_count}
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id: int):
    try:
        snippet = Snippet.objects.get(id=snippet_id) 
    except ObjectDoesNotExist: 
        return HttpResponseNotFound(f"Snippet with id={snippet_id} not found")
    else: 
        context = {
        'pagename': 'Просмотр сниппета',
        "snippet": snippet}
    return render(request, 'pages/snippet_detail.html', context)

def create_snippet(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_snip")
        return render(request, "pages/add_snippet.html", {'form':form})


