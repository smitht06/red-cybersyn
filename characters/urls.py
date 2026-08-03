from django.urls import path

from .views import (
    CharacterCreateView,
    CharacterDeleteView,
    CharacterDetailView,
    CharacterGearCreateView,
    CharacterGearDeleteView,
    CharacterListView,
    CharacterQualityCreateView,
    CharacterQualityDeleteView,
    CharacterSkillCreateView,
    CharacterSkillDeleteView,
    CharacterUpdateView,
)

app_name = "characters"

urlpatterns = [
    path("", CharacterListView.as_view(), name="list"),
    path("new/", CharacterCreateView.as_view(), name="create"),
    path("<int:pk>/", CharacterDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", CharacterUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", CharacterDeleteView.as_view(), name="delete"),
    # Skills
    path("<int:pk>/skills/add/", CharacterSkillCreateView.as_view(), name="skill_add"),
    path(
        "skills/<int:pk>/delete/",
        CharacterSkillDeleteView.as_view(),
        name="skill_delete",
    ),
    # Qualities
    path(
        "<int:pk>/qualities/add/",
        CharacterQualityCreateView.as_view(),
        name="quality_add",
    ),
    path(
        "qualities/<int:pk>/delete/",
        CharacterQualityDeleteView.as_view(),
        name="quality_delete",
    ),
    # Gear
    path("<int:pk>/gear/add/", CharacterGearCreateView.as_view(), name="gear_add"),
    path(
        "gear/<int:pk>/delete/",
        CharacterGearDeleteView.as_view(),
        name="gear_delete",
    ),
]
