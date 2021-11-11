from django.contrib.auth import authenticate
from rest_framework import serializers


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