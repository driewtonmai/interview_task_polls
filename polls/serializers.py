from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Poll, Question, OptionChoices, Answer, AnswerOptions, UserSelectedPoll, Client
from .validators import validate_question_type


class ActivePollSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='polls:polls-detail')

    class Meta:
        model = Poll
        fields = ['url', 'id', 'name', 'description', 'start_date', 'end_date']


class OptionChoicesSerializersForActivePoll(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OptionChoices
        fields = ['id', 'text', 'question']
        extra_kwargs = {
            'question': {'write_only': True, 'required': False}
        }


class QuestionSerializerForActivePoll(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    option_choices = OptionChoicesSerializersForActivePoll(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'option_choices']


class ActivePollDetailSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializerForActivePoll(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'question_set']


class CreateAnswerOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOptions
        fields = ['option_choice']


class CreateAnswerSerializer(serializers.ModelSerializer):
    answeroptions_set = CreateAnswerOptionsSerializer(many=True, required=False)

    class Meta:
        model = Answer
        fields = ['id', 'text', 'question', 'user_selected_poll', 'answeroptions_set']
        validators = [
            UniqueTogetherValidator(
                queryset=Answer.objects.all(),
                fields=['question', 'user_selected_poll']
            )
        ]

    def create(self, validated_data):
        try:
            answer_options_data = validated_data.pop('answeroptions_set')
        except KeyError:
            answer_options_data = []

        validate_question_type(validated_data, answer_options_data)
        answer_instance = Answer.objects.create(**validated_data)
        for answer in answer_options_data:
            answer['answer'] = answer_instance
            AnswerOptions.objects.create(**answer)
        return answer_instance


class ClientSerializer(serializers.ModelSerializer):
    login = serializers.IntegerField()

    class Meta:
        model = Client
        fields = ['id', 'login']


class UserSelectedPollSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = UserSelectedPoll
        fields = ['id', 'poll', 'client']

    def create(self, validated_data):
        selected_poll_data = validated_data.pop('client')
        client, create = Client.objects.get_or_create(login=selected_poll_data['login'])

        if UserSelectedPoll.objects.filter(
                poll=validated_data['poll'], client=client).exists():
            raise serializers.ValidationError('Вы уже проходили за этот опрос')

        poll = UserSelectedPoll.objects.create(client=client, **validated_data)
        return poll


class ListClientResultsSerializer(serializers.ModelSerializer):
    poll = serializers.SlugRelatedField(read_only=True, slug_field='name')
    client = serializers.SlugRelatedField(read_only=True, slug_field='login')
    # detail = serializers.HyperlinkedIdentityField(view_name=)

    class Meta:
        model = UserSelectedPoll
        fields = ['id', 'client', 'poll']


class AnswerOptionsSerializer(serializers.ModelSerializer):
    option_choice = serializers.SlugRelatedField(queryset=AnswerOptions.objects.all(), slug_field='text')

    class Meta:
        model = AnswerOptions
        fields = ['id', 'option_choice']


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializerForActivePoll(read_only=True)
    answeroptions_set = AnswerOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ['text', 'question', 'answeroptions_set']
        depth = 1


class RetrieveClientResultsSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True, read_only=True)
    poll = serializers.SlugRelatedField(read_only=True, slug_field='name')
    client = serializers.SlugRelatedField(read_only=True, slug_field='login')

    class Meta:
        model = UserSelectedPoll
        fields = ['id', 'client', 'poll', 'answer_set']
        depth = 1