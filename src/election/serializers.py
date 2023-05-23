from rest_framework import serializers
from election.models import VoteReport


class VoteReportSerializer(serializers.ModelSerializer):
    box_number = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    def get_box_number(self, obj: VoteReport):
        return obj.box.number
    
    def get_city(self, obj: VoteReport):
        return obj.box.district.city.name
    
    def get_district(self, obj: VoteReport):
        return obj.box.district.name

    class Meta:
        model = VoteReport
        exclude = ("source_ip", "file", )