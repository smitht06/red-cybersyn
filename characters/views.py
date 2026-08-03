from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    CharacterForm,
    CharacterGearForm,
    CharacterQualityForm,
    CharacterSkillForm,
)
from .models import (
    Character,
    CharacterGear,
    CharacterQuality,
    CharacterSkill,
)


class CharacterOwnerMixin(UserPassesTestMixin):
    """Mixin that restricts access to the character's owner."""

    def test_func(self):
        obj = self.get_object()
        # Through models (CharacterSkill, CharacterQuality, CharacterGear)
        # have a `character` FK; the Character model has `owner` directly.
        if hasattr(obj, "character"):
            character = obj.character
        else:
            character = obj
        return character.owner == self.request.user


class CharacterListView(LoginRequiredMixin, ListView):
    """List all characters owned by the current user."""

    model = Character
    template_name = "characters/character_list.html"
    context_object_name = "characters"

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)


class CharacterDetailView(LoginRequiredMixin, CharacterOwnerMixin, DetailView):
    """Show a single character's full sheet."""

    model = Character
    template_name = "characters/character_detail.html"
    context_object_name = "character"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = self.get_object()
        context["skills"] = character.character_skills.select_related("skill").all()
        context["qualities"] = character.character_qualities.select_related(
            "quality"
        ).all()
        context["gear"] = character.character_gear.select_related("gear").all()
        context["spells"] = character.spells.all()
        return context


class CharacterCreateView(LoginRequiredMixin, CreateView):
    """Create a new character."""

    model = Character
    form_class = CharacterForm
    template_name = "characters/character_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CharacterUpdateView(LoginRequiredMixin, CharacterOwnerMixin, UpdateView):
    """Edit an existing character."""

    model = Character
    form_class = CharacterForm
    template_name = "characters/character_form.html"


class CharacterDeleteView(LoginRequiredMixin, CharacterOwnerMixin, DeleteView):
    """Delete a character."""

    model = Character
    template_name = "characters/character_confirm_delete.html"
    success_url = reverse_lazy("characters:list")


# ---- Related item management views ----


class CharacterSkillCreateView(LoginRequiredMixin, CharacterOwnerMixin, CreateView):
    """Add a skill to a character."""

    model = CharacterSkill
    form_class = CharacterSkillForm
    template_name = "characters/character_skill_form.html"

    def get_character(self):
        return get_object_or_404(Character, pk=self.kwargs["pk"])

    def get_object(self, queryset=None):
        return self.get_character()

    def form_valid(self, form):
        form.instance.character = self.get_character()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("characters:detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.get_character()
        return context


class CharacterSkillDeleteView(LoginRequiredMixin, CharacterOwnerMixin, DeleteView):
    """Remove a skill from a character."""

    model = CharacterSkill
    template_name = "characters/character_skill_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "characters:detail", kwargs={"pk": self.object.character.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.object.character
        return context


class CharacterQualityCreateView(LoginRequiredMixin, CharacterOwnerMixin, CreateView):
    """Add a quality to a character."""

    model = CharacterQuality
    form_class = CharacterQualityForm
    template_name = "characters/character_quality_form.html"

    def get_character(self):
        return get_object_or_404(Character, pk=self.kwargs["pk"])

    def get_object(self, queryset=None):
        return self.get_character()

    def form_valid(self, form):
        form.instance.character = self.get_character()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("characters:detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.get_character()
        return context


class CharacterQualityDeleteView(LoginRequiredMixin, CharacterOwnerMixin, DeleteView):
    """Remove a quality from a character."""

    model = CharacterQuality
    template_name = "characters/character_quality_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "characters:detail", kwargs={"pk": self.object.character.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.object.character
        return context


class CharacterGearCreateView(LoginRequiredMixin, CharacterOwnerMixin, CreateView):
    """Add gear to a character."""

    model = CharacterGear
    form_class = CharacterGearForm
    template_name = "characters/character_gear_form.html"

    def get_character(self):
        return get_object_or_404(Character, pk=self.kwargs["pk"])

    def get_object(self, queryset=None):
        return self.get_character()

    def form_valid(self, form):
        form.instance.character = self.get_character()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("characters:detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.get_character()
        return context


class CharacterGearDeleteView(LoginRequiredMixin, CharacterOwnerMixin, DeleteView):
    """Remove gear from a character."""

    model = CharacterGear
    template_name = "characters/character_gear_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "characters:detail", kwargs={"pk": self.object.character.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.object.character
        return context
