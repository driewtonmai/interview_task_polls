from rest_framework import serializers

from .models import Poll


class ActivePollSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name=)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'start_date', 'end_date']