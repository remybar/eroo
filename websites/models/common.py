def get_photo_dir_path(instance, filename):
    return f"websites/{instance.website.key}/photos/{filename}"


def get_review_dir_path(instance, filename):
    return f"websites/{instance.website.key}/reviews/{filename}"
