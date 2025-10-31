"""
One-time setup script to create the custom Anki card type:
"Basic (and reversed card with media)"

This card type includes:
- Fields: Front, Back, Extra, Audio, Video
- Two card templates: Recognition (Front→Back) and Production (Back→Front)
- Custom styling with collapsible Extra information
"""

import requests
import json
from config import CARD_MODEL


def create_card_model():
    """Create the custom Anki card model via AnkiConnect API."""
    
    url = "http://localhost:8765"
    
    # First check if the model already exists
    check_payload = {
        "action": "modelNames",
        "version": 6
    }
    
    response = requests.post(url, json=check_payload)
    existing_models = response.json().get("result", [])
    
    model_name = CARD_MODEL
    
    if model_name in existing_models:
        print(f"✓ Card type '{model_name}' already exists!")
        return True
    
    # Create the new model
    payload = {
        "action": "createModel",
        "version": 6,
        "params": {
            "modelName": model_name,
            "inOrderFields": ["Front", "Back", "Extra", "Audio", "Video"],
            "css": """.card {
  font-family: arial;
  font-size: 20px;
  text-align: center;
  color: black;
  background-color: white;
}
.hidden-text {
  color: gray;
  font-style: italic;
  margin-top: 5px;
  text-align: center;
}


""",
            "isCloze": False,
            "cardTemplates": [
                {
                    "Name": "Recognition",
                    "Front": """{{Front}}
<br><br>
{{Audio}}""",
                    "Back": """{{FrontSide}}

<hr id=answer>

{{Back}}
<br>
{{Video}}
<br>

{{#Extra}}
  <button onclick="toggleAnswer(this)">
    👁️ Extra Information
  </button>
  <br>
  <div class="hidden-text" style="display: none;">
    {{Extra}}
  </div>
  <script>
  function toggleAnswer(button) {
    const hiddenText = button.nextElementSibling.nextElementSibling; // Target the div
    if (hiddenText.style.display === 'none') {
      hiddenText.style.display = 'block';
    } else {
      hiddenText.style.display = 'none';
    }
  }
  </script>
{{/Extra}}"""
                },
                {
                    "Name": "Production",
                    "Front": """{{Back}}
<br>
""",
                    "Back": """{{FrontSide}}

<hr id=answer>

{{Front}}
<br><br>
{{Audio}}
<br>
{{Video}}
<br>

{{#Extra}}
  <button onclick="toggleAnswer(this)">
    👁️ Extra Information
  </button>
  <br>
  <div class="hidden-text" style="display: none;">
    {{Extra}}
  </div>
  <script>
  function toggleAnswer(button) {
    const hiddenText = button.nextElementSibling.nextElementSibling; // Target the div
    if (hiddenText.style.display === 'none') {
      hiddenText.style.display = 'block';
    } else {
      hiddenText.style.display = 'none';
    }
  }
  </script>
{{/Extra}}"""
                }
            ]
        }
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result.get("error") is None:
        print(f"✓ Successfully created card type '{model_name}'!")
        print("\nThis card type includes:")
        print("  - Fields: Front, Back, Extra, Audio, Video")
        print("  - Recognition card: Front → Back (with audio)")
        print("  - Production card: Back → Front (reverse)")
        print("  - Collapsible 'Extra' information section")
        return True
    else:
        print(f"✗ Error creating card type: {result.get('error')}")
        return False


def main():
    print("Setting up Anki card type for Swedish flashcards...")
    print("=" * 60)
    
    # Check if Anki is running
    try:
        response = requests.get("http://localhost:8765", timeout=2)
        print("✓ Anki is running")
    except requests.exceptions.RequestException:
        print("✗ Error: Anki is not running or AnkiConnect is not installed.")
        print("\nPlease:")
        print("  1. Start Anki")
        print("  2. Ensure AnkiConnect plugin is installed")
        print("  3. Try again")
        return False
    
    print()
    success = create_card_model()
    
    if success:
        print("\n" + "=" * 60)
        print("Setup complete! You can now use the main script.")
    
    return success


if __name__ == "__main__":
    main()
