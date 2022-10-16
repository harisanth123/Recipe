from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from tracemalloc import Statistic
import django
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.home, name="blog-home"),
    path('', views.about, name="blog-about"),

    # path('home/', PostListView.as_view(), name="blog-home"),
    path('home/', PostListView.as_view(), name="blog-home"),
    path('post-new/', PostCreateView.as_view(), name="blog-new"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete"),
    path('getrecipeinfo/',view=views.getRecipeInfo),
    path('addrecipeinfo/',view=views.addRecipeInfo),
    path('getrecipeinstruction/',view=views.getRecipeInstruction),
    path('addrecipeinstruction/',view=views.addRecipeInstruction),
    path('play/<int:r_id>/',view=views.play,name="playss"),
    path('delete/<int:r_id>/',view=views.deleteRec,name="del"),
    path('search/',view=views.search,name="ser"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
