#!/home/rt/miniconda3/envs/py310/bin/python

from lexin_fetch import extract_data_from_json, fetch_word_data
from LLM_inference import hf_chat
import json
from anki_card import add_anki_card
import wget
import argparse
class AnkiError(Exception):
    pass

def extract_text_between_tag(text: str, tag_start, tag_end):
    if tag_start in text and tag_end in text:
        start_index = text.index(tag_start) + len(tag_start)
        end_index = text.index(tag_end)
        extracted_text = text[start_index:end_index]
        # if extracted_text.startswith('\n'):
        #     extracted_text = extracted_text[1:]
        # if extracted_text.endswith('\n'):
        #     extracted_text = extracted_text[:-1]
        return extracted_text
    else:
        raise ValueError(f'could not get values for tag: {tag_start}')

def download_files_to_tmp(url_list, output_paths):
    for url, out in zip(url_list, output_paths):
        wget.download(url, out=out)
        print()  # newline after each download progress bar

def get_audio_link(web_result):
    try:
        phonetics = web_result['Result'][0]['Phonetic']
        audio_links = [x.get('File') for x in phonetics if x.get('File')]
        return audio_links
    except Exception as e:
        print(f'Could not get audio files due to error: {e}')
        return []

def main(word, extra_user_input = None):
    if word != "":
        web_result = extract_data_from_json(fetch_word_data(word))
        print('=============== web result ===================')
        print(json.dumps(web_result, indent=4, ensure_ascii=False))
        print('=============== end / web result ===================')
        audio_links = get_audio_link(web_result)
        deck_name = "Swedish +"
    else:
        web_result, audio_links = None, None
        deck_name = "Swedish Adv."
        
    chat_response = hf_chat(web_result, extra_user_input)
    audio = []
    if audio_links:
        file_names = [x.split('/')[-1] for x in audio_links]
        output_paths = [f"/tmp/{x}" for x in file_names]
        download_files_to_tmp(audio_links, output_paths)
        audio = [{
                    "path": op,
                    "filename": fn,  # Or give your own name
                    "fields": ["Audio"]  # Must match one of your field names!
                        } for op, fn in zip(output_paths, file_names)]
    extracted_card_fields = {
        "Front": extract_text_between_tag(chat_response, "<Front>","</Front>"),
        "Back": extract_text_between_tag(chat_response, "<Back>","</Back>"),
        "Extra": extract_text_between_tag(chat_response, "<Extra>","</Extra>"),
    }
    print(extracted_card_fields)
    for _ in range(3):
        try:
            user_input = input("Add card to Anki? (Y/n): ").strip().lower()
            if user_input == 'n':
                print("Exiting without adding the card.")
                return
            response = add_anki_card(
                deck_name=deck_name,
                model_name="Basic (and reversed card with media)",
                fields=extracted_card_fields,
                tags=["swedish", "auto-generated"],
                audio=audio,
            )
            if response['error'] is not None:
                raise AnkiError("Failed to add card to Anki. Possibly Duplicate.")
            break  # Exit loop if successful
        except Exception as e:
            if isinstance(e, AnkiError):
                print(e)
            else:
                print(f"An error occurred when adding the card. Ensure Anki/Anki-connect are running and try again. Error: {e}")
    print(response)

if __name__ == "__main__":
    # main("allvarlig")
    # main("chaufför")
    # main("träna")
    parser = argparse.ArgumentParser(description="Generate Anki cards for Swedish words.")
    parser.add_argument("word", type=str, help="The Swedish word to process.")
    parser.add_argument(
        "extra_input",
        type=str,
        nargs="?",
        default=None,
        help="Optional extra input to provide additional context."
    )
    args = parser.parse_args()

    main(args.word, args.extra_input)