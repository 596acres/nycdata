from django import forms
from django.contrib import admin

from inplace.boundaries.models import Boundary

from .models import CityCouncilMember


class CityCouncilMemberForm(forms.ModelForm):
    district = forms.ModelChoiceField(
        queryset=Boundary.objects.filter(
            layer__name='city council districts',
        ),
    )

    class Meta:
        fields = '__all__'
        model = CityCouncilMember


class CityCouncilMemberAdmin(admin.ModelAdmin):
    form = CityCouncilMemberForm
    list_display = ('name', 'district',)
    search_fields = ('name',)


admin.site.register(CityCouncilMember, CityCouncilMemberAdmin)
