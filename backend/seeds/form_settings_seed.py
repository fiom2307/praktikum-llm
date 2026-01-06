from database import SessionLocal
from models.form_settings_model import FormSettings

def seed_form_settings():
    db = SessionLocal()

    default_settings = {
        "id": 1,
        "pretest_enabled": False,
        "pretest_url": "https://docs.google.com/forms/d/e/1FAIpQLSet9c40nwjKGZ6XGJ2tPWj0hW_960yl0xfAYSaIRm8-pTfaIw/viewform?usp=pp_url&entry.1458977373=",
        "posttest_enabled": False,
        "posttest_url": "https://docs.google.com/forms/d/e/1FAIpQLSet9c40nwjKGZ6XGJ2tPWj0hW_960yl0xfAYSaIRm8-pTfaIw/viewform?usp=pp_url&entry.1458977373=",
    }

    settings = db.query(FormSettings).filter(FormSettings.id == 1).first()

    if settings:
        # UPDATE if exists
        for key, value in default_settings.items():
            setattr(settings, key, value)
    else:
        # INSERT if doesnt exist
        db.add(FormSettings(**default_settings))

    db.commit()
    db.close()
