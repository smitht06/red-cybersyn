from django.urls import path
from . import views

app_name = "shadowrun_char"

urlpatterns = [
    # Home
    path("", views.CharacterGeneratorHome.as_view(), name="home"),
    # Create character
    path("create/", views.CharacterCreateView.as_view(), name="create"),
    path("random/", views.RandomCharacterGenerator.as_view(), name="random"),
    # Character steps
    path(
        "<int:pk>/attributes/",
        views.CharacterAttributeView.as_view(),
        name="character_attributes",
    ),
    path(
        "<int:pk>/skills/", views.CharacterSkillsView.as_view(), name="character_skills"
    ),
    path(
        "<int:pk>/qualities/",
        views.CharacterQualitiesView.as_view(),
        name="character_qualities",
    ),
    path(
        "<int:pk>/equipment/",
        views.CharacterEquipmentView.as_view(),
        name="character_equipment",
    ),
    path(
        "<int:pk>/details/",
        views.CharacterDetailsView.as_view(),
        name="character_details",
    ),
    # Character sheet and PDF
    path("<int:pk>/sheet/", views.CharacterSheetView.as_view(), name="character_sheet"),
    path("<int:pk>/pdf/", views.GeneratePDFView.as_view(), name="pdf"),
    # HTMX endpoints for attributes
    path(
        "<int:pk>/random-attributes/",
        views.RandomAttributeGenerator.as_view(),
        name="random_attributes",
    ),
    # HTMX endpoints for skills
    path("<int:pk>/add-skill/", views.AddSkillView.as_view(), name="add_skill"),
    path(
        "<int:pk>/remove-skill/<int:skill_pk>/",
        views.RemoveSkillView.as_view(),
        name="remove_skill",
    ),
    # HTMX endpoints for qualities
    path("<int:pk>/add-quality/", views.AddQualityView.as_view(), name="add_quality"),
    path(
        "<int:pk>/remove-quality/<int:quality_pk>/",
        views.RemoveQualityView.as_view(),
        name="remove_quality",
    ),
    # HTMX endpoints for equipment
    path("<int:pk>/add-gear/", views.AddGearView.as_view(), name="add_gear"),
    path(
        "<int:pk>/remove-gear/<str:item_type>/<int:item_id>/",
        views.RemoveGearView.as_view(),
        name="remove_gear",
    ),
    # Character management
    path("my-characters/", views.CharacterListView.as_view(), name="character_list"),
    path(
        "<int:pk>/delete/", views.DeleteCharacterView.as_view(), name="delete_character"
    ),
]
