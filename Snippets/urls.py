from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name="home"),
    path('snippets/add', views.add_snippet_page, name="add_snip"),
    path('snippets/view', views.snippets_page, name="view_snip"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
