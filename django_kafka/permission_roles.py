def is_login(user):
    if user.is_anonymous:
        return False
    return True
