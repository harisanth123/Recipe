from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from services.google import converter
from .serializers import InstructionSerializer, RecipeSerializer
from base.models import Recipe
from base.models import RecipeInstruction


@api_view(['GET'])
def getRecipeInfo(request):
    recipes  = Recipe.objects.all()
    serializer = RecipeSerializer(recipes,many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addRecipeInfo(request):
    serializer = RecipeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getRecipeInstruction(request):
    instructions  = RecipeInstruction.objects.all()
    serializer = InstructionSerializer(instructions,many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addRecipeInstruction(request):
    serializer =InstructionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

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
    



