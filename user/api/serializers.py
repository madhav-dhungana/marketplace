from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from projects.models import DesiredExpertise
from user.models import User, Languages
from django_countries.serializers import CountryFieldMixin
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction
from drf_writable_nested.serializers import WritableNestedModelSerializer


class UserLoginSerializers(serializers.Serializer):
    email = serializers.CharField(label='email')
    password = serializers.CharField(label='password')

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        # username = data['username']
        password = data['password']
        email = data['email']
        if not email and not password:
            raise ValidationError('No Credentials were given')
        return data


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesiredExpertise
        fields = ['id', 'skill_name']


class NameSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesiredExpertise
        fields = ['skill_name']


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    languages = LanguageSerializer(read_only=True, many=True)
    verified = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'display_name', 'avatar', 'banner_image', 'hourly_rate',
                  'verified', 'overview', 'country', 'address', 'gender', 'zipcode', 'state', 'skills', 'languages', 'role'
                  ]
        extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        with transaction.atomic():
            skill_data = validated_data.pop('skills', [])
            User.objects.filter(pk=instance.id).update(**validated_data)
            skills = [DesiredExpertise.objects.get_or_create(skill_name=i["skill_name"])[
                0] for i in skill_data]
            instance.skills.set(skills)
            user = User.objects.get(id=instance.id)
            return user


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255)
    password = serializers.CharField()
    role = serializers.CharField(max_length=255)


class UserLessInfoSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'display_name',
                  'country', 'skills', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}


class UserAdminSerializer(CountryFieldMixin, WritableNestedModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = User
        exclude = ["is_superuser", "last_login"]
        extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        from rest_framework.utils import model_meta
        with transaction.atomic():

            skill_data = validated_data.pop('skills', [])
            User.objects.filter(pk=instance.id).update(**validated_data)
            skills = [DesiredExpertise.objects.get_or_create(skill_name=i["skill_name"])[
                0] for i in skill_data]
            instance.skills.set(skills)
            user = User.objects.get(id=instance.id)
            return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['user'] = UserLessInfoSerializer(user, many=False).data
        return token
