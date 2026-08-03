from django.conf import settings
from django.db import models
from django.urls import reverse


class Metatype(models.Model):
    """A Shadowrun 6th World metatype (e.g. Human, Elf, Ork, Dwarf, Troll)."""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    # Attribute modifiers applied to the base attribute of 1
    body_mod = models.IntegerField(default=0)
    agility_mod = models.IntegerField(default=0)
    reaction_mod = models.IntegerField(default=0)
    strength_mod = models.IntegerField(default=0)
    willpower_mod = models.IntegerField(default=0)
    logic_mod = models.IntegerField(default=0)
    intuition_mod = models.IntegerField(default=0)
    charisma_mod = models.IntegerField(default=0)
    edge_mod = models.IntegerField(default=0)
    essence_mod = models.IntegerField(default=0)
    # Maximum attribute values (before augmentation)
    body_max = models.IntegerField(default=6)
    agility_max = models.IntegerField(default=6)
    reaction_max = models.IntegerField(default=6)
    strength_max = models.IntegerField(default=6)
    willpower_max = models.IntegerField(default=6)
    logic_max = models.IntegerField(default=6)
    intuition_max = models.IntegerField(default=6)
    charisma_max = models.IntegerField(default=6)
    edge_max = models.IntegerField(default=6)
    essence_max = models.IntegerField(default=6)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Skill(models.Model):
    """A Shadowrun 6th World skill."""

    SKILL_TYPES = [
        ("active", "Active"),
        ("knowledge", "Knowledge"),
        ("language", "Language"),
    ]

    name = models.CharField(max_length=100, unique=True)
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPES, default="active")
    # Linked attribute (e.g. "agility", "logic", etc.)
    linked_attribute = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    is_specialization = models.BooleanField(default=False)
    parent_skill = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="specializations",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Quality(models.Model):
    """A Shadowrun 6th World quality (positive or negative)."""

    QUALITY_TYPES = [
        ("positive", "Positive"),
        ("negative", "Negative"),
    ]

    name = models.CharField(max_length=100, unique=True)
    quality_type = models.CharField(max_length=20, choices=QUALITY_TYPES)
    karma_cost = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    # Optional attribute/stat modifiers granted by the quality
    body_mod = models.IntegerField(default=0)
    agility_mod = models.IntegerField(default=0)
    reaction_mod = models.IntegerField(default=0)
    strength_mod = models.IntegerField(default=0)
    willpower_mod = models.IntegerField(default=0)
    logic_mod = models.IntegerField(default=0)
    intuition_mod = models.IntegerField(default=0)
    charisma_mod = models.IntegerField(default=0)
    edge_mod = models.IntegerField(default=0)
    essence_mod = models.IntegerField(default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Gear(models.Model):
    """A piece of equipment a character can own."""

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    availability = models.CharField(max_length=50, blank=True)
    cost = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Spell(models.Model):
    """A spell a magic-using character can know."""

    SPELL_TYPES = [
        ("combat", "Combat"),
        ("detection", "Detection"),
        ("health", "Health"),
        ("illusion", "Illusion"),
        ("manipulation", "Manipulation"),
    ]

    name = models.CharField(max_length=100, unique=True)
    spell_type = models.CharField(max_length=20, choices=SPELL_TYPES)
    description = models.TextField(blank=True)
    drain = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Character(models.Model):
    """A Shadowrun 6th World character."""

    # Metatype choices (fallback if no Metatype records exist)
    METATYPE_CHOICES = [
        ("human", "Human"),
        ("elf", "Elf"),
        ("ork", "Ork"),
        ("dwarf", "Dwarf"),
        ("troll", "Troll"),
    ]

    # Magic/Resonance types
    MAGIC_TYPES = [
        ("mundane", "Mundane"),
        ("adept", "Adept"),
        ("magician", "Magician"),
        ("mystic_adept", "Mystic Adept"),
        ("technomancer", "Technomancer"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="characters",
    )
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, blank=True)
    metatype = models.ForeignKey(
        Metatype,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="characters",
    )
    metatype_name = models.CharField(
        max_length=20, choices=METATYPE_CHOICES, default="human"
    )
    magic_type = models.CharField(max_length=20, choices=MAGIC_TYPES, default="mundane")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Attributes (base values before metatype modifiers)
    body = models.IntegerField(default=1)
    agility = models.IntegerField(default=1)
    reaction = models.IntegerField(default=1)
    strength = models.IntegerField(default=1)
    willpower = models.IntegerField(default=1)
    logic = models.IntegerField(default=1)
    intuition = models.IntegerField(default=1)
    charisma = models.IntegerField(default=1)
    edge = models.IntegerField(default=1)
    essence = models.IntegerField(default=6)

    # Derived / resource values
    karma = models.IntegerField(default=0)
    nuyen = models.IntegerField(default=0)
    magic = models.IntegerField(default=0)
    resonance = models.IntegerField(default=0)

    # Background / flavor
    background = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    # Many-to-many relationships
    skills = models.ManyToManyField(
        Skill, through="CharacterSkill", related_name="characters"
    )
    qualities = models.ManyToManyField(
        Quality, through="CharacterQuality", related_name="characters"
    )
    gear = models.ManyToManyField(
        Gear, through="CharacterGear", related_name="characters"
    )
    spells = models.ManyToManyField(Spell, related_name="characters", blank=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characters:detail", kwargs={"pk": self.pk})

    # ---- Attribute helpers ----

    def _metatype_mod(self, attr):
        """Return the metatype modifier for a given attribute."""
        if self.metatype:
            return getattr(self.metatype, f"{attr}_mod", 0)
        return 0

    def _metatype_max(self, attr):
        """Return the metatype maximum for a given attribute."""
        if self.metatype:
            return getattr(self.metatype, f"{attr}_max", 6)
        return 6

    def _quality_mod(self, attr):
        """Return the total quality modifier for a given attribute."""
        total = 0
        for cq in self.character_qualities.all():
            total += getattr(cq.quality, f"{attr}_mod", 0)
        return total

    def _final_attribute(self, attr):
        """Compute the final attribute value including metatype and quality modifiers."""
        base = getattr(self, attr)
        return base + self._metatype_mod(attr) + self._quality_mod(attr)

    @property
    def final_body(self):
        return self._final_attribute("body")

    @property
    def final_agility(self):
        return self._final_attribute("agility")

    @property
    def final_reaction(self):
        return self._final_attribute("reaction")

    @property
    def final_strength(self):
        return self._final_attribute("strength")

    @property
    def final_willpower(self):
        return self._final_attribute("willpower")

    @property
    def final_logic(self):
        return self._final_attribute("logic")

    @property
    def final_intuition(self):
        return self._final_attribute("intuition")

    @property
    def final_charisma(self):
        return self._final_attribute("charisma")

    @property
    def final_edge(self):
        return self._final_attribute("edge")

    @property
    def final_essence(self):
        return self._final_attribute("essence")

    @property
    def attribute_dict(self):
        """Return a dict of all final attributes for template display."""
        return {
            "Body": self.final_body,
            "Agility": self.final_agility,
            "Reaction": self.final_reaction,
            "Strength": self.final_strength,
            "Willpower": self.final_willpower,
            "Logic": self.final_logic,
            "Intuition": self.final_intuition,
            "Charisma": self.final_charisma,
            "Edge": self.final_edge,
            "Essence": self.final_essence,
        }

    @property
    def total_karma_spent(self):
        """Estimate karma spent on attributes (base value above 1)."""
        attrs = [
            self.body,
            self.agility,
            self.reaction,
            self.strength,
            self.willpower,
            self.logic,
            self.intuition,
            self.charisma,
            self.edge,
        ]
        return sum(max(0, a - 1) for a in attrs)


class CharacterSkill(models.Model):
    """Through model linking a Character to a Skill with a rating."""

    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="character_skills"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    is_specialization = models.BooleanField(default=False)

    class Meta:
        unique_together = ("character", "skill")

    def __str__(self):
        return f"{self.character.name} - {self.skill.name} ({self.rating})"


class CharacterQuality(models.Model):
    """Through model linking a Character to a Quality."""

    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="character_qualities"
    )
    quality = models.ForeignKey(Quality, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("character", "quality")

    def __str__(self):
        return f"{self.character.name} - {self.quality.name}"


class CharacterGear(models.Model):
    """Through model linking a Character to a piece of Gear with quantity."""

    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="character_gear"
    )
    gear = models.ForeignKey(Gear, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ("character", "gear")

    def __str__(self):
        return f"{self.character.name} - {self.gear.name} x{self.quantity}"
