from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


class CharacterModelTests(TestCase):
    """Tests for the Character model."""

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.character = Character.objects.create(
            owner=self.user,
            name="Blade",
            metatype_name="elf",
            magic_type="adept",
            body=3,
            agility=5,
            reaction=4,
            strength=2,
            willpower=3,
            logic=3,
            intuition=4,
            charisma=3,
            edge=2,
            essence=6,
        )

    def test_character_str(self):
        """Test the string representation of a character."""
        self.assertEqual(str(self.character), "Blade")

    def test_character_owner(self):
        """Test that the character belongs to the correct owner."""
        self.assertEqual(self.character.owner, self.user)

    def test_character_get_absolute_url(self):
        """Test the absolute URL of a character."""
        self.assertEqual(
            self.character.get_absolute_url(),
            reverse("characters:detail", kwargs={"pk": self.character.pk}),
        )

    def test_final_attributes_without_metatype(self):
        """Test final attributes equal base when no metatype is set."""
        self.assertEqual(self.character.final_body, 3)
        self.assertEqual(self.character.final_agility, 5)
        self.assertEqual(self.character.final_essence, 6)

    def test_final_attributes_with_metatype(self):
        """Test final attributes include metatype modifiers."""
        metatype = Metatype.objects.create(
            name="Elf",
            agility_mod=2,
            charisma_mod=2,
            strength_mod=-1,
        )
        self.character.metatype = metatype
        self.character.save()
        self.assertEqual(self.character.final_agility, 7)
        self.assertEqual(self.character.final_charisma, 5)
        self.assertEqual(self.character.final_strength, 1)

    def test_final_attributes_with_quality(self):
        """Test final attributes include quality modifiers."""
        quality = Quality.objects.create(
            name="Toughness",
            quality_type="positive",
            body_mod=1,
        )
        CharacterQuality.objects.create(character=self.character, quality=quality)
        self.assertEqual(self.character.final_body, 4)

    def test_attribute_dict(self):
        """Test the attribute_dict property returns all attributes."""
        attrs = self.character.attribute_dict
        self.assertEqual(attrs["Body"], self.character.final_body)
        self.assertEqual(attrs["Agility"], self.character.final_agility)
        self.assertEqual(attrs["Essence"], self.character.final_essence)
        self.assertEqual(len(attrs), 10)

    def test_total_karma_spent(self):
        """Test the karma spent estimate."""
        # body=3, agility=5, reaction=4, strength=2, willpower=3,
        # logic=3, intuition=4, charisma=3, edge=2
        # (3-1)+(5-1)+(4-1)+(2-1)+(3-1)+(3-1)+(4-1)+(3-1)+(2-1)
        # = 2+4+3+1+2+2+3+2+1 = 20
        self.assertEqual(self.character.total_karma_spent, 20)


class CharacterSkillModelTests(TestCase):
    """Tests for the CharacterSkill through model."""

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.character = Character.objects.create(owner=self.user, name="Blade")
        self.skill = Skill.objects.create(name="Firearms", linked_attribute="agility")

    def test_character_skill_str(self):
        """Test the string representation."""
        cs = CharacterSkill.objects.create(
            character=self.character, skill=self.skill, rating=4
        )
        self.assertEqual(str(cs), "Blade - Firearms (4)")

    def test_character_skill_unique_together(self):
        """Test that a character cannot have the same skill twice."""
        CharacterSkill.objects.create(
            character=self.character, skill=self.skill, rating=3
        )
        with self.assertRaises(Exception):
            CharacterSkill.objects.create(
                character=self.character, skill=self.skill, rating=5
            )


