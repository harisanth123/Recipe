from tkinter.tix import Form
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from rest_framework.response import Response
from rest_framework.decorators import api_view
from services.google import converter
from .serializers import InstructionSerializer, RecipeSerializer
from .models import Recipe
from .models import RecipeInstruction

from .forms import RecipeInstructionForms,RecipeCreationForm

from django.forms import formset_factory


def home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        posts=Post.title=q
    else:
        posts=Post.all()


def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@api_view(['GET'])
def getRecipeInfo(request):
    recipes  = Recipe.objects.all()
    serializer = RecipeSerializer(recipes,many = True)
    return Response(serializer.data)

# @api_view(['POST'])
def addRecipeInfo(request):
    if request.method == "POST":
        form = RecipeCreationForm(request.POST)
        print(form)
        if form.is_valid():
            recipe = form.save()
            id = recipe.id
            dict1={'id':id}        
            form = RecipeInstructionForms() 
            # Instructions = formset_factory(RecipeInstructionForms,extra=1)
            # formset =  Instructions()
            return render(request, 'blog/post_form.html', {'form': form, 'id':recipe, 'name':recipe.name})
    else:
        form = RecipeCreationForm()
    return render(request, 'blog/post_form.html', {'form': form,'name':''})

@api_view(['GET'])
def getRecipeInstruction(request):
    instructions  = RecipeInstruction.objects.all()
    serializer = InstructionSerializer(instructions,many = True)
    return Response(serializer.data)

# @api_view(['POST'])
def addRecipeInstruction(request):
    serializer =InstructionSerializer(data=request.data1)
    if serializer.is_valid():
        serializer.save()
    return render(request, 'blog/post_form.html')

    # return Response(serializer.data)
    
    # if request.method == "POST":
    #     Instructions = formset_factory(RecipeInstructionForms,extra=1)
    #     formset =  Instructions(request.POST)
    #     print(formset)
        
    #     if formset.is_valid():
    #         for form in formset:
    #             form.save()
    #     form = RecipeInstructionForms()
    #     return render(request, 'blog/post_form.html', {'form': form })
    # else:

@api_view(['GET'])
def play(request):
    r_idvalue= request.GET.get('r_id',None)
    v_data = RecipeInstruction.objects.filter(r_id=r_idvalue)
    v_data = list(v_data)
    v_data.sort(key=lambda x: x.seq_no)
    filename=converter(v_data)
    # serializer = InstructionSerializer(v_data,many = True)
    # return Response(serializer.data)
    context={"filepath":"/media/"+filename}
    return render(request,"index.html",context)


# def addRecipeInstruction(request):
#     form = RecipeInstructionForms(request.POST)
#     if request.method == 'POST':
#         print(form)
#         if form.is_valid():
#             form.save()
#         else:
#             print(form.errors)
#     return render(request,'blog/post_form.html',{'form':form})
