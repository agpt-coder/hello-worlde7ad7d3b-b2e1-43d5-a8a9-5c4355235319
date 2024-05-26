from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class HelloWorldRequestModel(BaseModel):
    """
    The request model for the /api/v1/hello endpoint. This endpoint does not require any parameters.
    """

    pass


class HelloWorldResponseModel(BaseModel):
    """
    The response model for the /api/v1/hello endpoint. It contains a simple message field.
    """

    message: str


async def log_request(user_agent: str, ip_address: str):
    """
    Logs the incoming request to the database.

    Args:
        user_agent (str): The user agent of the request.
        ip_address (str): The IP address of the request.

    Returns:
        None
    """
    await prisma.models.HelloWorldRequestLog.prisma().create(
        data={
            "userAgent": user_agent,
            "ipAddress": ip_address,
            "timestamp": datetime.utcnow(),
        }
    )


async def say_hello(request: HelloWorldRequestModel) -> HelloWorldResponseModel:
    """
    This endpoint returns a 'hello world' message. It does not require any authentication and is accessible to everyone.

    Args:
    request (HelloWorldRequestModel): The request model for the /api/v1/hello endpoint. This endpoint does not require any parameters.

    Returns:
    HelloWorldResponseModel: The response model for the /api/v1/hello endpoint. It contains a simple message field.

    Example:
        request = HelloWorldRequestModel()
        response = say_hello(request)
        assert response.message == "Hello, world!"
    """
    user_agent = "some_user_agent"
    ip_address = "127.0.0.1"
    await log_request(user_agent, ip_address)
    response = HelloWorldResponseModel(message="Hello, world!")
    return response
