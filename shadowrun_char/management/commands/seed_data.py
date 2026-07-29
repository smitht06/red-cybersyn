# shadowrun_char/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from shadowrun_char.models import Metatype, MagicType, Skill, Quality


class Command(BaseCommand):
    help = "Seeds initial Shadowrun data"

    def handle(self, *args, **kwargs):
        # Create metatypes
        metatypes_data = [
            {
                "name": "human",
                "body_max": 6,
                "agility_max": 6,
                "reaction_max": 6,
                "strength_max": 6,
                "willpower_max": 6,
                "logic_max": 6,
                "intuition_max": 6,
                "charisma_max": 6,
                "edge_max": 7,
                "essence_max": 6.0,
            },
            {
                "name": "elf",
                "body_max": 6,
                "agility_max": 7,
                "reaction_max": 6,
                "strength_max": 6,
                "willpower_max": 6,
                "logic_max": 6,
                "intuition_max": 6,
                "charisma_max": 8,
                "edge_max": 6,
                "essence_max": 6.0,
                "special_attributes": "Thermographic Vision",
            },
            {
                "name": "dwarf",
                "body_max": 8,
                "agility_max": 6,
                "reaction_max": 5,
                "strength_max": 8,
                "willpower_max": 7,
                "logic_max": 6,
                "intuition_max": 6,
                "charisma_max": 6,
                "edge_max": 6,
                "essence_max": 6.0,
                "special_attributes": "Thermographic Vision, +2 Body for toxin resistance",
            },
            {
                "name": "ork",
                "body_max": 9,
                "agility_max": 6,
                "reaction_max": 6,
                "strength_max": 8,
                "willpower_max": 6,
                "logic_max": 5,
                "intuition_max": 5,
                "charisma_max": 5,
                "edge_max": 5,
                "essence_max": 6.0,
                "special_attributes": "Low-Light Vision",
            },
            {
                "name": "troll",
                "body_max": 10,
                "agility_max": 5,
                "reaction_max": 5,
                "strength_max": 10,
                "willpower_max": 6,
                "logic_max": 5,
                "intuition_max": 5,
                "charisma_max": 4,
                "edge_max": 5,
                "essence_max": 6.0,
                "special_attributes": "Thermographic Vision, Dermal Armor +1, +1 Reach",
            },
        ]

        for meta_data in metatypes_data:
            Metatype.objects.update_or_create(
                name=meta_data["name"], defaults=meta_data
            )
            self.stdout.write(f"Created metatype: {meta_data['name']}")

        # Create magic types
        magic_types = ["mundane", "adept", "magician", "aspected", "mystic_adept"]
        for magic_type in magic_types:
            MagicType.objects.update_or_create(name=magic_type)
            self.stdout.write(f"Created magic type: {magic_type}")

            # Create sample skills
            skills_data = [
                {
                    "name": "Archery",
                    "category": "combat",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Automatics",
                    "category": "combat",
                    "linked_attribute": "agility",
                },
                {"name": "Blades", "category": "combat", "linked_attribute": "agility"},
                {"name": "Clubs", "category": "combat", "linked_attribute": "agility"},
                {
                    "name": "Exotic Melee Weapons",
                    "category": "combat",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Exotic Ranged Weapons",
                    "category": "combat",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Heavy Weapons",
                    "category": "combat",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Longarms",
                    "category": "combat",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Pistols",
                    "category": "combat",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Throwing Weapons",
                    "category": "combat",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Unarmed Combat",
                    "category": "combat",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Disguise",
                    "category": "physical",
                    "linked_attribute": "intuition",
                },
                {"name": "Diving", "category": "physical", "linked_attribute": "body"},
                {
                    "name": "Escape Artist",
                    "category": "physical",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Free-Fall",
                    "category": "physical",
                    "linked_attribute": "reaction",
                },
                {
                    "name": "Gymnastics",
                    "category": "physical",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Palming",
                    "category": "physical",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Perception",
                    "category": "physical",
                    "linked_attribute": "intuition",
                },
                {"name": "Running", "category": "physical", "linked_attribute": "body"},
                {
                    "name": "Sneaking",
                    "category": "physical",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Survival",
                    "category": "physical",
                    "linked_attribute": "willpower",
                },
                {
                    "name": "Swimming",
                    "category": "physical",
                    "linked_attribute": "body",
                },
                {
                    "name": "Tracking",
                    "category": "physical",
                    "linked_attribute": "intuition",
                },
                {"name": "Con", "category": "social", "linked_attribute": "charisma"},
                {
                    "name": "Etiquette",
                    "category": "social",
                    "linked_attribute": "charisma",
                },
                {
                    "name": "Impersonation",
                    "category": "social",
                    "linked_attribute": "charisma",
                },
                {
                    "name": "Instruction",
                    "category": "social",
                    "linked_attribute": "charisma",
                },
                {
                    "name": "Intimidation",
                    "category": "social",
                    "linked_attribute": "charisma",
                },
                {
                    "name": "Leadership",
                    "category": "social",
                    "linked_attribute": "charisma",
                },
                {
                    "name": "Negotiation",
                    "category": "social",
                    "linked_attribute": "charisma",
                },
                {
                    "name": "Performance",
                    "category": "social",
                    "linked_attribute": "charisma",
                },
                {
                    "name": "Aeronautics Mechanic",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Automotive Mechanic",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Biotechnology",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Brewing/Distilling",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Chemistry",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Computer",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Cybercombat",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Cybertechnology",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Demolitions",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Electronic Warfare",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "First Aid",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Forgery",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Hacking",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Hardware",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Industrial Mechanic",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Locksmith",
                    "category": "technical",
                    "linked_attribute": "agility",
                },
                {
                    "name": "Medicine",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Navigation",
                    "category": "technical",
                    "linked_attribute": "intuition",
                },
                {
                    "name": "Nautical Mechanic",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Software",
                    "category": "technical",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Artisan",
                    "category": "technical",
                    "linked_attribute": "intuition",
                },
                {
                    "name": "Ground Craft",
                    "category": "vehicle",
                    "linked_attribute": "reaction",
                },
                {
                    "name": "Pilot Aircraft",
                    "category": "vehicle",
                    "linked_attribute": "reaction",
                },
                {
                    "name": "Pilot Exotic Vehicle",
                    "category": "vehicle",
                    "linked_attribute": "reaction",
                },
                {
                    "name": "Pilot Watercraft",
                    "category": "vehicle",
                    "linked_attribute": "reaction",
                },
                {
                    "name": "Assensing",
                    "category": "magic",
                    "linked_attribute": "intuition",
                },
                {
                    "name": "Astral Combat",
                    "category": "magic",
                    "linked_attribute": "willpower",
                },
                {
                    "name": "Banishing",
                    "category": "magic",
                    "linked_attribute": "charisma",
                },
                {
                    "name": "Binding",
                    "category": "magic",
                    "linked_attribute": "charisma",
                },
                {
                    "name": "Counterspelling",
                    "category": "magic",
                    "linked_attribute": "willpower",
                },
                {
                    "name": "Disenchanting",
                    "category": "magic",
                    "linked_attribute": "logic",
                },
                {
                    "name": "Ritual Spellcasting",
                    "category": "magic",
                    "linked_attribute": "willpower",
                },
                {
                    "name": "Spellcasting",
                    "category": "magic",
                    "linked_attribute": "magic",
                },
                {
                    "name": "Summoning",
                    "category": "magic",
                    "linked_attribute": "charisma",
                },
            ]

        for skill_data in skills_data:
            Skill.objects.update_or_create(name=skill_data["name"], defaults=skill_data)
            self.stdout.write(f"Created skill: {skill_data['name']}")

        # Create sample qualities
        qualities_data = [
            # Positive qualities
            {
                "name": "Aptitude",
                "type": "positive",
                "karmic_cost": 10,
                "max_rank": 1,
                "description": "Character has a natural talent for a specific skill. Choose one skill; the character gains a +1 dice pool modifier to that skill.",
            },
            {
                "name": "Astral Chameleon",
                "type": "positive",
                "karmic_cost": 5,
                "max_rank": 1,
                "description": "Your astral signature is difficult to read. You receive a +2 dice pool modifier on tests to conceal your astral signature.",
            },
            {
                "name": "Catlike",
                "type": "positive",
                "karmic_cost": 7,
                "max_rank": 1,
                "description": "You are exceptionally graceful. You gain +1 full dodge pool and +2 to Gymnastics tests.",
            },
            {
                "name": "College Education",
                "type": "positive",
                "karmic_cost": 5,
                "max_rank": 1,
                "description": "You have a college education. Choose three Knowledge skills; you receive a rating of 3 in each for free.",
            },
            {
                "name": "Common Sense",
                "type": "positive",
                "karmic_cost": 8,
                "max_rank": 1,
                "description": "You have excellent common sense. Once per game session, the GM must give you a hint about a course of action.",
            },
            {
                "name": "Double Jointed",
                "type": "positive",
                "karmic_cost": 8,
                "max_rank": 1,
                "description": "Your joints are unusually flexible. You gain +2 dice on Escape Artist tests.",
            },
            {
                "name": "Exceptional Attribute",
                "type": "positive",
                "karmic_cost": 14,
                "max_rank": 1,
                "description": "Choose one attribute; its maximum rating is increased by 1.",
            },
            {
                "name": "First Impression",
                "type": "positive",
                "karmic_cost": 5,
                "max_rank": 1,
                "description": "You make an excellent first impression. On the first social test you make in any scene, you gain +2 dice.",
            },
            {
                "name": "Focused Concentration",
                "type": "positive",
                "karmic_cost": 4,
                "max_rank": 3,
                "description": "You can sustain multiple spells. Each rank reduces the penalty for sustaining spells by 1.",
            },
            {
                "name": "Guts",
                "type": "positive",
                "karmic_cost": 7,
                "max_rank": 1,
                "description": "You are brave and resolute. You gain +2 dice on tests to resist fear or intimidation.",
            },
            # Negative qualities
            {
                "name": "Addiction",
                "type": "negative",
                "karmic_cost": 5,
                "max_rank": 3,
                "description": "You are addicted to a substance or activity. The severity increases with rank.",
            },
            {
                "name": "Astral Beacon",
                "type": "negative",
                "karmic_cost": 6,
                "max_rank": 1,
                "description": "Your astral signature is bright and easy to spot. You suffer -2 dice on tests to conceal your astral signature.",
            },
            {
                "name": "Bad Luck",
                "type": "negative",
                "karmic_cost": 8,
                "max_rank": 1,
                "description": "You are extremely unlucky. Once per game session, the GM can force you to reroll a successful test.",
            },
            {
                "name": "Bad Rep",
                "type": "negative",
                "karmic_cost": 8,
                "max_rank": 1,
                "description": "You have a bad reputation in the shadows. You suffer -2 dice on social tests.",
            },
            {
                "name": "Combat Paralysis",
                "type": "negative",
                "karmic_cost": 6,
                "max_rank": 1,
                "description": "You freeze up in combat. During the first Combat Turn of combat, you cannot take any actions.",
            },
            {
                "name": "Dependent",
                "type": "negative",
                "karmic_cost": 4,
                "max_rank": 1,
                "description": "You have someone who depends on you for support. This can be used as leverage against you.",
            },
            {
                "name": "Distinctive Style",
                "type": "negative",
                "karmic_cost": 5,
                "max_rank": 1,
                "description": "You have a very distinctive appearance or style that makes you easy to identify.",
            },
            {
                "name": "Gremlins",
                "type": "negative",
                "karmic_cost": 5,
                "max_rank": 3,
                "description": "Technology seems to malfunction around you. Each rank gives -1 die on tests involving technology.",
            },
            {
                "name": "Insomnia",
                "type": "negative",
                "karmic_cost": 6,
                "max_rank": 1,
                "description": "You have difficulty sleeping. You start each session with 1 less point of Edge.",
            },
            {
                "name": "Prejudiced",
                "type": "negative",
                "karmic_cost": 4,
                "max_rank": 1,
                "description": "You hold strong prejudices against a particular group. This affects your interactions with them.",
            },
        ]

        for quality_data in qualities_data:
            Quality.objects.update_or_create(
                name=quality_data["name"], defaults=quality_data
            )
            self.stdout.write(f"Created quality: {quality_data['name']}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded all Shadowrun data!"))
