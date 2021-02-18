from rest_framework import viewsets

from App.models import ContactPeople
from App.serializers.contact_people_serializer import ContactPeopleSerializer
from App.views_constant import not_using


class ContactPeopleViewSet(viewsets.ModelViewSet):
    queryset = ContactPeople.objects.all()
    serializer_class = ContactPeopleSerializer

    # 改写原来的删除函数，使其变为假删
    def perform_destroy(self, instance):
        instance.status = not_using
        instance.save()
