from wsgiref import validate
from rest_framework import serializers,exceptions
from django_countries.serializers import CountryFieldMixin
from user.api.serializers import UserLessInfoSerializer,SkillSerializer
from projects.models import *
from django.db import transaction
from drf_writable_nested.serializers import WritableNestedModelSerializer


class ProjectSerializer(CountryFieldMixin,WritableNestedModelSerializer):

    posted_by = UserLessInfoSerializer(read_only=True)
    desired_skills = SkillSerializer(many=True)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    expires_on = serializers.DateField()
    detail=serializers.CharField()
    status=serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ['id','title','posted_by','status','category','pricing_type','expires_on','start_date','end_date','desired_skills','detail','price','location']

    
    def create(self, validated_data):
        with transaction.atomic():
            skill_data = validated_data.pop('desired_skills',[])
            project = Project.objects.create(**validated_data)
            if len(skill_data):
                for i in skill_data:
                    skill,_ =DesiredExpertise.objects.get_or_create(skill_name=i["skill_name"])
                    project.desired_skills.add(skill)
            return project
    
    def update(self,instance, validated_data):
        from rest_framework.utils import  model_meta
        with transaction.atomic():
            #serializer update default code overriden to remove nested field
            #serializer update gives error when dealing nested field but we need it's capability to update all other fields
            info = model_meta.get_field_info(instance)
            skill_data = validated_data.pop('desired_skills',[])
            m2m_fields = []
            for attr, value in validated_data.items():
                if attr in info.relations and info.relations[attr].to_many:
                    m2m_fields.append((attr, value))
                else:
                    setattr(instance, attr, value)

            instance.save()
            for attr, value in m2m_fields:
                field = getattr(instance, attr)
                field.set(value)

            #updating related model
            skills = [DesiredExpertise.objects.get_or_create(skill_name= i["skill_name"])[0] for i in skill_data]
            instance.desired_skills.set(skills)
            return instance

    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise exceptions.APIException('Start date must be less than end date !')
        if (data['expires_on'] < data['start_date'] ) or (data['expires_on'] > data['end_date']):
            raise exceptions.APIException('Expire date must be between Start Date and End Date !')
        return data

            

class ReviewSerializer(CountryFieldMixin,serializers.ModelSerializer):

    review_by = UserLessInfoSerializer(read_only=True)
    review_to =UserLessInfoSerializer(read_only=True)

    class Meta:
        model = Reviews
        fields = '__all__'

    

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectCategory
        fields = '__all__'

class InviteSerializer(serializers.ModelSerializer):
    # project =ProjectSerializer(read_only=True)
    sent_by = UserLessInfoSerializer(read_only=True)
    sent_to = UserLessInfoSerializer(read_only=True,many=False)
    sent_to_id = serializers.IntegerField(required=False)
    project_id = serializers.IntegerField(required=False)
    answered = serializers.ReadOnlyField()
    accepted = serializers.ReadOnlyField()

    class Meta:
        model = InviteModel
        fields = '__all__'
