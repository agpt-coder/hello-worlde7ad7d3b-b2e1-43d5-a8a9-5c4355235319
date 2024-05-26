import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    This response model returns a status message indicating whether the user was successfully deleted or not.
    """

    status: str


async def delete_user(user_id: int) -> DeleteUserResponse:
    """
    This endpoint deletes a specific user by user_id. It is protected and typically only an admin can delete users.

    Args:
        user_id (int): The ID of the user to be deleted.

    Returns:
        DeleteUserResponse: This response model returns a status message indicating whether the user was successfully deleted or not.

    Example:
        response = await delete_user(user_id=1)
        > response.status == "User successfully deleted" or "User not found"
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await prisma.models.HelloWorldRequestLog.prisma().delete_many(
        where={"userId": user_id}
    )
    await prisma.models.AccessLog.prisma().delete_many(where={"userId": user_id})
    await prisma.models.User.prisma().delete(where={"id": user_id})
    return DeleteUserResponse(status="User successfully deleted")
