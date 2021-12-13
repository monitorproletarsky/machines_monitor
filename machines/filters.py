import django_filters
from django import forms
from .models import Equipment, ClassifiedInterval


class EquipmentFilter(django_filters.FilterSet):
    class Meta:
        model = Equipment
        fields = [
            'workshop',
            'model',
	        'machine_or_furnace_sign',
            'area',
        ]
        attrs = {'class': 'sr-only'}


# for a perspective
class ClassifiedIntervalFilter(django_filters.FilterSet):
    empty_only = django_filters.BooleanFilter(field_name='user_classification',
                                              widget=forms.CheckboxInput,
                                              label='Без причины простоя',
                                              method='filter_empty_only'
                                              )

    def filter_empty_only(self, queryset, name, value):
        if value:
            return queryset.filter(user_classification__isnull=True)
        else:
            return queryset

    class Meta:
        model = ClassifiedInterval
        fields = {
            'equipment': ['exact'],
            'start': ['gte'],
        }


class StatisticsFilter(django_filters.FilterSet):
    """
    For statistics purposes
    """
    PERIODS = [
        ['прошлая неделя', 'За прошедшую неделю'],
        ['прошлая декада', 'За прошедшую декаду'],
        ['прошлый месяц', 'За прошедший месяц'],
        ['текущий месяц', 'За текущий месяц'],
    ]
    periods_selector = django_filters.ChoiceFilter(choices=PERIODS, label='Период')
    start_date = django_filters.DateFilter(field_name='end', lookup_expr='gte', label='Начало')
    end_date = django_filters.DateFilter(field_name='start', lookup_expr='lte', label='Конец')

    class Meta:
        model = ClassifiedInterval
        fields = []


class calendar_repair(django_filters.FilterSet):

    start_date = django_filters.DateFilter(field_name='end', lookup_expr='gte', label='Начало')
    end_date = django_filters.DateFilter(field_name='start', lookup_expr='lte', label='Конец')
