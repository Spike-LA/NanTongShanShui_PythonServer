import django_filters

from App.models import Client


class ClientFilter(django_filters.FilterSet):

    class Meta:
        model = Client
        fields = ['client_unit', 'aid']
