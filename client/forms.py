from django import forms


class OffreForm(forms.Form):
    OPTIONS = (
        ("AUT", "Automobile"),
        ("CIV", "RC Civile"),
        ("HAB", "Multirisque habitation"),
        ("ACC", "Individuel Accident"),
        ("VOY", "Voyage"),
        ("SCO", "RC Scolaire"),
        ("SAN", "Santé"),
        ("AVI", "Aviation"),
        ("MAR", "Maritime"),
        ("IND", "Industriel")
    )

    Offres = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)