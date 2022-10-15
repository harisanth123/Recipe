from attr import fields
from rest_framework import serializers
from .models import Recipe
from .models import RecipeInstruction

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeInstruction
        fields = '__all__'
