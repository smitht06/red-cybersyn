from django import forms

from .models import Character, CharacterGear, CharacterQuality, CharacterSkill


class CharacterForm(forms.ModelForm):
    """Form for creating and editing a Shadowrun character."""

    class Meta:
        model = Character
        fields = [
            "name",
            "alias",
            "metatype",
            "metatype_name",
            "magic_type",
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
            "karma",
            "nuyen",
            "magic",
            "resonance",
            "background",
            "notes",
        ]
        widgets = {
            "background": forms.Textarea(attrs={"rows": 4}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make metatype_name optional since metatype FK is preferred
        self.fields["metatype_name"].required = False
        # metatype FK is optional in the model (null=True, blank=True)
        self.fields["metatype"].required = False
        # These fields have model defaults; make them optional in the form
        for field in ["karma", "nuyen", "magic", "resonance"]:
            self.fields[field].required = False


class CharacterSkillForm(forms.ModelForm):
    """Form for adding a skill to a character."""

    class Meta:
        model = CharacterSkill
        fields = ["skill", "rating", "is_specialization"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 0, "max": 12}),
        }


class CharacterQualityForm(forms.ModelForm):
    """Form for adding a quality to a character."""

    class Meta:
        model = CharacterQuality
        fields = ["quality"]


class CharacterGearForm(forms.ModelForm):
    """Form for adding gear to a character."""

    class Meta:
        model = CharacterGear
        fields = ["gear", "quantity"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"min": 1}),
        }