class CharacterViewTests(TestCase):
    """Tests for the character views."""

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.other_user = self.User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        self.character = Character.objects.create(
            owner=self.user, name="Blade", metatype_name="human"
        )
        self.other_character = Character.objects.create(
            owner=self.other_user, name="Other", metatype_name="ork"
        )

    def test_list_requires_login(self):
        """Test that the list view requires authentication."""
        response = self.client.get(reverse("characters:list"))
        self.assertEqual(response.status_code, 302)

    def test_list_shows_only_own_characters(self):
        """Test that the list only shows the current user's characters."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("characters:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blade")
        self.assertNotContains(response, "Other")

    def test_detail_requires_login(self):
        """Test that the detail view requires authentication."""
        response = self.client.get(
            reverse("characters:detail", kwargs={"pk": self.character.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_detail_owner_only(self):
        """Test that a user cannot view another user's character."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("characters:detail", kwargs={"pk": self.other_character.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_detail_owner_can_view(self):
        """Test that the owner can view their character."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("characters:detail", kwargs={"pk": self.character.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blade")

    def test_create_requires_login(self):
        """Test that creating a character requires authentication."""
        response = self.client.get(reverse("characters:create"))
        self.assertEqual(response.status_code, 302)

    def test_create_character(self):
        """Test creating a new character."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("characters:create"),
            {
                "name": "New Runner",
                "metatype_name": "elf",
                "magic_type": "magician",
                "body": 2,
                "agility": 4,
                "reaction": 3,
                "strength": 2,
                "willpower": 3,
                "logic": 4,
                "intuition": 3,
                "charisma": 3,
                "edge": 2,
                "essence": 6,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Character.objects.filter(name="New Runner", owner=self.user).exists()
        )

    def test_update_owner_only(self):
        """Test that a user cannot edit another user's character."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("characters:update", kwargs={"pk": self.other_character.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_character(self):
        """Test editing a character."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("characters:update", kwargs={"pk": self.character.pk}),
            {
                "name": "Blade Updated",
                "metatype_name": "human",
                "magic_type": "mundane",
                "body": 3,
                "agility": 3,
                "reaction": 3,
                "strength": 3,
                "willpower": 3,
                "logic": 3,
                "intuition": 3,
                "charisma": 3,
                "edge": 1,
                "essence": 6,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.character.refresh_from_db()
        self.assertEqual(self.character.name, "Blade Updated")

    def test_delete_owner_only(self):
        """Test that a user cannot delete another user's character."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("characters:delete", kwargs={"pk": self.other_character.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_character(self):
        """Test deleting a character."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("characters:delete", kwargs={"pk": self.character.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Character.objects.filter(pk=self.character.pk).exists())


class CharacterRelatedViewTests(TestCase):
    """Tests for the skill/quality/gear management views."""

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.character = Character.objects.create(
            owner=self.user, name="Blade", metatype_name="human"
        )
        self.skill = Skill.objects.create(name="Firearms", linked_attribute="agility")
        self.quality = Quality.objects.create(
            name="Toughness", quality_type="positive", karma_cost=10
        )
        self.gear = Gear.objects.create(name="Ares Predator", category="Weapon")
        self.client.force_login(self.user)

    def test_add_skill(self):
        """Test adding a skill to a character."""
        response = self.client.post(
            reverse("characters:skill_add", kwargs={"pk": self.character.pk}),
            {"skill": self.skill.pk, "rating": 4},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CharacterSkill.objects.filter(
                character=self.character, skill=self.skill
            ).exists()
        )

    def test_remove_skill(self):
        """Test removing a skill from a character."""
        cs = CharacterSkill.objects.create(
            character=self.character, skill=self.skill, rating=4
        )
        response = self.client.post(
            reverse("characters:skill_delete", kwargs={"pk": cs.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CharacterSkill.objects.filter(pk=cs.pk).exists())

    def test_add_quality(self):
        """Test adding a quality to a character."""
        response = self.client.post(
            reverse("characters:quality_add", kwargs={"pk": self.character.pk}),
            {"quality": self.quality.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CharacterQuality.objects.filter(
                character=self.character, quality=self.quality
            ).exists()
        )

    def test_remove_quality(self):
        """Test removing a quality from a character."""
        cq = CharacterQuality.objects.create(
            character=self.character, quality=self.quality
        )
        response = self.client.post(
            reverse("characters:quality_delete", kwargs={"pk": cq.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CharacterQuality.objects.filter(pk=cq.pk).exists())

    def test_add_gear(self):
        """Test adding gear to a character."""
        response = self.client.post(
            reverse("characters:gear_add", kwargs={"pk": self.character.pk}),
            {"gear": self.gear.pk, "quantity": 2},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CharacterGear.objects.filter(
                character=self.character, gear=self.gear
            ).exists()
        )

    def test_remove_gear(self):
        """Test removing gear from a character."""
        cg = CharacterGear.objects.create(
            character=self.character, gear=self.gear, quantity=1
        )
        response = self.client.post(
            reverse("characters:gear_delete", kwargs={"pk": cg.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CharacterGear.objects.filter(pk=cg.pk).exists())


class CharacterURLTests(TestCase):
    """Tests for URL resolution."""

    def test_list_url(self):
        """Test the list URL."""
        self.assertEqual(reverse("characters:list"), "/characters/")

    def test_create_url(self):
        """Test the create URL."""
        self.assertEqual(reverse("characters:create"), "/characters/new/")

    def test_detail_url(self):
        """Test the detail URL."""
        self.assertEqual(
            reverse("characters:detail", kwargs={"pk": 1}), "/characters/1/"
        )

    def test_update_url(self):
        """Test the update URL."""
        self.assertEqual(
            reverse("characters:update", kwargs={"pk": 1}), "/characters/1/edit/"
        )

    def test_delete_url(self):
        """Test the delete URL."""
        self.assertEqual(
            reverse("characters:delete", kwargs={"pk": 1}), "/characters/1/delete/"
        )
