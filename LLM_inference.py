from huggingface_hub import InferenceClient

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

def get_prompt(input_json):
    system_prompt = f"""
    Instructions: the following json are contents from a dictionary. Generate a concise Anki flash card with the Swedish word and its translations to English, it is possible to include a few synonyms if they are very close in meaning. In the field "Extra", we want to have example sentences (but not too long paragraphs) with both Swedish and translation, important grammatical and other info to help user learn better, can be left empty if not necessary. Only swedish in Back and English in Front. Keep the front and back lean and include swedish descriptions as well as english (english should come before swedish) in extra. Only generate the flash card within the provided tags (Front, Back, Extra) so they are parsed, add simple html to Extra to discern english and swedish words, avoid unnecessary general words (like "English", "Swedish","Inflection:").  for verbs, Extra should include this format 〈att, , har , är, !〉
    Example output: 
    <Front>mild, minor</Front>
    <Back>lindrig | mild</Back>
    <Extra>(lindrigt, lindriga)<br> Inte allvarlig, obetydlig, lätt<br><br><i>She only suffered minor injuries in the accident.</i><br>hon fick bara lindriga skador vid olyckan</Extra>

    Input json: {input_json}
    """
    return system_prompt

def hf_chat(
    input_json: str,
    verbose: int = 1,
) -> str:
    client = InferenceClient()

    system_prompt = get_prompt(input_json=input_json)
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
