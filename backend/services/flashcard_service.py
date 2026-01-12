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
            
            prompt = f"""We play two games now. The first game is called “Sounds Like A Word”:

                GAME OBJECTIVE

                The objective of this linguistic game is to dissect a target word into syllables and find an array of common real words that, when pronounced, produce a similar sound to the target word. This game is not about spelling, but about phonetics.

                CONTEXT

                - The target word is in Italian (L2).
                - The keywords must be in German (L1).
                - The audience is Grade 8.
                - The final response (verbal cue) must be written in German (L1).

                INPUT

                Il vocabolo: {word}
                Il significato: **MEANING_DE**

                GAME RULES (KEYWORDS)

                1) Each part of the target word should correspond with a standalone word, not a prefix or a suffix.
                2) The words selected should be suitable for 8th graders with L1 German for learning Italian as L2 in the second year. Avoid obscure or rare words.
                3) The goal is to find words that sound like the target word when pronounced together, not necessarily to match the exact number of syllables.
                4) Players must correctly split each target word into syllables and locate common words that closely match these syllables in sound.
                5) Avoid slang, offensive, or sexually suggestive words.
                6) The keywords must be real German words (L1) that sound similar to the Italian (L2) target word when pronounced together.

                EXAMPLES (KEYWORDS)

                Input: stazione → Output: [Stadt, Zone]
                Input: domani → Output: [Dom, Mann, nie]
                Input: ragione → Output: [Rad, schonen]
                Input: cucina → Output: [Kuh, China]
                Input: contadino → Output: [Konto, Dino]
                Input: buonanotte → Output: [Bohne, Not, Tee]
                Input: piccolo → Output: [Pik, Koloss]

                NEXT TASK

                Now proceed with the next game and next task using the generated keywords.
                The next game is called “StoryWeave”.

                INTERNAL VARIABLE (for StoryWeave)

                - KEYWORDS = the Keywords list generated in “Sounds Like A Word”.
                - Do NOT change KEYWORDS after generating them.

                GAME DESCRIPTION

                In StoryWeave, players craft a story using the target word and the keywords in the exact order given. After the story, they must produce a summary that also contains the keywords in the same order.

                CONTEXT (STORYWEAVE)

                - The story and the summary must be written in German (L1).
                - The target word must appear exactly as the Italian (L2) word.
                - The keywords remain German (L1) and must appear in the exact order.

                INPUT

                Il vocabolo: {word}
                Il significato: **MEANING_DE**
                KEYWORDS (from “Sounds Like A Word”)
                Italian gender (m/f): **MEANING_DE**

                ARTICLE CUE

                Use German definite articles with correct German case, but choose the gender based on **MEANING_DE**, not on the German translation.

                GAME RULES / CONSTRAINTS (STORYWEAVE)

                1) The target word must appear in the story.
                2) The keywords must appear exactly in the given order.
                3) A summary must be produced after the story.
                4) Keywords must not be rearranged.
                5) Story and summary must reflect the same plot.
                6) Use Grade 8-appropriate, classroom-safe German.
                7) Provide clear context so the meaning is inferable.

                STRICT OUTPUT & CHECKING RULES

                - Output only these four parts (no extra text):

                Vocabolo: {word}
                
                Significato: **MEANING_DE**

                Parole chiave: [<k1>, <k2>, ...]
                
                Storia: <German text>
                
                Riassunto: <German text>

                - The Italian target word must appear exactly as "{word}".
                - Reuse exactly the same keyword tokens in Story and Summary:
                * exact order, exact spelling (case-sensitive)
                * standalone words
                * no inflection
                * each keyword exactly once in Story and exactly once in Summary
                - Formatting rule: wrap each keyword occurrence with **double asterisks**.

                EXAMPLES (STORYWEAVE)

                [Input]
                Target word: stazione
                Meaning: Bahnhof
                Keywords: Stadt, Zone

                [Output]
                Story: In einer fremden **Stadt** stehen wir plötzlich ohne Plan da. Auf der Karte ist eine **Zone** markiert, und genau dort finden wir die stazione.
                Summary: In der **Stadt** zeigt uns die **Zone** den Weg zur stazione.

                [Input]
                Target word: ragazzo
                Meaning: Junge
                Keywords: Rad, Katze

                [Output]
                Story: Ein Junge fährt mit dem **Rad** über den Hof und bremst vor einer **Katze**. Die Lehrerin sagt: ragazzo, pass auf!
                Summary: Ein ragazzo kommt mit dem **Rad** und bremst vor der **Katze**.

                [Input]
                Target word: cucina
                Meaning: Küche
                Keywords: Kuh, China

                [Output]
                Story: In der cucina hängt ein Bild von einer **Kuh** und daneben ein Kalender aus **China**.
                Summary: In der cucina hängt das Bild einer **Kuh** neben dem Kalender aus **China**.

                [Input]
                Target word: contadino
                Meaning: Bauer
                Keywords: Konto, Dino

                [Output]
                Story: Der contadino schaut auf sein **Konto** und füttert den **Dino**.
                Summary: Der contadino prüft das **Konto**, während der **Dino** frisst.
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