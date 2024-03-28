from rest_framework import serializers
from courses.models import *

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image']  = instance.image.url
        return req


class CourseSerializer (ItemSerializer):
    class Meta:
        model = Course
        fields = ['id','name', 'image', 'created_date']


class LessonSerializer (ItemSerializer):
    class Meta:
        model = Lesson
        fields = ['id','subject', 'image', 'created_date']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']



class LessionDetailSerializer(LessonSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content','tags']


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['avatar']  = instance.avatar.url
        return req

    def create(self, validated_data):
        data = validated_data.copy() #deep copy
        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u


    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password','avatar']
        extra_kwargs = { # chi dc doc password
            'password': {
                'write_only': True
            }
        }