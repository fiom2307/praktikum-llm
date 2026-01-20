from database import SessionLocal
from models import Flashcard
from services.openai_service import generate_from_prompt

def save_flashcard(user_id, word, definition=None):
    db = SessionLocal()
    try:
        # check duplicates
        existing = (
            db.query(Flashcard)
            .filter(Flashcard.user_id == user_id, Flashcard.word == word)
            .first()
        )

        if existing:
            return existing

        if not definition:
                
            prompt = f"""
We play two games: (1) “Sounds Like A Word” and (2) “StoryWeave”.

STEP 0: INPUT + NORMALIZATION (must happen before Step 1)

SCOPE

- Exactly ONE target word per run. If multiple words are provided, process only the first.
- Do not ask questions. Assume input is correct and complete.
- Output MUST be ONLY the STRICT OUTPUT block. No meta text.

INPUT

Vocabolo: {word}

Significato: **MEANING_DE**

Genere (italiano): **GENDER_IT**

GENERE HANDLING (critical)

Allowed values for **GENDER_IT**: m, f, verb, adj.

- Add a German article before the Italian target ONLY if **GENDER_IT** is m or f.
- If **GENDER_IT** is verb or adj: NEVER add a German article before the target.
- In output:
  - If **GENDER_IT** is m or f: print the line "Genere (italiano): m/f".
  - If **GENDER_IT** is verb or adj: do NOT print any "Genere (italiano)" line.

ITALIAN ARTICLE STRIP (ALWAYS)

If {word} starts with an Italian article/determiner (il, lo, la, l’, l', i, gli, le, un, uno, una),
REMOVE it and define TARGET_CORE as the remaining word(s).

From this point on:
- Use TARGET_CORE for keyword phonetics.
- Print TARGET_CORE everywhere in output (Vocabolo line, story reveal, summary reveal).
- Never print the removed Italian article anywhere.

========================
STEP 1: Game “Sounds Like A Word”
========================

GOAL

Find 2-4 German keywords that, spoken in sequence, sound similar to TARGET_CORE. Phonetics first.

KEYWORD RULES (HARD)

1) German-only (STRICT): each keyword must be a common German dictionary word in its standard form. No foreign-language words, no invented forms.
2) Dominant-association rule: choose words whose FIRST association for a smart 9th grade audience matches the intended image/concept. Avoid “secondary/rare meanings” as a trick.
3) Names policy:
   - Common FIRST NAMES allowed (clearly perceived as first names).
   - SURNAMES forbidden.
   - Use at most ONE name total.
4) Function words / articles forbidden as keywords (HARD-FAIL):
   denn, und, aber, oder, weil, dass, wenn, der, die, das, den, dem, des, ein, eine, einen,
   dann, noch, hier, dort, wieder, um, im, am, in, zu, zur, zum, ohne.
   Hard-fail rule: If any forbidden token appears in Parole chiave, regenerate keywords.
5) No single letters or filler interjections: O/Oh/Ah/N/Äh/Hm etc.
6) Min length: each keyword ≥ 3 letters (phrases allowed, but each word ≥ 3).
7) Standalone words only: no prefixes/suffixes/morpheme pieces (un-, ver-, -ung, -keit, -chen, -los, …).
8) Capitalization MUST match German norms:
   - Nouns capitalized in keyword list (Paar, Rolle).
   - Verbs/adjectives/adverbs lowercase (pressen, immer).
   - Names capitalized.
9) Anti-“single-letter/single-sound” (CRITICAL):
   - Do NOT pick a keyword mainly to cover ONE letter/one simple sound.
   - Each keyword must plausibly match at least a 2-letter/2-sound chunk (im-, le-, pre-, son-, ran-, can-).
   - First keyword must cover more than a single vowel/letter.
   - Prefer fewer, closer keywords; merge segments if needed.
10) Technical/science terms are allowed IF common in school context and conceptually clear for 9th grade (e.g., Ionen is OK). Avoid obscure jargon.

EXAMPLES (Step 1; illustrative only)

stazione → [Stadt, Zone]
cucina → [Kuh, China]
domani → [Dom, Mann, nie]
buonanotte → [Bohne, Not, Tee]

Output of Step 1:

_Parole chiave: [<k1>, <k2>, ...]_

====================
STEP 2: Game “StoryWeave”
====================

GOAL

Write a short German story + 1-sentence summary. Use keywords as a phonetic chain; TARGET_CORE is the final reveal.

ARTICLE CUE (German article before the Italian target)

- If **GENDER_IT** is verb or adj: no German article before TARGET_CORE.
- If **GENDER_IT** is m or f: place a German definite article immediately before TARGET_CORE.
  Choose CASE by correct German grammar of your final sentence.

Forms: m der/den/dem/des ; f die/die/der/der

IMPORTANT (no contractions)

Do NOT use contracted forms that hide the article (e.g., “zur”, “zum”, “ins”, “im”, “am”).
Write the separate article explicitly (e.g., “zu der …”, “zu dem …”, “in das …”).

TARGET + KEYWORD FORMATTING (critical)

- In Storia and Riassunto: each keyword must be bold: **Keyword**
- TARGET_CORE must also be bold: **TARGET_CORE**

STORY RULES (HARD)

1) Keywords appear EXACTLY ONCE, in EXACT order, in BOTH story and summary.
2) Each keyword must be a standalone token (spaces/punctuation), not inside other words, not compounds, not hyphen-joined.
3) Keywords must be unchanged (no inflection/derivation/capitalization change).
4) REVEAL RULE (CRITICAL):
   - TARGET_CORE appears exactly once in the story and once in the summary, only AFTER the last keyword.
   - TARGET_CORE is the final word of the story and the final word of the summary (punctuation allowed after).
   - No keyword may appear after TARGET_CORE.
5) Plot-faithful summary: no new facts/characters/places/solutions; same events/outcome.
6) Audience: smart 9th grade; classroom-safe.
7) Length: Storia 3-5 sentences. Riassunto 1 sentence.
8) Story flow rule (style, but required):
   Avoid “one keyword per sentence” writing. At least one sentence must contain TWO keywords (still in order), without sounding forced.

STORY COHERENCE RULES (required)

- The story must be a coherent mini-scene with a clear setting (school / everyday life / project / trip) and a clear point (goal, discovery, decision, insight).
- Use each keyword in its dominant, everyday meaning (the first association). Do NOT rely on rare/secondary meanings.
- Avoid vague fillers (seltsam, irgendwie, plötzlich) unless there is a concrete cause.
- Keep tone neutral-to-positive; avoid horror atmosphere unless the meaning itself requires it.

OUTPUT LABEL FORMATTING (critical)

- In the STRICT OUTPUT block, the labels must be exactly: "Storia:" and "Riassunto:" (no underscores, no extra characters).
- The Parole chiave line must be italic and contain only the bracketed list.

EXAMPLES (Step 2; follow constraints)

Vocabolo: stazione
Significato: Bahnhof
Genere (italiano): f

Parole chiave: [Stadt, Zone]

Storia: In der **Stadt** testen wir im Geografieprojekt, wie man ohne Handy navigiert. Auf der Karte ist eine **Zone** markiert, in der wir uns sammeln sollen, falls jemand verloren geht. Von dort folgen wir den Schildern und erreichen pünktlich die **stazione**.

Riassunto: In der **Stadt** führt uns die **Zone** bis zu der **stazione**.

Vocabolo: cucina
Significato: Küche
Genere (italiano): f

Parole chiave: [Kuh, China]

Storia: Auf dem Bauernhof steht eine **Kuh** direkt neben dem kleinen Hofladen. Drinnen hängt ein Kalender aus **China**, den die Familie als Geschenk bekommen hat. Dann riecht es nach frischem Essen aus der **cucina**.

Riassunto: Neben der **Kuh** hängt etwas aus **China**, und es duftet herrlich aus der **cucina**.

Vocabolo: volare
Significato: fliegen

Parole chiave: [Wolle, Alarm, Reh]

Storia: In der AG testen wir einen Mini-Gleiter; ein Büschel **Wolle** zeigt die Windrichtung. Beim Start piept der **Alarm**, und am Wiesenrand schaut ein **Reh** still zu. Für einen Moment wirkt es, als könnten wir selbst **volare**.

Riassunto: **Wolle**, **Alarm** und ein **Reh** begleiten den Test, und der Gedanke bleibt: **volare**.

====================
STRICT OUTPUT (ONLY)
====================

If **GENDER_IT** is m or f:

Vocabolo: **TARGET_CORE**
Significato: **MEANING_DE**
Genere (italiano): **GENDER_IT**

_Parole chiave: [<k1>, <k2>, ...]_
Storia: <German text>
Riassunto: <German text>

If **GENDER_IT** is verb or adj:

Vocabolo: **TARGET_CORE**
Significato: **MEANING_DE**

_Parole chiave: [<k1>, <k2>, ...]_
Storia: <German text>
Riassunto: <German text>

FINAL CHECK (do not print)

- If **GENDER_IT** is m/f: "Genere (italiano)" line present; if verb/adj: no such line.
- Labels exactly "Storia:" and "Riassunto:"; Parole chiave line is italic and contains only the bracketed list.
- Step 1 hard-fail respected: no function words/articles in keywords.
- Each keyword appears exactly once in story and once in summary, bolded, unchanged, standalone, correct order.
- TARGET_CORE appears exactly once in story and once in summary, bolded, only after last keyword, and is final word in both.
- Article used ONLY if **GENDER_IT** is m/f, written explicitly (no contractions).
- Story flow rule met: at least one sentence contains two keywords in order.

If any check fails: revise and regenerate.
"""



            definition = generate_from_prompt(prompt).strip()

        new_card = Flashcard(
            user_id=user_id,
            word=word,
            definition=definition
        )

        db.add(new_card)
        db.commit()
        db.refresh(new_card)

        return new_card
    finally:
        db.close()

def get_flashcards(user_id):
    db = SessionLocal()
    try:
        return db.query(Flashcard).filter(Flashcard.user_id == user_id).all()
    finally:
        db.close()