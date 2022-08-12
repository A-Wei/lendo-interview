from fastapi import FastAPI
from uuid import UUID
from .service import (
    create_application,
    fetch_application_by_id,
    fetch_application_by_status,
    update_application_status_by_id
)
from .constant import ApplicationIn, ApplicationStatus
from .rmq_client import rmq_client


app = FastAPI()


@app.post("/application/")
async def post_application(
        application: ApplicationIn
):
    try:
        db_application = await create_application(application)
    except Exception as error:
        raise error

    if db_application:
        message = {
            "id": str(db_application.id),
            "first_name": db_application.first_name,
            "last_name": db_application.last_name
        }
        await rmq_client(message)

        return {"success": True, "application_id": db_application.id}
    else:
        return {"success": False, "msg": "application creation failed"}


@app.get("/application/{uuid}")
async def get_application(uuid: UUID):
    try:
        db_application = await fetch_application_by_id(uuid)
    except Exception as error:
        raise error

    if db_application:
        return {"success": True, "data": db_application}
    else:
        return {"success": False, "msg": "No application found"}


@app.put("/application/{uuid}")
async def update_application(
        uuid: UUID,
        data: ApplicationStatus
):
    try:
        db_application = await update_application_status_by_id(uuid, data)
    except Exception as error:
        raise error

    if db_application:
        return {"success": True}
    else:
        return {"success": False, "msg": "Application status not updated"}


@app.get("/applications/{status}")
async def get_applications_with_status(status: str):
    try:
        db_application = await fetch_application_by_status(status)
    except Exception as error:
        raise error

    if db_application:
        return {"success": True, "data": db_application}
    else:
        return {"success": False, "msg": "No applications found"}
