from ast import keyword
from dis import Instruction
from multiprocessing import context
from tkinter.tix import Form
from unittest import result
from urllib import request
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
import json

from .forms import RecipeCreationForm

from django.contrib.auth.models import User



def home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        posts=Post.title=q
    else:
        posts=Post.all()


def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})


class PostListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = RecipeInstruction
    template_name = 'blog/post_detail.html'


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
    model = Recipe
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
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            id = recipe.id            
            return render(request, 'blog/post_form.html', {'id':id, 'name':recipe.name})
    else:
        form = RecipeCreationForm()
    return render(request, 'blog/post_form.html', {'form': form,'name':''})

@api_view(['GET'])
def getRecipeInstruction(request):
    instructions  = RecipeInstruction.objects.all()
    serializer = InstructionSerializer(instructions,many = True)
    return Response(serializer.data)


def addRecipeInstruction(request):
    if request.method == "POST":
        requestData=json.loads(request.body.decode('UTF-8'))
        recipe = Recipe.objects.get(id=requestData["r_id"])
        requestData["r_id"] = recipe
        instruction = RecipeInstruction(**requestData)
        instruction.save()
        return redirect("")
    return render(request, 'blog/post_form.html')


def search(request):
    keyword = request.GET.get("keyword")
    posts = Recipe.objects.filter(name__icontains=keyword)
    print(posts)
    context = {"posts":posts, "keyword":keyword}
    return render(request,'blog/home.html',context)



def play(request,r_id):
    recipe = Recipe.objects.get(id=r_id)
    v_data = RecipeInstruction.objects.filter(r_id=r_id)
    v_data = list(v_data)
    v_data.sort(key=lambda x: x.seq_no)
    filename=converter(v_data)
    instructions  = RecipeInstruction.objects.all()
    # serializer = InstructionSerializer(v_data,many = True)
    # return Response(serializer.data)
    context={"filepath":"/media/"+filename,"instructions":v_data, "recipe":recipe}
    return render(request,"blog/play.html",context)


def deleteRec(request,r_id):
    RecipeInstruction.objects.filter(r_id=r_id).delete()
    Recipe.objects.get(id=r_id).delete()
    return redirect("/home/")

