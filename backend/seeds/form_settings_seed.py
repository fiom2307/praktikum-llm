from database import SessionLocal
from models import FormSettings

def seed_form_settings():
    db = SessionLocal()

    default_settings = {
        "id": 1,
        "pretest_enabled": False,
        "pretest_url": "https://docs.google.com/forms/d/e/1FAIpQLScH3j7FehXKkRrXw_Xdd-nbVdgHYghE8r8G_xB4adRKt8pKcg/viewform?usp=pp_url&entry.1646617742=",
        "posttest_enabled": False,
        "posttest_url": "https://docs.google.com/forms/d/e/1FAIpQLScjRTjcD2RVHFdEYZF2-rMsCglGqn09YGpv2NHiLDLHVqbvQQ/viewform?usp=pp_url&entry.170677882=",
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
