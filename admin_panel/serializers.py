from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from polls.models import Poll, Question, OptionChoices

from .validators import validate_type_for_create, validate_type_for_update


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="email", write_only=True)
    password = serializers.CharField(label='password',
                                     style={'input_type': 'password'},
                                     write_only=True,
                                     trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            msg = 'Введенные данные неправильны.'
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


class OptionChoicesSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OptionChoices
        fields = ['id', 'text', 'question']
        extra_kwargs = {
            'question': {'write_only': True, 'required': False}
        }


class QuestionSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    poll = serializers.SlugRelatedField(read_only=True, slug_field='name')
    option_choices = OptionChoicesSerializers(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'poll', 'option_choices']


class QuestionCreateSerializer(serializers.ModelSerializer):
    option_choices = OptionChoicesSerializers(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'option_choices']

    def create(self, validated_data):
        validate_type_for_create(validated_data)
        try:
            choices_data = validated_data.pop('option_choices')
        except KeyError:
            choices_data = []
        question = Question.objects.create(**validated_data)
        for choice in choices_data:
            choice['question'] = question
            OptionChoices.objects.create(**choice)
        return question

    def update(self, instance, validated_data):
        try:
            choices_data = validated_data.pop('option_choices')
        except KeyError:
            choices_data = []

        validate_type_for_update(validated_data, choices_data)

        instance.type = validated_data.get('type', instance.type)
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        for choice in choices_data:
            choice_id = choice.get('id', None)
            if choice_id:
                choice_object = OptionChoices.objects.get(id=choice_id, question=instance)
                choice_object.text = choice.get('text', choice_object.text)
                choice_object.save()
            else:
                OptionChoices.objects.create(question=instance, **choice)
        return instance




