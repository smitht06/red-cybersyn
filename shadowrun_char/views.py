import random
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    FormView,
    View,
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib import messages
from django.template.loader import get_template
from weasyprint import HTML
import tempfile

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
from .forms import (
    CharacterCreateForm,
    CharacterAttributeForm,
    CharacterSkillForm,
    CharacterQualityForm,
    CharacterEquipmentForm,
    CharacterContactForm,
    CharacterDetailsForm,
)


class CharacterGeneratorHome(TemplateView):
    """Home page for the character generator"""

    template_name = "shadowrun_char/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character_ids = self.request.session.get("character_ids", [])
        context["recent_characters"] = ShadowrunCharacter.objects.filter(
            pk__in=character_ids
        ).order_by("-created_at")[:5]
        return context


class CharacterCreateView(CreateView):
    """Step 1: Create a new character with basic info"""

    model = ShadowrunCharacter
    form_class = CharacterCreateForm
    template_name = "shadowrun_char/character_create.html"

    def form_valid(self, form):
        self.object = form.save()
        # Store character ID in session
        if "character_ids" not in self.request.session:
            self.request.session["character_ids"] = []
        self.request.session["character_ids"].append(self.object.pk)
        self.request.session.modified = True

        # Redirect to attribute setup with character ID
        return redirect("shadowrun_char:character_attributes", pk=self.object.pk)


