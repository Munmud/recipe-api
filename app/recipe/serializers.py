from rest_framework import serializers
from core.models import Tag, Ingridient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngridientSerializer(serializers.ModelSerializer):
    """Serializer for ingridient object"""

    class Meta:
        model = Ingridient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe Object"""
    ingridients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingridient.objects.all(),
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingridients', 'tags', 'time_minutes',
                  'price', 'link',)
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a Recipe details"""
    ingridients = IngridientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
