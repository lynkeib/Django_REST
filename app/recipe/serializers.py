from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ("id", "name",)
        read_only_fields = ("id",)


class IngredientsSerializer(serializers.ModelSerializer):
    """Serializer for ingredients objects"""

    class Meta:
        model = Ingredient
        fields = ("id", "name",)
        read_only_fields = ("id",)


class RecipesSerializer(serializers.ModelSerializer):
    """Serializer for recipes objects"""

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ("id", "title", "ingredients", "tags", "time_minutes", "price", "link",)
        read_only_fields = ("id",)
