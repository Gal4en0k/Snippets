from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name="home"),
    path('snippets/add', views.add_snippet_page, name="add_snip"),
    path('snippets/list', views.snippets_page, name="list_snip"),
    path('snippets/<int:snippet_id>', views.snippet_detail, name="detail_snip"),
    path('snippets/create', views.create_snippet, name="create_snip")
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 