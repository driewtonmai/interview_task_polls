from rest_framework import serializers

from polls.constants import TEXT


def validate_type_for_create(validated_data):
    if validated_data['type'] != TEXT:
        if not validated_data.get('option_choices'):
            raise serializers.ValidationError('Пожалуйста заполните варианты ответа')
    elif validated_data['type'] == TEXT:
        if not validated_data.get('options'):
            raise serializers.ValidationError('У вопроса формата "текст" не должно быть дополнительных полей')


def validate_type_for_update(validated_data, choices_data):
    if validated_data['type'] != TEXT:
        if not validated_data.get('option_choices') and not choices_data:
            raise serializers.ValidationError('Пожалуйста заполните варианты ответа')
    elif validated_data['type'] == TEXT:
        if validated_data.get('option_choices') or choices_data:
            raise serializers.ValidationError('У вопроса формата "текст" не должно быть дополнительных полей')