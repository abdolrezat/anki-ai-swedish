# Automated Anki Flashcards Generator for 🇸🇪 Swedish Vocabulary

This project automates the creation of Anki cards for Swedish words using freely available tools:

- [Lexin KTH API](https://lexin.nada.kth.se/lexin/)
- [Hugging Face Inference API / DeepSeek V3 model](https://huggingface.co/deepseek-ai)
- [AnkiConnect plugin](https://github.com/FooSoft/anki-connect)

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://gitlab.com/rezaT/anki-ai-swedish.git
cd anki-ai-swedish
```

### 2. Install Python Dependencies

```bash
pip install huggingface_hub requests wget
```
---

## 3. Hugging Face Setup

### a. Install the Hugging Face CLI

```bash
pip install huggingface_hub
```

### b. Login to Hugging Face

```bash
huggingface-cli login
```

> This will prompt you to paste your Hugging Face token. You can create one for free [here](https://huggingface.co/settings/tokens) (select "Read" access when creating the token, huggingface-cli command will save the token to ~/.cache/huggingface/token).

---

## 4. AnkiConnect Plugin Setup

### a. Install Anki

Download and install Anki if you haven't already, from [https://apps.ankiweb.net/](https://apps.ankiweb.net/).

### b. Install the AnkiConnect Plugin

1. Open Anki.
2. Go to `Tools` → `Add-ons` → `Get Add-ons`.
3. Paste the following code: `2055492159`
4. Click "OK" and restart Anki.

### c. Test the AnkiConnect Server

Ensure Anki is running, then test the connection:

```bash
curl localhost:8765
```

Example output:

```json
{"apiVersion": "AnkiConnect v.6"}
```

---

## 5. Running the Pipeline

> **Important:** Anki needs to be running for the card to be added.

The workflow is:

1. Input a Swedish word.
2. Fetch JSON response from the KTH Lexin API.
3. Strip/clean relevant content (definitions, examples, grammar).
4. Use DeepSeek V3 via Hugging Face Inference API to summarize the content into a formatted Anki card.
5. Send the card to Anki via AnkiConnect.

Run the script:

```bash
python main.py <swedish_word>
```

## 6. Create a Symlink for Easy Access

To make the script accessible from anywhere, create a symbolic link under `/usr/bin`:

```bash
sudo ln -s <path_to_main.py> /usr/bin/anki-add && sudo chmod +x /usr/bin/anki-add
```

### Running the code:

Now you can run the script using:

```bash
anki-add <swedish_word> <extra context>
```
---

Extra context is optional, it can be e.g. a sentence to include in the flashcard.

## 🔍 Example Usage

```bash
anki-add programmerare
```

### Output:
```html
<Front>programmer</Front>
<Back>programmerare</Back>
<Extra>
(en programmerare, programmeraren, programmerare, programmerarna)
Person som programmerar
<i>He works as a programmer at a tech company.</i>
Han jobbar som programmerare på ett teknikföretag.
</Extra>
```

### Other Usage Modes

The script supports three modes depending on the input:

1. **Word only**: `anki-add <word>`  
   Creates a flashcard from the Lexin dictionary definition.

2. **Word + context**: `anki-add <word> "<sentence or context>"`  
   Creates a flashcard from Lexin and includes your provided sentence/context.

3. **Context only**: `anki-add "" "<sentence or context>"`  
   Creates a flashcard directly from your sentence without dictionary lookup.


---

## 📝 License

This project is licensed under the [LGPL 3 License](https://gitlab.com/rezaT/anki-ai-swedish/-/blob/main/LICENSE). Please observe the license for the acknowledged sources:

- [Lexin API](https://lexin.nada.kth.se/lexin/)
- [Hugging Face and DeepSeek V3](https://huggingface.co/deepseek-ai)
- [AnkiConnect](https://github.com/FooSoft/anki-connect)

---