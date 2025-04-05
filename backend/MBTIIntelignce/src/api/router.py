from fastapi import Response, APIRouter

main_router = APIRouter()

@main_router.get("/ping")
def ping() -> str:
    return Response("pong", status_code=200)