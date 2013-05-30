# User's roles
ROLES = {
    "USER": 1,
    "ADMIN": 2
}

# Permissons
PERMISSIONS = {
    ROLES["ADMIN"]: [
        # Projects
        "create_project", "edit_project", "delete_project",
        # Stages
        "create_stage", "edit_stage", "delete_stage", "deploy_stage",
        # Tasks
        "create_task", "edit_task", "delete_task"
    ],
    ROLES["USER"]: []
}

# Deployment's statuses
STATUSES = {
    "READY": 1,
    "RUNNING": 2,
    "COMPLETED": 3,
    "CANCELED": 4,
    "FAILED": 5,
}
