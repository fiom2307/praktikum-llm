from seeds.cities_seed import seed_cities
from seeds.form_settings_seed import seed_form_settings
from seeds.story_reading_exercises_seed import seed_story_reading_exercises
from seeds.story_vocabulary_exercises_seed import seed_story_vocabulary_exercises
from seeds.story_writing_exercises_seed import seed_story_writing_exercises

def seed_all():
    seed_cities()
    seed_form_settings()
    seed_story_reading_exercises()
    seed_story_vocabulary_exercises()
    seed_story_writing_exercises()
    