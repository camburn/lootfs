from django import forms

from .models import Player, Item


class ItemChoiceIterator(forms.models.ModelChoiceIterator):
    def __iter__(self):
        queryset = self.queryset.select_related('dropped_by').order_by('dropped_by__dungeon__name', 'name')
        groups = groupby(queryset, key=lambda x: x.dropped_by.dungeon.name)
        for country, cities in groups:
            yield [
                country.name,
                [
                    (city.id, city.name)
                    for city in cities
                ]
            ]

class ItemChoiceField(forms.models.ModelChoiceField):
    iterator = ItemChoiceIterator

    def __init__(self, *args, **kwargs):
        super().__init__(City.objects.all(), *args, **kwargs)


class LootListForm(forms.Form):
    '''
    def __init__(self, *args, **kwargs):
        super(LootListForm, self).__init__(*args, **kwargs)

        self.fields['item_one'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return obj.wowhead_link
    '''

    #TODO: This should be based on your auth
    player_name = forms.ModelChoiceField(queryset=Player.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': "selectpicker", "data-live-search": "true", "data-width": "100%"})
    )

    item_one = forms.ModelChoiceField(
        queryset=Item.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': "selectpicker", "data-live-search": "true", "data-width": "100%"})
    )
    item_two = forms.ModelChoiceField(
        queryset=Item.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': "selectpicker", "data-live-search": "true", "data-width": "100%"})
    )
    item_three = forms.ModelChoiceField(
        queryset=Item.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': "selectpicker", "data-live-search": "true", "data-width": "100%"})
    )
    item_four = forms.ModelChoiceField(
        queryset=Item.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': "selectpicker", "data-live-search": "true", "data-width": "100%"})
    )
    item_five = forms.ModelChoiceField(
        queryset=Item.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': "selectpicker", "data-live-search": "true", "data-width": "100%"})
    )


class LogSubmitForm(forms.Form):
    ''' '''
    log_url = forms.URLField()
