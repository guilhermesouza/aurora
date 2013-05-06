# User's roles
ROLES = {
    "USER": 1,
    "ADMIN": 2
}

PERMISSIONS = {
    ROLES["ADMIN"]: ["create_project", "edit_project", "delete_project",
                     "create_stage", "edit_stage", "delete_stage",
                     "create_task", "edit_task", "delete_task"],
    ROLES["USER"]: []
}
