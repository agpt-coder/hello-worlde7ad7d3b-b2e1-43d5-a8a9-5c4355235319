from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CreateUserResponseModel(BaseModel):
    """
    This response model will return the newly created user details.
    """

    id: int
    username: str
    email: Optional[str] = None
    role: prisma.enums.Role


async def create_user(username: str, password: str) -> CreateUserResponseModel:
    """
    This endpoint creates a new user. The request should include user details such as username and password. This is protected and typically only an admin can create new users.

    Args:
    username (str): The username for the new user.
    password (str): The password for the new user.

    Returns:
    CreateUserResponseModel: This response model will return the newly created user details.

    Example:
        response = await create_user("newuser", "password123")
        print(response)
        # CreateUserResponseModel(id=1, username='newuser', email=None, role=prisma.enums.Role.User)
    """
    user = await prisma.models.User.prisma().create(
        data={"email": username, "role": "User"}
    )
    return CreateUserResponseModel(id=user.id, username=user.email, role=user.role)
