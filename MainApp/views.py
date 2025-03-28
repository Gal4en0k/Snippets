from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required



def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required(login_url='home')

def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
               'form': form}
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit = False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("list_snip")
        return render(request, "pages/add_snippet.html", {'form':form})
    
def create_user(request):
    context = {'pagename': 'Регистрация нового пользователя'}
    if request.method == "GET":
        form =UserRegistrationForm()
        context['form'] = form
        return render(request, 'pages/registration.html', context)
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        context['form'] = form
        return render(request, "pages/registration.html",context)

def snippets_page(request):
    if request.user.is_authenticated:
        snippets = Snippet.objects.filter(is_public = True).union(Snippet.objects.filter(user = request.user))
        snippets_count =  snippets.count()
        context = {
            'pagename': 'Просмотр сниппетов',
            'snippets' : snippets      ,      
            'snippets_count': snippets_count}
        return render(request, 'pages/view_snippets.html', context)
    else:
        snippets = Snippet.objects.filter(is_public = True)
        snippets_count =  snippets.count()
        context = {
            'pagename': 'Просмотр сниппетов',
            'snippets' : snippets      ,      
            'snippets_count': snippets_count}
        return render(request, 'pages/view_snippets.html', context)

@login_required    
def snippets_my(request):
    # if request.user.is_authenticated:
    snippets = Snippet.objects.filter(user = request.user)
    snippets_count =  Snippet.objects.filter(user = request.user).count()
    if snippets_count > 0:
        context = {
            'pagename': 'Мои сниппеты',
            'snippets' : snippets      ,      
            'snippets_count': snippets_count}
        return render(request, 'pages/view_snippets.html', context)
    # Return error message - Вы не залогинены или У вас нет ни одного сниппета 
    # тогда показываем все - доработать здесь не срабатывает
    # snippets = Snippet.objects.all()
    # snippets_count =  Snippet.objects.count()  
    # return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id: int):
    context = {"pagename": 'Просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id) 
    except ObjectDoesNotExist: 
        return HttpResponseNotFound(f"Snippet with id={snippet_id} not found")
    else: 
        comments_form = CommentForm()
        context["snippet"] = snippet
        context["type"] = "view"
        context["comments_form"] = comments_form
        return render(request, 'pages/snippet_detail.html', context)

@login_required
def snippet_delete(request, snippet_id: int):
    if request.user.is_authenticated: 
        if request.method in ("POST" , "GET"):
            snippet = get_object_or_404(Snippet.object.filter(user=request.user), id=snippet_id) 
            if snippet.user == request.user:
                snippet.delete()
        return redirect("list_snip")
    else:
        return redirect("list_snip")

@login_required
def snippet_edit(request, snippet_id: int):
    if request.user.is_authenticated:
        context = {"pagename": 'редактирование сниппета'}
        try:
            snippet = Snippet.objects.get(id=snippet_id) 
            if  snippet.user != request.user:
                #сообщение об ошибке - вы пытаетесь править чужой сниппет
                return redirect("list_snip")   
        except ObjectDoesNotExist: 
            return Http404
    else:
        return redirect("list_snip")
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
        snippet.is_public = data_form.get("public",False)
        # snippet.creation_date = data_form["creation_date"]
        snippet.save()
        return redirect("list_snip")


        return render(request, "pages/add_snippet.html", {'form':form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
       # print("username =", username)
       # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                "pagename": "PythonBin",
                "errors": ['wrong username or password'],
            }
            return render(request, "pages/index.html", context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect("home")

@login_required
def comments_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get("snippet_id")
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect("detail_snip", snippet_id=snippet.id)
    return HttpResponseNotAllowed(['POST'])
