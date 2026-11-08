from rest_framework import serializers

from apps.taskmanager.models import Category

# Same text and shape as DRF's built-in UniqueValidator error for the name field
NAME_TAKEN_MESSAGE = "category with this name already exists."


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')

    def create(self, validated_data):
        name = validated_data.get('name')
        # all_objects: soft-deleted names are still taken by the unique constraint in the DB
        if Category.all_objects.filter(name=name).exists():
            raise serializers.ValidationError({'name': [NAME_TAKEN_MESSAGE]})
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        if Category.all_objects.filter(name=name).exclude(id=instance.id).exists():
            raise serializers.ValidationError({'name': [NAME_TAKEN_MESSAGE]})
        instance.name = name
        instance.save()
        return instance
