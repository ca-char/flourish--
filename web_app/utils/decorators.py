from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Admins can only access this page.", category="error")
            return redirect(url_for("views.user_base"))
        return f(*args, **kwargs)
    return decorated_function

def regular_user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            flash("Regular users can only access this page.", category="error")
            return redirect(url_for("views.admin_base"))
        return f(*args, **kwargs)
    return decorated_function
