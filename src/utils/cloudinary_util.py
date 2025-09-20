def create_public_id(username: str, local_id: int, recipe_local_id: int) -> str:
    """Creating uniq public id, contains from `folder_name`/`some_id`"""
    return f"{username}/{local_id}_{recipe_local_id}"
