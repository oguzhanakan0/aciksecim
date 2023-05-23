from rest_framework import serializers
from election.models import Box

class BoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Box
        fields = "__all__"