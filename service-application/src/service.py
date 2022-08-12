import uuid

from sqlalchemy.orm import Session
from sqlalchemy import update, text

from .constant import ApplicationIn, ApplicationModel, ApplicationStatus, ApplicationOut
from .db import get_db


async def create_application(
        application: ApplicationIn
) -> ApplicationOut:

    query = """
        INSERT INTO applications ("id", "first_name", "last_name", "status")
        VALUES (:id, :first_name, :last_name, :status)
    """
    app_values = {
        "id": str(uuid.uuid4()),
        "first_name": application.first_name,
        "last_name": application.last_name,
        "status": "pending"
    }
    db = await get_db()
    db.execute(text(query), app_values)

    return ApplicationOut.parse_obj(app_values)


async def fetch_application_by_id(uuid: uuid):
    query = """
        SELECT 
            *
        FROM applications
        WHERE id = :id
    """
    db = await get_db()
    cursor = db.execute(text(query), {"id": uuid})

    application = cursor.fetchone()

    return application


async def update_application_status_by_id(
        uuid: uuid,
        data: ApplicationStatus
):
    query = """
            UPDATE applications 
            SET 
                status = :status,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :id
        """

    db = await get_db()
    try:
        db.execute(text(query), {"id": uuid, "status": data.status.value})
        return True
    except:
        return False


async def fetch_application_by_status(status: str):
    query = """
            SELECT 
                *
            FROM applications
            WHERE status = :status
        """
    db = await get_db()
    cursor = db.execute(text(query), {"status": status})

    applications = cursor.fetchall()

    return applications
