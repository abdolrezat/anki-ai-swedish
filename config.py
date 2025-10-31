"""
Configuration file for Anki card generation.

Edit these values to customize your setup:
- DECK_NAME_MODE_1_2: Deck for cards created from Lexin dictionary lookups
- DECK_NAME_MODE_3: Deck for cards created from custom sentences only
- CARD_MODEL: The Anki card type to use (must exist in Anki)
- TAGS: Default tags to add to all generated cards
"""

# Deck names (see Usage section in readme)
DECK_NAME_MODE_1_2 = "Swedish +"      # Deck for dictionary-based cards (with word lookup)
DECK_NAME_MODE_3 = "Swedish Adv."  # Deck for custom sentence cards (no lookup)

# Card model/type name (must match exactly with Anki)
CARD_MODEL = "Basic (and reversed card with media)"

# Default tags for all cards
TAGS = ["swedish", "auto-generated"]
