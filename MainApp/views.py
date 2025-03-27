from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import SnippetForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
               'form': form}
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_snip")
        return render(request, "pages/add_snippet.html", {'form':form})
    


def snippets_page(request):
    snippets = Snippet.objects.all()
    snippets_count =  Snippet.objects.count()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets' : snippets      ,      
        'snippets_count': snippets_count}
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id: int):
    context = {"pagename": 'Просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id) 
    except ObjectDoesNotExist: 
        return HttpResponseNotFound(f"Snippet with id={snippet_id} not found")
    else: 
        context ["snippet"] = snippet
        context ["type"] = "view"
        return render(request, 'pages/snippet_detail.html', context)

def snippet_delete(request, snippet_id: int):
    if request.method in ("POST" , "GET"):
        snippet = get_object_or_404(Snippet, id=snippet_id) 
        snippet.delete()
    return redirect("list_snip")

def snippet_edit(request, snippet_id: int):
    context = {"pagename": 'редактирование сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id) 
    except ObjectDoesNotExist: 
        return Http404
    #variant1
    # if request.method == "GET":
    #     form = SnippetForm(instance=snippet)
    #     return render(request,"pages/add_snippet.html", {"form": form} )
    
    #variant2
    if request.method == "GET":
        context = {'snippet': snippet,
                   "type" : "edit"}
        return render(request, 'pages/snippet_detail.html', context)
    
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        # snippet.lang = data_form["lang"]
        snippet.code = data_form["code"]
        # snippet.creation_date = data_form["creation_date"]
        snippet.save()
        return redirect("list_snip")


# def create_snippet(request):
#     if request.method == "POST":
#         form = SnippetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("list_snip")
#         return render(request, "pages/add_snippet.html", {'form':form})


