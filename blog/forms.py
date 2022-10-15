from dataclasses import fields
from pyexpat import model
from .models import Recipe,RecipeInstruction
from django import forms


class RecipeCreationForm(forms.ModelForm):
    name = forms.CharField()
    class Meta:
        model = Recipe
        fields = ['name']

class RecipeInstructionForms(forms.ModelForm):
    r_id = forms.IntegerField()
    time_stamp = forms.CharField()
    seq_no = forms.IntegerField()
    instruction = forms.CharField(max_length=200)
    class Meta:
        model =  RecipeInstruction
        fields = ['r_id','time_stamp','seq_no','instruction'] 