# app/auth/permission.py

from enum import Enum


class Permission(str, Enum):
    VIEW = "VIEW"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    MANAGE_EMPLOYEE = "MANAGE_EMPLOYEE"
    MANAGE_PROJECT = "MANAGE_PROJECT"
    MANAGE_ISSUE = "MANAGE_ISSUE"
    
class Role(str,Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    DEVELOPER = "DEVELOPER"
    
ROLE_PERMISSIONS = {

    Role.ADMIN: {
        Permission.VIEW,
        Permission.CREATE,
        Permission.UPDATE,
        Permission.DELETE,
        Permission.MANAGE_EMPLOYEE,
        Permission.MANAGE_PROJECT,
        Permission.MANAGE_ISSUE,
    },

    Role.MANAGER: {
        Permission.VIEW,
        Permission.CREATE,
        Permission.UPDATE,
        Permission.MANAGE_EMPLOYEE,
        Permission.MANAGE_PROJECT,
        Permission.MANAGE_ISSUE,
    },

    Role.DEVELOPER: {
        Permission.VIEW,
        Permission.UPDATE,
        Permission.MANAGE_ISSUE,
    },
}

def has_permission(role: str, permission: Permission) -> bool:

    permissions = ROLE_PERMISSIONS.get(role, set())

    return permission in permissions