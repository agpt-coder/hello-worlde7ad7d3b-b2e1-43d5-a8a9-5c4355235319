import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.create_user_service
import project.delete_user_service
import project.getHelloWorld_service
import project.helloWorld_service
import project.read_user_service
import project.say_hello_service
import project.update_user_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="hello world",
    lifespan=lifespan,
    description="create a simple api that has just one endpoint that returns hello world.",
)


@app.get(
    "/hello-world", response_model=project.getHelloWorld_service.HelloWorldResponseModel
)
async def api_get_getHelloWorld(
    request: project.getHelloWorld_service.HelloWorldRequestModel,
) -> project.getHelloWorld_service.HelloWorldResponseModel | Response:
    """
    This endpoint returns a 'Hello, world!' message. It is a simple GET request with no parameters. When a client makes a GET request to this endpoint, the server responds with a plaintext message saying 'Hello, world!'. This endpoint does not use any other APIs or perform any database operations. It simply generates and returns the hardcoded message.
    """
    try:
        res = project.getHelloWorld_service.getHelloWorld(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/v1/users/{user_id}",
    response_model=project.read_user_service.GetUserResponseModel,
)
async def api_get_read_user(
    user_id: int,
) -> project.read_user_service.GetUserResponseModel | Response:
    """
    This endpoint retrieves the details of a specific user by user_id. The response includes user information. It is protected and can be accessed by both admin and the user owning the record.
    """
    try:
        res = await project.read_user_service.read_user(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/v1/users/{user_id}",
    response_model=project.update_user_service.UpdateUserResponse,
)
async def api_put_update_user(
    user_id: int, email: Optional[str], role: Optional[str]
) -> project.update_user_service.UpdateUserResponse | Response:
    """
    This endpoint updates the details of an existing user. The request should include the user_id to update and the new user details. It is protected and can only be accessed by the user themselves or an admin.
    """
    try:
        res = await project.update_user_service.update_user(user_id, email, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/v1/users/{user_id}",
    response_model=project.delete_user_service.DeleteUserResponse,
)
async def api_delete_delete_user(
    user_id: int,
) -> project.delete_user_service.DeleteUserResponse | Response:
    """
    This endpoint deletes a specific user by user_id. It is protected and typically only an admin can delete users.
    """
    try:
        res = await project.delete_user_service.delete_user(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/v1/hello", response_model=project.say_hello_service.HelloWorldResponseModel
)
async def api_get_say_hello(
    request: project.say_hello_service.HelloWorldRequestModel,
) -> project.say_hello_service.HelloWorldResponseModel | Response:
    """
    This endpoint returns a 'hello world' message. It does not require any authentication and is accessible to everyone.
    """
    try:
        res = await project.say_hello_service.say_hello(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/hello-world", response_model=project.helloWorld_service.HelloWorldResponseModel
)
async def api_get_helloWorld(
    request: project.helloWorld_service.HelloWorldRequestModel,
) -> project.helloWorld_service.HelloWorldResponseModel | Response:
    """
    This route handles GET requests to return a 'Hello, World!' message. When a GET request is sent to '/hello-world', the request is routed to the HelloWorldResponseModule, which constructs and sends back a JSON response with the message 'Hello, World!'. No user validation is performed for this endpoint as it is publicly accessible.
    """
    try:
        res = await project.helloWorld_service.helloWorld(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/v1/users", response_model=project.create_user_service.CreateUserResponseModel
)
async def api_post_create_user(
    username: str, password: str
) -> project.create_user_service.CreateUserResponseModel | Response:
    """
    This endpoint creates a new user. The request should include user details such as username and password. This is protected and typically only an admin can create new users.
    """
    try:
        res = await project.create_user_service.create_user(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
