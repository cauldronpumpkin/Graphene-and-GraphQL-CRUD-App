import graphene

from graphene_django.types import DjangoObjectType

from .models import Category, Ingredient

from django.shortcuts import get_object_or_404


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    category = graphene.Field(lambda: CategoryType)

    def mutate(root, info, name):
        category = Category.objects.create(name = name)
        return CreateCategory(category=category)

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class CreateIngredient(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        notes = graphene.String()
        category = graphene.String()
    
    ingredient = graphene.Field(lambda: IngredientType)

    def mutate(root, info, name, notes, category):
        category_queryset = Category.objects.all()
        
        found = False
        for instance in category_queryset:
            if category == instance.name:
                category_object = get_object_or_404(Category, name = category)
                found = True
                break
            else:
                continue
        if (found == False):
            category_object = Category.objects.create(name = category)
        ingredient = Ingredient.objects.create(name=name, notes=notes, category=category_object)
        return CreateIngredient(ingredient=ingredient)

class DeleteIngredient(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ingredient = graphene.Field(lambda: IngredientType)

    def mutate(root, info, name):
        ingredient = Ingredient.objects.get(name = name)
        ingredient.delete()
        return DeleteIngredient(ingredient=ingredient)

class UpdateIngredient(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        notes =  graphene.String()
        category = graphene.String()
    
    ingredient = graphene.Field(lambda: IngredientType)

    def mutate(root, info, name, notes, category):
        category_queryset = Category.objects.all()
        
        found = False
        for instance in category_queryset:
            if category == instance.name:
                category_object = get_object_or_404(Category, name = category)
                found = True
                break
            else:
                continue
        if (found == False):
            category_object = Category.objects.create(name = category)

        ingredient = Ingredient.objects.filter(name = name).update(notes=notes, category=category_object)

        return UpdateIngredient(ingredient = ingredient)

class Query(object):
      category = graphene.Field(CategoryType, id=graphene.Int(), name=graphene.String())
      all_categories = graphene.List(CategoryType)


      ingredient = graphene.Field(IngredientType, id=graphene.Int(), name=graphene.String())
      all_ingredients = graphene.List(IngredientType)

      def resolve_all_categories(self, info, **kwargs):
          return Category.objects.all()

      def resolve_all_ingredients(self, info, **kwargs):
          return Ingredient.objects.all()

      def resolve_category(self, info, **kwargs):
          id = kwargs.get('id')
          name = kwargs.get('name')

          if id is not None:
              return Category.objects.get(pk=id)

          if name is not None:
              return Category.objects.get(name=name)

          return None

      def resolve_ingredient(self, info, **kwargs):
          id = kwargs.get('id')
          name = kwargs.get('name')

          if id is not None:
              return Ingredient.objects.get(pk=id)

          if name is not None:
              return Ingredient.objects.get(name=name)

          return None

class MyMutations(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_ingredient = CreateIngredient.Field()
    delete_ingredient = DeleteIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
