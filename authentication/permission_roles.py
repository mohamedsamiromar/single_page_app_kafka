def is_student(user):
    if user.is_anonymous:
        return False
    return user.profile.is_student