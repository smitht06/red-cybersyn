# shadowrun_char/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Metatype(models.Model):
    """Different metatypes available in Shadowrun"""

    METATYPE_CHOICES = [
        ("human", "Human"),
        ("elf", "Elf"),
        ("dwarf", "Dwarf"),
        ("ork", "Ork"),
        ("troll", "Troll"),
    ]

    name = models.CharField(max_length=20, choices=METATYPE_CHOICES, unique=True)
    body_min = models.IntegerField(default=1)
    body_max = models.IntegerField(default=6)
    agility_min = models.IntegerField(default=1)
    agility_max = models.IntegerField(default=6)
    reaction_min = models.IntegerField(default=1)
    reaction_max = models.IntegerField(default=6)
    strength_min = models.IntegerField(default=1)
    strength_max = models.IntegerField(default=6)
    willpower_min = models.IntegerField(default=1)
    willpower_max = models.IntegerField(default=6)
    logic_min = models.IntegerField(default=1)
    logic_max = models.IntegerField(default=6)
    intuition_min = models.IntegerField(default=1)
    intuition_max = models.IntegerField(default=6)
    charisma_min = models.IntegerField(default=1)
    charisma_max = models.IntegerField(default=6)
    edge_min = models.IntegerField(default=1)
    edge_max = models.IntegerField(default=6)
    essence_max = models.DecimalField(max_digits=3, decimal_places=1, default=6.0)
    special_attributes = models.TextField(
        blank=True, help_text="Special metatype attributes like Thermographic Vision"
    )

    class Meta:
        verbose_name = "Metatype"
        verbose_name_plural = "Metatypes"

    def __str__(self):
        return self.get_name_display()


class MagicType(models.Model):
    """Magic types available"""

    MAGIC_CHOICES = [
        ("mundane", "Mundane"),
        ("adept", "Adept"),
        ("magician", "Magician"),
        ("aspected", "Aspected Magician"),
        ("mystic_adept", "Mystic Adept"),
    ]

    name = models.CharField(max_length=30, choices=MAGIC_CHOICES, unique=True)
    magic_max = models.IntegerField(default=6)
    resonance_available = models.BooleanField(default=False)

    def __str__(self):
        return self.get_name_display()


