import prisma
import prisma.models
from pydantic import BaseModel


class GetUserResponseModel(BaseModel):
    """
    Response model containing detailed information of the user.
    """

    id: int
    email: str
    role: str


async def read_user(user_id: int) -> GetUserResponseModel:
    """
    This endpoint retrieves the details of a specific user by user_id.
    The response includes user information. It is protected and can be accessed
    by both admin and the user owning the record.

    Args:
    user_id (int): The ID of the user to retrieve.

    Returns:
    GetUserResponseModel: Response model containing detailed information of the user.

    Example:
        user_id = 1
        user_info = await read_user(user_id)
        # user_info will contain the user's details, including id, email and role
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if user is None:
        raise ValueError("User not found")
    return GetUserResponseModel(id=user.id, email=user.email, role=user.role.value)
