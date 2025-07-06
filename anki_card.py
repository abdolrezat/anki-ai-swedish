import requests
import json

def add_anki_card(deck_name: str, model_name: str, fields: dict, tags: list = [], audio = []):
    result = requests.post("http://localhost:8765", json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": model_name,
                "fields": fields,
                "tags": tags,
                "options": {
                    "allowDuplicate": False
                },
                "audio": audio,   # Add audio if needed
                "video": [],
                "picture": []
            }
        }
    }).json()
    return result


def get_sample():
    return {
        'Front': 'serious, solemn, sever', 
        'Back': 'allvarlig | högtidlig, sträng, allvarsa', 
        'Extra': '(allvarligt, allvarliga)\n<b>1.</b> solemn, stern, grave (högtidlig, sträng, allvarsam)\n<b>2.</b> worrying, dangerous (oroande, farlig)\n<b>3.</b> sincere, honest, serious (uppriktig, ärlig, seriös)\n\nThe principal looked seriously at the boys.\nrektorn såg allvarligt på pojkarna\n\nA serious accident.\nen allvarlig olycka\n\nA serious illness.\nen allvarlig sjukdom\n\nA serious buyer for the house.\nen allvarlig spekulant på huset\n\nThey made serious attempts to find the money.\nde gjorde allvarliga försök att hitta pengarn'
        }
# print(response)