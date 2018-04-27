from django import forms
from .models import KeyWord, ItemData, SearchTask


class KeywordForm(forms.ModelForm):
    class Meta:
        model = KeyWord
        fields = "__all__"


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchTask
        # fields = "__all__"
        exclude = ("create_time", )

