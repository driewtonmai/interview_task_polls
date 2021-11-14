from rest_framework import serializers

from .constants import TEXT, SELECT, MULTI_SELECT


def validate_question_type(validated_data, answer_options_data):
    question = validated_data['question']
    if question.type != TEXT:
        if validated_data.get('text'):
            raise serializers.ValidationError('У вопроса формата "multi-select" или "select" не может быть текста')

        if question.type == SELECT:
            if len(answer_options_data) != 1 or not answer_options_data:
                raise serializers.ValidationError('У вопроса формата "select" должен быть один вариант ответа')

    else:
        if not validated_data.get('text'):
            raise serializers.ValidationError('Пожалуйста напишите ответ к вопросу')
        if answer_options_data:
            raise serializers.ValidationError('У вопроса формата "text" не может быть опций')