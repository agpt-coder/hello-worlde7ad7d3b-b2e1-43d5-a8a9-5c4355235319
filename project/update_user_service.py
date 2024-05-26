from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UpdateUserResponse(BaseModel):
    """
    The response model containing the updated user details.
    """

    id: int
    email: str
    role: str


async def update_user(
    user_id: int, email: Optional[str], role: Optional[str]
) -> UpdateUserResponse:
    """
    This endpoint updates the details of an existing user. The request should include the user_id to update and the new user details. It is protected and can only be accessed by the user themselves or an admin.

    Args:
        user_id (int): The ID of the user to update.
        email (Optional[str]): The new email address of the user.
        role (Optional[str]): The new role of the user. Allowed values are 'Admin' and 'User'.

    Returns:
        UpdateUserResponse: The response model containing the updated user details.

    Example:
        user_id = 1
        email = "newemail@example.com"
        role = "Admin"
        update_user(user_id, email, role)
        > UpdateUserResponse(id=1, email="newemail@example.com", role="Admin")
    """
    if role and role not in ["Admin", "User"]:
        raise ValueError('Invalid role. Allowed values are "Admin" and "User".')
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        raise ValueError(f"User with ID {user_id} does not exist.")
    update_data = {}
    if email:
        update_data["email"] = email
    if role:
        update_data["role"] = prisma.enums.Role(role)
    updated_user = await prisma.models.User.prisma().update(
        where={"id": user_id}, data=update_data
    )
    return UpdateUserResponse(
        id=updated_user.id, email=updated_user.email, role=updated_user.role
    )
