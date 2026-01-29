from database import SessionLocal
from services.user_service import get_user_by_username
from services.auth_service import pwd_context
import re

def reset_user_password(admin_username, child_username, new_password):
    db = SessionLocal()
    try:
        # --- admin check ---
        admin = get_user_by_username(admin_username)

        if not admin or admin.username != "admin":
            return {
                "success": False,
                "message": "Unauthorized"
            }, 403

        # --- child exists ---
        child = get_user_by_username(child_username)
        if not child:
            return {
                "success": False,
                "message": "User not found"
            }, 404

        # --- password validation ---
        if not new_password:
            return {
                "success": False,
                "message": "Password is required"
            }, 400

        # --- reset password ---
        child.password_hashed = pwd_context.hash(new_password)
        db.add(child)
        db.flush()
        db.commit()
        db.refresh(child)

        return {
            "success": True,
            "message": "Password updated successfully"
        }, 200

    finally:
        db.close()

