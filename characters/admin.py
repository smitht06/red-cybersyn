from django.contrib import admin

from .models import (
    Character,
    CharacterGear,
    CharacterQuality,
    CharacterSkill,
    Gear,
    Metatype,
    Quality,
    Skill,
    Spell,
)


class CharacterSkillInline(admin.TabularInline):
    model = CharacterSkill
    extra = 0


class CharacterQualityInline(admin.TabularInline):
    model = CharacterQuality
    extra = 0


class CharacterGearInline(admin.TabularInline):
    model = CharacterGear
    extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "owner",
        "metatype_name",
        "magic_type",
        "updated_at",
    ]
    list_filter = ["metatype_name", "magic_type"]
    search_fields = ["name", "alias", "owner__username", "owner__email"]
    inlines = [CharacterSkillInline, CharacterQualityInline, CharacterGearInline]
    filter_horizontal = ["spells"]


@admin.register(Metatype)
class MetatypeAdmin(admin.ModelAdmin):
    list_display = ["name", "body_mod", "agility_mod", "strength_mod", "edge_mod"]
    search_fields = ["name"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "skill_type", "linked_attribute"]
    list_filter = ["skill_type"]
    search_fields = ["name"]


@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    list_display = ["name", "quality_type", "karma_cost"]
    list_filter = ["quality_type"]
    search_fields = ["name"]


@admin.register(Gear)
class GearAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "availability", "cost"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
    list_display = ["name", "spell_type", "drain"]
    list_filter = ["spell_type"]
    search_fields = ["name"]