class CharacterAttributeView(UpdateView):
    """Step 2: Set character attributes"""

    model = ShadowrunCharacter
    form_class = CharacterAttributeForm
    template_name = "shadowrun_char/character_attributes.html"

    def get_success_url(self):
        return reverse_lazy(
            "shadowrun_char:character_skills", kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["metatype"] = self.object.metatype
        context["total_attribute_points"] = self.calculate_attribute_points()
        return context

    def calculate_attribute_points(self):
        """Calculate available attribute points based on metatype"""
        metatype = self.object.metatype
        if metatype.name == "human":
            return 24
        elif metatype.name == "elf":
            return 22
        elif metatype.name == "dwarf":
            return 20
        elif metatype.name == "ork":
            return 20
        elif metatype.name == "troll":
            return 18
        return 24


class RandomAttributeGenerator(View):
    """HTMX endpoint for random attribute generation"""

    def post(self, request, pk):
        character = get_object_or_404(ShadowrunCharacter, pk=pk)
        metatype = character.metatype

        # Generate random attributes within metatype limits
        attributes = {
            "body": random.randint(metatype.body_min, min(metatype.body_max, 6)),
            "agility": random.randint(
                metatype.agility_min, min(metatype.agility_max, 6)
            ),
            "reaction": random.randint(
                metatype.reaction_min, min(metatype.reaction_max, 6)
            ),
            "strength": random.randint(
                metatype.strength_min, min(metatype.strength_max, 6)
            ),
            "willpower": random.randint(
                metatype.willpower_min, min(metatype.willpower_max, 6)
            ),
            "logic": random.randint(metatype.logic_min, min(metatype.logic_max, 6)),
            "intuition": random.randint(
                metatype.intuition_min, min(metatype.intuition_max, 6)
            ),
            "charisma": random.randint(
                metatype.charisma_min, min(metatype.charisma_max, 6)
            ),
            "edge": random.randint(metatype.edge_min, min(metatype.edge_max, 6)),
        }

        # Update character
        for attr, value in attributes.items():
            setattr(character, attr, value)
        character.save()

        return render_to_string(
            "shadowrun_char/partials/attribute_form.html",
            {
                "form": CharacterAttributeForm(instance=character),
                "character": character,
            },
            request=request,
        )


class CharacterSkillsView(UpdateView):
    """Step 3: Add skills to character"""

    model = ShadowrunCharacter
    form_class = CharacterSkillForm
    template_name = "shadowrun_char/character_skills.html"

    def get_success_url(self):
        return reverse_lazy(
            "shadowrun_char:character_qualities", kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skills"] = Skill.objects.filter(is_knowledge_skill=False)
        context["knowledge_skills"] = Skill.objects.filter(is_knowledge_skill=True)
        context["character_skills"] = CharacterSkill.objects.filter(
            character=self.object
        )
        return context


class AddSkillView(View):
    """HTMX endpoint to add a skill to character"""

    def post(self, request, pk):
        character = get_object_or_404(ShadowrunCharacter, pk=pk)
        skill_id = request.POST.get("skill_id")
        rating = int(request.POST.get("rating", 1))
        specialization = request.POST.get("specialization", "")

        skill = get_object_or_404(Skill, pk=skill_id)

        # Check if skill already exists
        existing_skill = CharacterSkill.objects.filter(
            character=character, skill=skill
        ).first()

        if existing_skill:
            existing_skill.rating = rating
            existing_skill.specialization = specialization
            existing_skill.save()
        else:
            CharacterSkill.objects.create(
                character=character,
                skill=skill,
                rating=rating,
                specialization=specialization,
            )

        # Return updated skill list
        skills = CharacterSkill.objects.filter(character=character)
        return render_to_string(
            "shadowrun_char/partials/skill_list.html",
            {"character_skills": skills, "character": character},
            request=request,
        )


class RemoveSkillView(View):
    """HTMX endpoint to remove a skill"""

    def delete(self, request, pk, skill_pk):
        character = get_object_or_404(ShadowrunCharacter, pk=pk)
        CharacterSkill.objects.filter(character=character, pk=skill_pk).delete()

        skills = CharacterSkill.objects.filter(character=character)
        return render_to_string(
            "shadowrun_char/partials/skill_list.html",
            {"character_skills": skills, "character": character},
            request=request,
        )


class CharacterQualitiesView(UpdateView):
    """Step 4: Add qualities"""

    model = ShadowrunCharacter
    form_class = CharacterQualityForm
    template_name = "shadowrun_char/character_qualities.html"

    def get_success_url(self):
        return reverse_lazy(
            "shadowrun_char:character_equipment", kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["positive_qualities"] = Quality.objects.filter(type="positive")
        context["negative_qualities"] = Quality.objects.filter(type="negative")
        context["character_qualities"] = CharacterQuality.objects.filter(
            character=self.object
        )
        context["total_karma"] = self.calculate_karma()
        return context

    def calculate_karma(self):
        """Calculate karma based on qualities"""
        qualities = CharacterQuality.objects.filter(character=self.object)
        total = 25  # Starting karma
        for cq in qualities:
            if cq.quality.type == "positive":
                total -= cq.quality.karmic_cost
            else:
                total += cq.quality.karmic_cost
        return total


class AddQualityView(View):
    """HTMX endpoint to add quality"""

    def post(self, request, pk):
        character = get_object_or_404(ShadowrunCharacter, pk=pk)
        quality_id = request.POST.get("quality_id")
        quality = get_object_or_404(Quality, pk=quality_id)

        CharacterQuality.objects.get_or_create(
            character=character, quality=quality, defaults={"rating": 1}
        )

        qualities = CharacterQuality.objects.filter(character=character)
        return render_to_string(
            "shadowrun_char/partials/quality_list.html",
            {
                "character_qualities": qualities,
                "character": character,
            },
            request=request,
        )


class RemoveQualityView(View):
    """HTMX endpoint to remove quality"""

    def delete(self, request, pk, quality_pk):
        character = get_object_or_404(ShadowrunCharacter, pk=pk)
        CharacterQuality.objects.filter(character=character, pk=quality_pk).delete()

        qualities = CharacterQuality.objects.filter(character=character)
        return render_to_string(
            "shadowrun_char/partials/quality_list.html",
            {"character_qualities": qualities, "character": character},
            request=request,
        )


class CharacterEquipmentView(UpdateView):
    """Step 5: Add equipment"""

    model = ShadowrunCharacter
    form_class = CharacterEquipmentForm
    template_name = "shadowrun_char/character_equipment.html"

    def get_success_url(self):
        return reverse_lazy(
            "shadowrun_char:character_details", kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gear_list"] = Gear.objects.all()
        context["weapon_list"] = Weapon.objects.all()
        context["armor_list"] = Armor.objects.all()
        return context


class AddGearView(View):
    """HTMX endpoint to add gear"""

    def post(self, request, pk):
        character = get_object_or_404(ShadowrunCharacter, pk=pk)
        item_type = request.POST.get("item_type")
        item_id = request.POST.get("item_id")

        if item_type == "gear":
            item = get_object_or_404(Gear, pk=item_id)
            character.gear.add(item)
        elif item_type == "weapon":
            item = get_object_or_404(Weapon, pk=item_id)
            character.weapons.add(item)
        elif item_type == "armor":
            item = get_object_or_404(Armor, pk=item_id)
            character.armor.add(item)

        return render_to_string(
            "shadowrun_char/partials/equipment_list.html",
            {
                "character": character,
                "gear_list": character.gear.all(),
                "weapon_list": character.weapons.all(),
                "armor_list": character.armor.all(),
            },
            request=request,
        )


class RemoveGearView(View):
    """HTMX endpoint to remove gear"""

    def delete(self, request, pk, item_type, item_id):
        character = get_object_or_404(ShadowrunCharacter, pk=pk)

        if item_type == "gear":
            item = get_object_or_404(Gear, pk=item_id)
            character.gear.remove(item)
        elif item_type == "weapon":
            item = get_object_or_404(Weapon, pk=item_id)
            character.weapons.remove(item)
        elif item_type == "armor":
            item = get_object_or_404(Armor, pk=item_id)
            character.armor.remove(item)

        return render_to_string(
            "shadowrun_char/partials/equipment_list.html",
            {
                "character": character,
                "gear_list": character.gear.all(),
                "weapon_list": character.weapons.all(),
                "armor_list": character.armor.all(),
            },
            request=request,
        )


class CharacterDetailsView(UpdateView):
    """Step 6: Final details"""

    model = ShadowrunCharacter
    form_class = CharacterDetailsForm
    template_name = "shadowrun_char/character_details.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_created = True
        self.object.save()

        return redirect("shadowrun_char:character_sheet", pk=self.object.pk)


class CharacterSheetView(DetailView):
    """View completed character sheet"""

    model = ShadowrunCharacter
    template_name = "shadowrun_char/character_sheet.html"
    context_object_name = "character"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character_skills"] = CharacterSkill.objects.filter(
            character=self.object
        ).select_related("skill")
        context["character_qualities"] = CharacterQuality.objects.filter(
            character=self.object
        ).select_related("quality")
        context["contacts"] = Contact.objects.filter(character=self.object)
        context["lifestyles"] = Lifestyle.objects.filter(character=self.object)
        context["gear_list"] = self.object.gear.all()
        context["weapon_list"] = self.object.weapons.all()
        context["armor_list"] = self.object.armor.all()

        # Calculate totals
        total_karma = 25
        for cq in context["character_qualities"]:
            total_karma += (
                -cq.quality.karmic_cost
                if cq.quality.type == "positive"
                else cq.quality.karmic_cost
            )
        context["total_karma"] = total_karma

        return context


class GeneratePDFView(View):
    """Generate PDF of character sheet"""

    def get(self, request, pk):
        character = get_object_or_404(ShadowrunCharacter, pk=pk)

        # Get all related data
        character_skills = CharacterSkill.objects.filter(
            character=character
        ).select_related("skill")
        character_qualities = CharacterQuality.objects.filter(
            character=character
        ).select_related("quality")
        contacts = Contact.objects.filter(character=character)
        lifestyles = Lifestyle.objects.filter(character=character)
        gear_list = character.gear.all()
        weapon_list = character.weapons.all()
        armor_list = character.armor.all()

        # Calculate karma
        total_karma = 25
        for cq in character_qualities:
            total_karma += (
                -cq.quality.karmic_cost
                if cq.quality.type == "positive"
                else cq.quality.karmic_cost
            )

        context = {
            "character": character,
            "character_skills": character_skills,
            "character_qualities": character_qualities,
            "contacts": contacts,
            "lifestyles": lifestyles,
            "gear_list": gear_list,
            "weapon_list": weapon_list,
            "armor_list": armor_list,
            "total_karma": total_karma,
        }

        # Render HTML
        html_string = render_to_string(
            "shadowrun_char/character_sheet_pdf.html", context, request=request
        )

        # Generate PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{character.name}_character_sheet.pdf"'
        )

        HTML(string=html_string).write_pdf(response)

        return response


class RandomCharacterGenerator(View):
    """Generate a completely random character"""

    def post(self, request):
        # Random metatype
        metatype = random.choice(Metatype.objects.all())
        magic_type = random.choice(MagicType.objects.all())

        # Create character
        character = ShadowrunCharacter.objects.create(
            name=f"Runner-{random.randint(1000, 9999)}",
            metatype=metatype,
            magic_type=magic_type,
            body=random.randint(metatype.body_min, metatype.body_max),
            agility=random.randint(metatype.agility_min, metatype.agility_max),
            reaction=random.randint(metatype.reaction_min, metatype.reaction_max),
            strength=random.randint(metatype.strength_min, metatype.strength_max),
            willpower=random.randint(metatype.willpower_min, metatype.willpower_max),
            logic=random.randint(metatype.logic_min, metatype.logic_max),
            intuition=random.randint(metatype.intuition_min, metatype.intuition_max),
            charisma=random.randint(metatype.charisma_min, metatype.charisma_max),
            edge=random.randint(metatype.edge_min, metatype.edge_max),
            essence=6.0,
            is_created=True,
        )

        # Add random skills
        skills = list(Skill.objects.filter(is_knowledge_skill=False))
        random_skills = random.sample(skills, min(len(skills), random.randint(5, 10)))
        for skill in random_skills:
            CharacterSkill.objects.create(
                character=character, skill=skill, rating=random.randint(1, 6)
            )

        # Add random qualities
        qualities = list(Quality.objects.all())
        random_qualities = random.sample(
            qualities, min(len(qualities), random.randint(2, 4))
        )
        for quality in random_qualities:
            CharacterQuality.objects.create(character=character, quality=quality)

        # Store in session
        if "character_ids" not in request.session:
            request.session["character_ids"] = []
        request.session["character_ids"].append(character.pk)
        request.session.modified = True

        return redirect("shadowrun_char:character_sheet", pk=character.pk)


class CharacterListView(ListView):
    """List all characters created in this session"""

    model = ShadowrunCharacter
    template_name = "shadowrun_char/character_list.html"
    context_object_name = "characters"

    def get_queryset(self):
        character_ids = self.request.session.get("character_ids", [])
        return ShadowrunCharacter.objects.filter(pk__in=character_ids).order_by(
            "-created_at"
        )


class DeleteCharacterView(View):
    """Delete a character from session"""

    def post(self, request, pk):
        character = get_object_or_404(ShadowrunCharacter, pk=pk)

        # Remove from session
        character_ids = request.session.get("character_ids", [])
        if pk in character_ids:
            character_ids.remove(pk)
            request.session["character_ids"] = character_ids
            request.session.modified = True

        # Delete the character
        character.delete()

        return redirect("shadowrun_char:character_list")
