from django import forms
from .models import (
    ShadowrunCharacter,
    CharacterSkill,
    CharacterQuality,
    Contact,
    Lifestyle,
    Skill,
    Quality,
    Gear,
    Weapon,
    Armor,
)


class CharacterCreateForm(forms.ModelForm):
    """Form for creating a new character"""

    class Meta:
        model = ShadowrunCharacter
        fields = ["name", "alias", "metatype", "magic_type"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Character Name"}
            ),
            "alias": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Street Name"}
            ),
            "metatype": forms.Select(attrs={"class": "form-select"}),
            "magic_type": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Character Name"
        self.fields["alias"].label = "Street Name / Alias"
        self.fields["metatype"].label = "Metatype"
        self.fields["magic_type"].label = "Awakened/Emerged Type"


class CharacterAttributeForm(forms.ModelForm):
    """Form for character attributes"""

    class Meta:
        model = ShadowrunCharacter
        fields = [
            "body",
            "agility",
            "reaction",
            "strength",
            "willpower",
            "logic",
            "intuition",
            "charisma",
            "edge",
            "essence",
        ]
        widgets = {
            "body": forms.NumberInput(
                attrs={"class": "form-control attribute-input", "min": 1, "max": 12}
            ),
            "agility": forms.NumberInput(
                attrs={"class": "form-control attribute-input", "min": 1, "max": 12}
            ),
            "reaction": forms.NumberInput(
                attrs={"class": "form-control attribute-input", "min": 1, "max": 12}
            ),
            "strength": forms.NumberInput(
                attrs={"class": "form-control attribute-input", "min": 1, "max": 12}
            ),
            "willpower": forms.NumberInput(
                attrs={"class": "form-control attribute-input", "min": 1, "max": 12}
            ),
            "logic": forms.NumberInput(
                attrs={"class": "form-control attribute-input", "min": 1, "max": 12}
            ),
            "intuition": forms.NumberInput(
                attrs={"class": "form-control attribute-input", "min": 1, "max": 12}
            ),
            "charisma": forms.NumberInput(
                attrs={"class": "form-control attribute-input", "min": 1, "max": 12}
            ),
            "edge": forms.NumberInput(
                attrs={"class": "form-control attribute-input", "min": 1, "max": 12}
            ),
            "essence": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "max": 6, "step": 0.1}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set min/max based on metatype
        if self.instance and self.instance.metatype:
            metatype = self.instance.metatype
            for field in [
                "body",
                "agility",
                "reaction",
                "strength",
                "willpower",
                "logic",
                "intuition",
                "charisma",
            ]:
                min_val = getattr(metatype, f"{field}_min", 1)
                max_val = getattr(metatype, f"{field}_max", 6)
                self.fields[field].widget.attrs["min"] = min_val
                self.fields[field].widget.attrs["max"] = max_val

            self.fields["edge"].widget.attrs["min"] = metatype.edge_min
            self.fields["edge"].widget.attrs["max"] = metatype.edge_max


class CharacterSkillForm(forms.Form):
    """Form for adding skills"""

    skill = forms.ModelChoiceField(
        queryset=Skill.objects.filter(is_knowledge_skill=False),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    rating = forms.IntegerField(
        min_value=1,
        max_value=12,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 12}),
    )
    specialization = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Specialization"}
        ),
    )


class CharacterQualityForm(forms.Form):
    """Form for selecting qualities"""

    quality = forms.ModelChoiceField(
        queryset=Quality.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class CharacterEquipmentForm(forms.Form):
    """Form for equipment selection"""

    GEAR_CHOICES = [
        ("gear", "Gear"),
        ("weapon", "Weapon"),
        ("armor", "Armor"),
    ]

    item_type = forms.ChoiceField(
        choices=GEAR_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    gear = forms.ModelChoiceField(
        queryset=Gear.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    weapon = forms.ModelChoiceField(
        queryset=Weapon.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    armor = forms.ModelChoiceField(
        queryset=Armor.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class CharacterContactForm(forms.ModelForm):
    """Form for contacts"""

    class Meta:
        model = Contact
        fields = [
            "name",
            "archetype",
            "connection_rating",
            "loyalty_rating",
            "description",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "archetype": forms.TextInput(attrs={"class": "form-control"}),
            "connection_rating": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 12}
            ),
            "loyalty_rating": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 12}
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class CharacterDetailsForm(forms.ModelForm):
    """Final character details"""

    class Meta:
        model = ShadowrunCharacter
        fields = [
            "age",
            "height",
            "weight",
            "description",
            "background",
            "character_concept",
        ]
        widgets = {
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "height": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., 180cm"}
            ),
            "weight": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., 75kg"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Physical description",
                }
            ),
            "background": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Character background story",
                }
            ),
            "character_concept": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Street Samurai, Face, Hacker",
                }
            ),
        }
