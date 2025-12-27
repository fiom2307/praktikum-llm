from database import SessionLocal
from models.form_settings_model import FormSettings

def get_form_settings():
    db = SessionLocal()
    try:
        settings = db.query(FormSettings).first()
        return settings
    finally:
        db.close()
