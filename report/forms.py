from django import forms


class StudentsFilterForm(forms.Form):
    ordering = forms.ChoiceField(widget=forms.RadioSelect(attrs={}),
                                 label="sort", required=False, choices=[
            ["last_name", "Фамилия arrow_drop_up"],
            ["-last_name", "Фамилия sort"],
            ["first_name", "Имя arrow_drop_up"],
            ["-first_name", "Имя sort"],
        ], )
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    iexact = forms.BooleanField(required=False, label="Полное совпадение",
                                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
