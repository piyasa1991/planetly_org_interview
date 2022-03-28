import fastapi
import fastapi.middleware.cors
import fastapi.exceptions
import fastapi.encoders
import fastapi.responses
import pydantic
import interview_app.api
import interview_app.models as models
import interview_app.db.session as db

import interview_app.core.deps as deps
import sqlalchemy
import logging

logger = logging.getLogger(__name__)

app = fastapi.FastAPI(title="Global Temperatures by city")
origins = [
    "*",
]

# Set all CORS enabled origins
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview_app.api.router, prefix="/cities")


# @app.on_event("startup")
# def startup_event():
#     pass
# models.Base.metadata.create_all(bind=db.engine)
