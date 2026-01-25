from huggingface_hub import InferenceClient
import argparse
import json

huggingface_models = [
    # === TIER 1: Best for Swedish + Instruction Following ===
    "deepseek-ai/DeepSeek-V3",                    # Current best - excellent multilingual including Swedish
    "Qwen/Qwen2.5-72B-Instruct",                  # Excellent multilingual, very strong instruction following
    "meta-llama/Llama-3.3-70B-Instruct",          # Latest Llama, good multilingual support
    "meta-llama/Llama-3.1-70B-Instruct",          # Strong instruction following
    
    # === TIER 2: Good alternatives (smaller/faster) ===
    "Qwen/Qwen2.5-32B-Instruct",                  # Good balance of size and capability
    "meta-llama/Llama-3.1-8B-Instruct",           # Your current fallback - decent
    "mistralai/Mistral-Small-Instruct-2409",      # Updated Mistral with good multilingual
    "mistralai/Mixtral-8x22B-Instruct-v0.1",      # Larger Mixtral, better than 8x7B
    
    # === TIER 3: Specialized (if you want to experiment) ===
    "google/gemma-2-27b-it",                      # Updated Gemma 2
    "google/gemma-2-9b-it",                       # Smaller Gemma 2
    "nvidia/Llama-3.1-Nemotron-70B-Instruct",     # Nvidia-tuned for helpfulness
]

selected_model = huggingface_models[0]  # DeepSeek-V3 is excellent choice
# selected_model = huggingface_models[1]

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
        Instructions: the following json are contents from a dictionary. Generate a concise Anki flash card with the Swedish word and its translations to English, it is possible to include a few synonyms if they are very close in meaning. In the field "Extra", we want to have definition in swedish, example sentences (but not too long paragraphs) with both Swedish and translation, important grammatical and other info to help user learn better, can be left empty if not necessary. Only swedish in Back and English in Front, only one card including all the meanings stated in the input. Keep the front and back lean and include swedish descriptions as well as english (english should come before swedish) in extra, observe the placement of tags used for swedish (<sub>) vs. english (<i>) according to example outputs (Important: <sub> is only for 'Example' field and example sentences, not for Definition.Content and definition that appears in the beginning of extra). Only generate the flash card within the provided tags (Front, Back, Extra) so they are parsed, add simple html to Extra to discern english and swedish words, avoid unnecessary general words (like "English", "Swedish","Inflection:").  for verbs, Extra should include this format 〈att, , har , är, !〉
        Example output 1: 
        <Front>mild, minor</Front>
        <Back>lindrig | mild</Back>
        <Extra>(lindrigt, lindriga)<br> Inte allvarlig, obetydlig, lätt<br><br><i>She only suffered minor injuries in the accident.</i><br>hon fick bara lindriga skador vid olyckan</Extra>
        Example output 2:
        <Front>not care about, ignore</Front>
        <Back>strunta (i)</Back>
        <Extra>〈att strunta, struntade, har struntat, är struntande, strunta!〉<br>Bryr sig inte om, låter bli<br><br><i>She ignored washing the windows.</i><br>hon struntade i att tvätta fönstren<br><br><i>We'll just ignore it.</i><br><sub>vi struntar i det</sub></Extra>
        Example output 3 (nouns, include en/ett):
        <Front>a spy</Front>
        <Back>en spion</Back>
        <Extra>(spionen, spioner, spionerna)<br>  
        person som ägnar sig åt spioneri<br><br>  
        <i>The spy got life imprisonment.</i><br>  
        <sub>spionen fick livstids fängelse</sub><br><br>  
        </Extra>
        
        Input json: {input_json} 
        {input_extra}
        """
    elif input_json is None and extra_user_input:
        system_prompt = f"""
        Instructions: A context / sentence is provided between tags <sentence>, where user may be asking how to say something in everyday Swedish (or is guessing the sentence in Swedish and may need to be corrected for grammatical errors). Generate a concise Anki flash card of the context/sentence in Swedish and their translation in English. If the user input is a single sentence, one or two sentences can be added to make it sound like a natural dialogue between two persons (e.g. question and answer). If the user input is multiple sentences, include all of them in the card, with all english in <Front> and all swedish sentences in <Back>. In the field "Extra", we want to have perhaps 1-2 alternatives to the dialogue (as something can be said in different ways) or important grammatical and other info to help user learn better, the Extra field can be left empty if not necessary or the alternatives are already provided in multiple sentences. Only swedish in Back and English in Front. Only generate one flash card within the provided tags (Front, Back, Extra) so they are parsed, add simple html to Extra to discern english and swedish words. 
        Example sentence: when does the next ferry go? 
        Example output 1: 
        <Front><i>- When does the next ferry go?</i> <br><i>- The last one will go 11.</i></Front>
        <Back>- När går nästa färja? <br>- Den sista går kl. 11:00.</Back>
        <Extra><br>- Vilken tid avgår nästa färja?<br>- Den sista avgår klockan 11.<br><br><i>- What time does the next ferry depart?<br>- The last one departs at 11.</i><br>- Vilken tid avgår nästa färja?<br>- Den sista avgår klockan 11.</Extra>
        Example output 2:
        <Front><i>- Are you coming on the bike tour tomorrow?</i> <br><i>- I don’t think I can, I’ve got quite a bit to do.</i> <br><i>- No worries! We’re going anyway.</i> <br><i>- Hope it’s fun!</i> <br><i>- It will be! See you another time.</i></Front>
        <Back>- Ska du med på cykelturen imorgon? <br>- Jag tror inte jag kan, jag har ganska mycket att göra. <br>- Det är lugnt! Vi kör ändå. <br>- Hoppas det blir kul! <br>- Det blir det! Vi ses en annan gång.</Back>
        <Extra></Extra>
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