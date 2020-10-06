import uuid

from rest_framework import serializers

from App.models import ContactPeople


class ContactPeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactPeople
        fields = '__all__'
        read_only_fields = ('aid',)

    def create(self, validated_data):

        instance = ContactPeople()

        instance.aid = uuid.uuid4().hex
        instance.contact_person = validated_data.get('contact_person')
        instance.contact_position = validated_data.get('contact_position')
        instance.contact_tel = validated_data.get('contact_tel')
        instance.client_id = validated_data.get('client_id')
        instance.remark = validated_data.get('remark')

        instance.save()

        return instance
