from huggingface_hub import InferenceClient
import argparse
import json

huggingface_models = [
    # Chat / Instruction-following
    "deepseek-ai/DeepSeek-V2-Chat",
    "deepseek-ai/DeepSeek-V3-0324",
    # "meta-llama/Llama-3-8b-chat-hf",
    "meta-llama/Llama-3.1-8B",
    "facebook/mbart-large-50-many-to-many-mmt",
    # "meta-llama/Llama-3-70b-chat-hf",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "Qwen/Qwen1.5-7B-Chat",
    "google/gemma-1.1-7b-it"
    "meta-llama/Llama-2-7b-chat",
    "meta-llama/Llama-3.1-8B-Instruct",
    # Text Generation / Summarization
    "google/flan-t5-small",
    "google/flan-t5-xl",
    "facebook/bart-large-cnn",
    # Translation
    "Helsinki-NLP/opus-mt-en-fr",
    "Helsinki-NLP/opus-mt-en-de",
    # Embeddings / Semantic Search
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
    "BAAI/bge-base-en-v1.5",
    "intfloat/e5-base",
    # Code Models
    "bigcode/starcoder",
    "deepseek-ai/DeepSeek-Coder-6.7B-instruct",
    "WizardLM/WizardCoder-Python-34B-V1.0",
    # Vision-Language (Multimodal)
    "Salesforce/blip-image-captioning-base",
    "openai/clip-vit-base-patch32",
    # Speech-to-Text (ASR)
    "openai/whisper-large-v3",
    "distil-whisper/distil-large-v3.5"
]

selected_model = huggingface_models[1]
print("Using model:", selected_model)

def get_prompt(input_json, extra_user_input=None):
    """
    Three modes:
    1. input_json only: creates flashcard from lexin response
    2. input_json and extra input: same as 1 but also includes the sentences and context from extra in the flashcard
    3. only extra input: creates a flashcard for the sentence
    """

    if input_json:
        input_extra = f"""
            Ensure that the following sentence / context is included in <Extra>: {extra_user_input}
            """  if extra_user_input else ''
        system_prompt = f"""
        Instructions: the following json are contents from a dictionary. Generate a concise Anki flash card with the Swedish word and its translations to English, it is possible to include a few synonyms if they are very close in meaning. In the field "Extra", we want to have example sentences (but not too long paragraphs) with both Swedish and translation, important grammatical and other info to help user learn better, can be left empty if not necessary. Only swedish in Back and English in Front. Keep the front and back lean and include swedish descriptions as well as english (english should come before swedish) in extra. Only generate the flash card within the provided tags (Front, Back, Extra) so they are parsed, add simple html to Extra to discern english and swedish words, avoid unnecessary general words (like "English", "Swedish","Inflection:").  for verbs, Extra should include this format 〈att, , har , är, !〉
        Example output: 
        <Front>mild, minor</Front>
        <Back>lindrig | mild</Back>
        <Extra>(lindrigt, lindriga)<br> Inte allvarlig, obetydlig, lätt<br><br><i>She only suffered minor injuries in the accident.</i><br>hon fick bara lindriga skador vid olyckan</Extra>

        Input json: {input_json} 
        {input_extra}
        """
    elif input_json is None and extra_user_input:
        system_prompt = f"""
        Instructions: A context / sentence is provided between tags <sentence>, where user is asking how to say something in everyday Swedish (or is guessing the sentence in Swedish and may need to be corrected for grammatical errors). Generate a concise Anki flash card of the sentence in Swedish and their translation in English. One or two sentences can be added to make it sound like a natural dialogue between two persons (e.g. question and answer). In the field "Extra", we want to have perhaps 1-2 alternatives to the dialogue (as something can be said in different ways) or important grammatical and other info to help user learn better, the Extra field can be left empty if not necessary. Only swedish in Back and English in Front. Only generate the flash card within the provided tags (Front, Back, Extra) so they are parsed, add simple html to Extra to discern english and swedish words. 
        Example sentence: when does the next ferry go? 
        Example output: 
        <Front><i>- When does the next ferry go?</i> <br><i>- The last one will go 11.</i></Front>
        <Back>- När går nästa färja? <br>- Den sista går kl. 11:00.</Back>
        <Extra><br>- Vilken tid avgår nästa färja?<br>- Den sista avgår klockan 11.<br><br><i>- What time does the next ferry depart?<br>- The last one departs at 11.</i><br>- Vilken tid avgår nästa färja?<br>- Den sista avgår klockan 11.</Extra>

        <sentence>{extra_user_input}</sentence>
        """
    return system_prompt

def hf_chat(
    input_json: str,
    extra_user_input: str = None,
    verbose: int = 1,
) -> str:
    client = InferenceClient()

    system_prompt = get_prompt(input_json=input_json, extra_user_input = extra_user_input)

    if verbose:
        print("============ SYSTEM PROMPT =========================")
        print(system_prompt)
    completion = client.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": "system", "content": system_prompt},
        ],
    )
    response = completion.choices[0].message.content
    if verbose:
        print("============ RESPONSE =========================")
        print(response)

    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run hf_chat with input JSON and optional extra user input.")
    parser.add_argument("input_json", type=str)
    parser.add_argument("extra_user_input", type=str, nargs="?", help="Additional user input for the prompt.", default=None)

    args = parser.parse_args()

    # Load JSON from file if input_json is a file path
    input_json = None if args.input_json == "" else args.input_json

    response = hf_chat(
        input_json=None,
        extra_user_input=args.extra_user_input,
    )