class Skill(models.Model):
    """Skills that characters can have"""

    SKILL_CATEGORIES = [
        ("combat", "Combat"),
        ("physical", "Physical"),
        ("social", "Social"),
        ("technical", "Technical"),
        ("vehicle", "Vehicle"),
        ("magic", "Magic"),
        ("resonance", "Resonance"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    is_knowledge_skill = models.BooleanField(default=False)
    is_language = models.BooleanField(default=False)
    linked_attribute = models.CharField(
        max_length=20, help_text="Primary attribute linked to this skill"
    )
    default_attribute = models.CharField(
        max_length=20, blank=True, help_text="Default attribute if not trained"
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Quality(models.Model):
    """Positive and negative qualities"""

    QUALITY_TYPES = [
        ("positive", "Positive"),
        ("negative", "Negative"),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=QUALITY_TYPES)
    karmic_cost = models.IntegerField(
        help_text="Karma cost (positive) or bonus (negative)"
    )
    max_rank = models.IntegerField(default=1)
    description = models.TextField()
    prerequisites = models.TextField(
        blank=True, help_text="Any prerequisites for this quality"
    )
    effects = models.JSONField(
        default=dict, blank=True, help_text="Game mechanics effects in JSON format"
    )

    class Meta:
        ordering = ["type", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Spell(models.Model):
    """Spells for magical characters"""

    SPELL_CATEGORIES = [
        ("combat", "Combat"),
        ("detection", "Detection"),
        ("health", "Health"),
        ("illusion", "Illusion"),
        ("manipulation", "Manipulation"),
    ]

    SPELL_TYPES = [
        ("physical", "Physical"),
        ("mana", "Mana"),
    ]

    SPELL_RANGES = [
        ("touch", "Touch"),
        ("los", "Line of Sight"),
        ("los_a", "Line of Sight (Area)"),
        ("personal", "Personal"),
    ]

    SPELL_DURATIONS = [
        ("instant", "Instant"),
        ("sustained", "Sustained"),
        ("permanent", "Permanent"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SPELL_CATEGORIES)
    spell_type = models.CharField(max_length=10, choices=SPELL_TYPES)
    range = models.CharField(max_length=10, choices=SPELL_RANGES)
    duration = models.CharField(max_length=10, choices=SPELL_DURATIONS)
    drain_code = models.CharField(max_length=10, help_text="Drain value like F-2")
    description = models.TextField()

    def __str__(self):
        return self.name


class AdeptPower(models.Model):
    """Adept powers"""

    name = models.CharField(max_length=100)
    activation_type = models.CharField(
        max_length=20,
        choices=[
            ("always", "Always On"),
            ("simple", "Simple Action"),
            ("free", "Free Action"),
        ],
    )
    cost_per_rank = models.DecimalField(
        max_digits=4, decimal_places=1, help_text="Power points per rank"
    )
    max_rank = models.IntegerField(default=6)
    description = models.TextField()
    prerequisites = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Gear(models.Model):
    """Equipment and gear"""

    GEAR_CATEGORIES = [
        ("weapon", "Weapon"),
        ("armor", "Armor"),
        ("electronics", "Electronics"),
        ("survival", "Survival Gear"),
        ("tools", "Tools"),
        ("drugs", "Drugs"),
        ("vehicles", "Vehicles"),
        ("drones", "Drones"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=GEAR_CATEGORIES)
    availability = models.CharField(
        max_length=50, blank=True, help_text="Availability rating"
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    legality = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    stats = models.JSONField(
        default=dict, blank=True, help_text="Game statistics in JSON format"
    )

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Weapon(models.Model):
    """Detailed weapon stats"""

    WEAPON_CATEGORIES = [
        ("blade", "Blade"),
        ("club", "Club"),
        ("exotic_melee", "Exotic Melee"),
        ("pistol", "Pistol"),
        ("smg", "Submachine Gun"),
        ("assault_rifle", "Assault Rifle"),
        ("shotgun", "Shotgun"),
        ("sniper_rifle", "Sniper Rifle"),
        ("heavy_weapon", "Heavy Weapon"),
        ("bow", "Bow/Crossbow"),
        ("thrown", "Thrown Weapon"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=WEAPON_CATEGORIES)
    accuracy = models.IntegerField()
    damage = models.CharField(max_length=20, help_text="Damage value like 6P or 8S")
    armor_penetration = models.IntegerField(default=0)
    attack_rating = models.IntegerField(
        blank=True, null=True, help_text="For melee attacks"
    )
    defense_rating = models.IntegerField(
        blank=True, null=True, help_text="For melee attacks"
    )
    reach = models.IntegerField(default=0, help_text="For melee weapons")
    concealability = models.IntegerField(default=0)
    availability = models.CharField(max_length=50, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Armor(models.Model):
    """Armor stats"""

    name = models.CharField(max_length=100)
    armor_rating = models.IntegerField()
    social_penalty = models.IntegerField(default=0)
    availability = models.CharField(max_length=50, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=0, help_text="Modification capacity")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ShadowrunCharacter(models.Model):
    """Main character model"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shadowrun_characters"
    )
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, blank=True)

    # Core attributes
    metatype = models.ForeignKey(Metatype, on_delete=models.PROTECT)
    magic_type = models.ForeignKey(MagicType, on_delete=models.PROTECT)

    # Attributes (1-6 for humans, higher for some metatypes)
    body = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    agility = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    reaction = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    strength = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    willpower = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    logic = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    intuition = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    charisma = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    edge = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])

    # Derived attributes
    magic = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(12)]
    )
    resonance = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(12)]
    )
    essence = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=6.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(6.0)],
    )

    # Combat stats
    initiative_physical = models.IntegerField(
        default=0, help_text="Physical initiative dice"
    )
    initiative_matrix = models.IntegerField(
        default=0, help_text="Matrix initiative dice"
    )
    initiative_astral = models.IntegerField(
        default=0, help_text="Astral initiative dice"
    )

    # Health
    physical_track = models.IntegerField(help_text="Physical damage track boxes")
    stun_track = models.IntegerField(help_text="Stun damage track boxes")

    # Resources
    total_karma = models.IntegerField(default=0)
    current_karma = models.IntegerField(default=0)
    nuyen = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Character details
    age = models.IntegerField(default=25)
    height = models.CharField(max_length=20, blank=True)
    weight = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    background = models.TextField(blank=True)
    character_concept = models.CharField(max_length=200, blank=True)

    # Creation tracking
    is_created = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many-to-many relationships
    skills = models.ManyToManyField(Skill, through="CharacterSkill")
    qualities = models.ManyToManyField(Quality, through="CharacterQuality")
    spells = models.ManyToManyField(Spell, blank=True)
    adept_powers = models.ManyToManyField(AdeptPower, through="CharacterAdeptPower")
    gear = models.ManyToManyField(Gear, blank=True)
    weapons = models.ManyToManyField(Weapon, blank=True)
    armor = models.ManyToManyField(Armor, blank=True)

    class Meta:
        verbose_name = "Shadowrun Character"
        verbose_name_plural = "Shadowrun Characters"

    def __str__(self):
        return f"{self.alias or self.name} ({self.metatype})"

    def calculate_physical_track(self):
        """Calculate physical damage track based on Body attribute"""
        if self.body >= 1 and self.body <= 3:
            base = 8
        elif self.body >= 4 and self.body <= 6:
            base = 10
        elif self.body >= 7 and self.body <= 9:
            base = 11
        elif self.body >= 10 and self.body <= 12:
            base = 12
        else:
            base = 10
        return base + self.body // 2

    def calculate_stun_track(self):
        """Calculate stun damage track based on Willpower attribute"""
        if self.willpower >= 1 and self.willpower <= 3:
            base = 8
        elif self.willpower >= 4 and self.willpower <= 6:
            base = 10
        elif self.willpower >= 7 and self.willpower <= 9:
            base = 11
        else:
            base = 12
        return base + self.willpower // 2

    def save(self, *args, **kwargs):
        """Auto-calculate derived stats on save"""
        self.physical_track = self.calculate_physical_track()
        self.stun_track = self.calculate_stun_track()
        super().save(*args, **kwargs)


class CharacterSkill(models.Model):
    """Through model for character skills with ratings"""

    SKILL_RATINGS = [(i, str(i)) for i in range(1, 13)]
    SPECIALIZATION_CHOICES = [
        ("none", "None"),
        ("specialization", "Specialization"),
        ("expertise", "Expertise"),
    ]

    character = models.ForeignKey(ShadowrunCharacter, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=SKILL_RATINGS)
    specialization = models.CharField(max_length=100, blank=True)
    specialization_type = models.CharField(
        max_length=20, choices=SPECIALIZATION_CHOICES, default="none"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["character", "skill", "specialization"]

    def __str__(self):
        return f"{self.character.name} - {self.skill.name}: {self.rating}"


class CharacterQuality(models.Model):
    """Through model for character qualities"""

    character = models.ForeignKey(ShadowrunCharacter, on_delete=models.CASCADE)
    quality = models.ForeignKey(Quality, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ["character", "quality"]

    def __str__(self):
        return f"{self.character.name} - {self.quality.name}"


class CharacterAdeptPower(models.Model):
    """Through model for character adept powers"""

    character = models.ForeignKey(ShadowrunCharacter, on_delete=models.CASCADE)
    adept_power = models.ForeignKey(AdeptPower, on_delete=models.CASCADE)
    rank = models.IntegerField(default=1)
    power_points_spent = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ["character", "adept_power"]

    def __str__(self):
        return f"{self.character.name} - {self.adept_power.name} (Rank {self.rank})"


class Cyberware(models.Model):
    """Cyberware implants"""

    name = models.CharField(max_length=100)
    essence_cost = models.DecimalField(max_digits=4, decimal_places=2)
    availability = models.CharField(max_length=50, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    grade = models.CharField(
        max_length=20,
        choices=[
            ("standard", "Standard"),
            ("alpha", "Alpha"),
            ("beta", "Beta"),
            ("delta", "Delta"),
            ("used", "Used"),
        ],
        default="standard",
    )
    description = models.TextField()
    stats = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class Bioware(models.Model):
    """Bioware enhancements"""

    name = models.CharField(max_length=100)
    essence_cost = models.DecimalField(max_digits=4, decimal_places=2)
    availability = models.CharField(max_length=50, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    grade = models.CharField(
        max_length=20,
        choices=[
            ("standard", "Standard"),
            ("alpha", "Alpha"),
            ("beta", "Beta"),
            ("delta", "Delta"),
            ("used", "Used"),
        ],
        default="standard",
    )
    description = models.TextField()
    stats = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class CharacterCyberware(models.Model):
    """Through model for character cyberware"""

    character = models.ForeignKey(ShadowrunCharacter, on_delete=models.CASCADE)
    cyberware = models.ForeignKey(Cyberware, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    essence_cost_total = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ["character", "cyberware"]

    def __str__(self):
        return f"{self.character.name} - {self.cyberware.name}"


class CharacterBioware(models.Model):
    """Through model for character bioware"""

    character = models.ForeignKey(ShadowrunCharacter, on_delete=models.CASCADE)
    bioware = models.ForeignKey(Bioware, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    essence_cost_total = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ["character", "bioware"]

    def __str__(self):
        return f"{self.character.name} - {self.bioware.name}"


class Contact(models.Model):
    """Character contacts"""

    character = models.ForeignKey(
        ShadowrunCharacter, on_delete=models.CASCADE, related_name="contacts"
    )
    name = models.CharField(max_length=100)
    archetype = models.CharField(max_length=100, blank=True)
    connection_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    loyalty_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    description = models.TextField(blank=True)
    is_fixer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (Connection: {self.connection_rating}, Loyalty: {self.loyalty_rating})"


class Lifestyle(models.Model):
    """Character lifestyle"""

    LIFESTYLE_CHOICES = [
        ("street", "Street"),
        ("squatter", "Squatter"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("luxury", "Luxury"),
    ]

    character = models.ForeignKey(
        ShadowrunCharacter, on_delete=models.CASCADE, related_name="lifestyles"
    )
    name = models.CharField(max_length=100)
    lifestyle_type = models.CharField(max_length=20, choices=LIFESTYLE_CHOICES)
    monthly_cost = models.DecimalField(max_digits=10, decimal_places=2)
    district = models.CharField(max_length=100, blank=True)
    security_rating = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_lifestyle_type_display()})"


class CharacterLog(models.Model):
    """Log of character changes and roleplay notes"""

    character = models.ForeignKey(
        ShadowrunCharacter, on_delete=models.CASCADE, related_name="logs"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    log_type = models.CharField(
        max_length=50,
        choices=[
            ("session", "Session Log"),
            ("character_development", "Character Development"),
            ("karma", "Karma Change"),
            ("nuyen", "Nuyen Change"),
            ("note", "General Note"),
        ],
        default="note",
    )
    karma_change = models.IntegerField(default=0)
    nuyen_change = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.character.name} - {self.title} ({self.timestamp.date()})"
