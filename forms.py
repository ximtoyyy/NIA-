from django import forms
from .models import SubAllotmentAdvice, AllotmentStatement


class SubAllotmentAdviceForm(forms.ModelForm):
    class Meta:
        model = SubAllotmentAdvice
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'advice_number':
                field.required = False
        if not self.instance.pk:
            self.fields['calendar_year'].initial = 2025
            self.fields['region'].initial = '13'
            self.fields['fund_code'].initial = '501'
            self.fields['to_office'].initial = 'REGIONAL IRRIGATION MANAGER'
            self.fields['total_amount'].initial = 0

def clean_advice_number(self):
    value = self.cleaned_data.get('advice_number')
    qs = SubAllotmentAdvice.objects.filter(advice_number=value)
    if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)
    if qs.exists():
        # Auto-append a copy number: 501-2026-140-CARP (2), (3), etc.
        count = 2
        new_value = f"{value} ({count})"
        while SubAllotmentAdvice.objects.filter(advice_number=new_value).exists():
            count += 1
            new_value = f"{value} ({count})"
        return new_value
    return value

class AllotmentStatementForm(forms.ModelForm):
    class Meta:
        model = AllotmentStatement
        fields = ['project_name', 'ada_number',
                  'allotment_received', 'ada_received', 'object_code', 'date', 'remarks']
        widgets = {
            'sub_allotment_record': forms.Select(attrs={'class': 'af-input', 'id': 'id_sub_allotment_record'}),
            'project_name':         forms.HiddenInput(attrs={'id': 'id_project_name'}),
            'ada_number':           forms.HiddenInput(attrs={'id': 'id_ada_number'}),
            'allotment_received':   forms.HiddenInput(attrs={'id': 'id_allotment_received'}),
            'ada_received':         forms.HiddenInput(attrs={'id': 'id_ada_received'}),
            'object_code':          forms.HiddenInput(attrs={'id': 'id_object_code'}),
            'date':                 forms.DateInput(attrs={'type': 'date', 'class': 'af-input'}),
            'remarks':              forms.Textarea(attrs={'class': 'af-input', 'rows': 3, 'placeholder': 'Optional remarks...'}),
        }

   
