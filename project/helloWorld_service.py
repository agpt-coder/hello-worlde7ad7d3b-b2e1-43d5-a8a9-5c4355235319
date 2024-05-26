import datetime
from typing import Optional

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


async def log_hello_world_request(
    user_id: Optional[int], user_agent: Optional[str], ip_address: Optional[str]
) -> None:
    """
    Logs the hello world request into the HelloWorldRequestLog table.

    This function logs the details of the request like user_id, user_agent, and ip_address into
    the HelloWorldRequestLog table for future references.

    Args:
        user_id (Optional[int]): The ID of the user making the request. It can be None for anonymous requests.
        user_agent (Optional[str]): The user agent string from the request headers.
        ip_address (Optional[str]): The IP address from which the request is made.

    Returns:
        None

    Example:
        log_hello_world_request(1, 'Mozilla/5.0', '192.168.1.1')
    """
    await prisma.models.HelloWorldRequestLog.prisma().create(
        data={
            "userId": user_id,
            "userAgent": user_agent,
            "ipAddress": ip_address,
            "timestamp": datetime.datetime.now(),
        }
    )


async def helloWorld(request: HelloWorldRequestModel) -> HelloWorldResponseModel:
    """
    This route handles GET requests to return a 'Hello, World!' message. When a GET request is sent to '/hello-world', the request is routed to the HelloWorldResponseModel, which constructs and sends back a JSON response with the message 'Hello, World!'. No user validation is performed for this endpoint as it is publicly accessible.

    Args:
    request (HelloWorldRequestModel): The request model for the /api/v1/hello endpoint. This endpoint does not require any parameters.

    Returns:
    HelloWorldResponseModel: The response model for the /api/v1/hello endpoint. It contains a simple message field.

    Example:
        helloWorld(HelloWorldRequestModel())
        > HelloWorldResponseModel(message='Hello, World!')
    """
    user_id = None
    user_agent = "ExampleUserAgent"
    ip_address = "127.0.0.1"
    await log_hello_world_request(user_id, user_agent, ip_address)
    response = HelloWorldResponseModel(message="Hello, World!")
    return response
