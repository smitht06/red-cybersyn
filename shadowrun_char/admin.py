from django.contrib import admin
from .models import (
    Metatype,
    MagicType,
    Skill,
    Quality,
    Spell,
    AdeptPower,
    Gear,
    Weapon,
    Armor,
    ShadowrunCharacter,
    CharacterSkill,
    CharacterQuality,
    CharacterAdeptPower,
    Cyberware,
    Bioware,
    CharacterCyberware,
    CharacterBioware,
    Contact,
    Lifestyle,
    CharacterLog,
)


class CharacterSkillInline(admin.TabularInline):
    model = CharacterSkill
    extra = 3


class CharacterQualityInline(admin.TabularInline):
    model = CharacterQuality
    extra = 2


class CharacterAdeptPowerInline(admin.TabularInline):
    model = CharacterAdeptPower
    extra = 1


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


@admin.register(Metatype)
class MetatypeAdmin(admin.ModelAdmin):
    list_display = ["name", "essence_max"]


@admin.register(MagicType)
class MagicTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "magic_max", "resonance_available"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "linked_attribute", "is_knowledge_skill"]
    list_filter = ["category", "is_knowledge_skill"]
    search_fields = ["name"]


@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "karmic_cost", "max_rank"]
    list_filter = ["type"]
    search_fields = ["name"]


@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "spell_type", "drain_code"]
    list_filter = ["category", "spell_type"]


@admin.register(AdeptPower)
class AdeptPowerAdmin(admin.ModelAdmin):
    list_display = ["name", "cost_per_rank", "max_rank", "activation_type"]
    search_fields = ["name"]


@admin.register(Gear)
class GearAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "cost", "availability"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "damage", "armor_penetration", "accuracy"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(Armor)
class ArmorAdmin(admin.ModelAdmin):
    list_display = ["name", "armor_rating", "social_penalty", "cost"]
    search_fields = ["name"]


@admin.register(ShadowrunCharacter)
class ShadowrunCharacterAdmin(admin.ModelAdmin):
    list_display = ["name", "alias", "metatype", "magic_type", "is_created"]
    list_filter = ["metatype", "magic_type", "is_created"]
    search_fields = ["name", "alias"]

    inlines = [
        CharacterSkillInline,
        CharacterQualityInline,
        CharacterAdeptPowerInline,
        ContactInline,
    ]

    fieldsets = (
        ("Basic Info", {"fields": ("name", "alias", "metatype", "magic_type", "age")}),
        (
            "Attributes",
            {
                "fields": (
                    "body",
                    "agility",
                    "reaction",
                    "strength",
                    "willpower",
                    "logic",
                    "intuition",
                    "charisma",
                    "edge",
                )
            },
        ),
        (
            "Derived Attributes",
            {
                "fields": (
                    "magic",
                    "resonance",
                    "essence",
                    "physical_track",
                    "stun_track",
                )
            },
        ),
        (
            "Initiative",
            {
                "fields": (
                    "initiative_physical",
                    "initiative_matrix",
                    "initiative_astral",
                )
            },
        ),
        ("Resources", {"fields": ("total_karma", "current_karma", "nuyen")}),
        (
            "Character Details",
            {
                "fields": (
                    "height",
                    "weight",
                    "description",
                    "background",
                    "character_concept",
                )
            },
        ),
        ("Status", {"fields": ("is_created",)}),
    )


@admin.register(Cyberware)
class CyberwareAdmin(admin.ModelAdmin):
    list_display = ["name", "essence_cost", "grade", "cost"]
    list_filter = ["grade"]
    search_fields = ["name"]


@admin.register(Bioware)
class BiowareAdmin(admin.ModelAdmin):
    list_display = ["name", "essence_cost", "grade", "cost"]
    list_filter = ["grade"]
    search_fields = ["name"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "character", "connection_rating", "loyalty_rating"]
    search_fields = ["name", "character__name"]


@admin.register(Lifestyle)
class LifestyleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "character",
        "lifestyle_type",
        "monthly_cost",
        "security_rating",
    ]
    list_filter = ["lifestyle_type"]


@admin.register(CharacterLog)
class CharacterLogAdmin(admin.ModelAdmin):
    list_display = [
        "character",
        "title",
        "log_type",
        "timestamp",
        "karma_change",
        "nuyen_change",
    ]
    list_filter = ["log_type", "timestamp"]
    search_fields = ["character__name", "title"]
