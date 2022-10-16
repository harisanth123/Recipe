from django.contrib import admin


from .models import Recipe,RecipeInstruction

admin.site.register(Recipe)
admin.site.register(RecipeInstruction)
