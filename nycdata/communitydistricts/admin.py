from django import forms
from django.contrib import admin

from inplace.boundaries.models import Boundary

from .models import CommunityDistrictDetails


class CommunityDistrictDetailsForm(forms.ModelForm):
    district = forms.ModelChoiceField(
        queryset=Boundary.objects.filter(
            layer__name='community districts',
        ),
    )

    class Meta:
        fields = '__all__'
        model = CommunityDistrictDetails


class CommunityDistrictDetailsAdmin(admin.ModelAdmin):
    form = CommunityDistrictDetailsForm
    list_display = ('name', 'borough', 'district',)
    list_filters = ('borough',)
    search_fields = ('name',)


admin.site.register(CommunityDistrictDetails, CommunityDistrictDetailsAdmin)
