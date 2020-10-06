from rest_framework import viewsets

from App.models import ContactPeople
from App.serializers.contact_people_serializer import ContactPeopleSerializer


class ContactPeopleViewSet(viewsets.ModelViewSet):
    queryset = ContactPeople.objects.all()
    serializer_class = ContactPeopleSerializer
