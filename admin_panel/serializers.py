from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator

from polls.models import Poll, Question, QuestionOptions, OptionChoices


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="email", write_only=True)
    password = serializers.CharField(label='password',
                                     style={'input_type': 'password'},
                                     write_only=True,
                                     trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                msg = 'Введенные данные неправильны.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Пожалуйста введите логин и пароль'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class PollListSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'start_date', 'end_date',
                  'created_by']


class PollCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'draft']

        validators = [
            UniqueTogetherValidator(
                queryset=Poll.objects.all(),
                fields=['name', 'start_date']
            )
        ]

    def update(self, instance, validated_data):
        if validated_data.get('start_date'):
            raise serializers.ValidationError('Вы не можете изменять дату старта')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance


class PollDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'draft',
                  'created_by', 'created_at', 'updated_at']

