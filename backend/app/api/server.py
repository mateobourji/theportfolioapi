from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core import config, tasks
from app.api.routes import router as api_router
from app.services.logger import logger
import logging
import json


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION, description=config.DESCRIPTION,
                  redoc_url=config.DOCS_URL, openapi_tags=config.TAGS_META)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))
    app.include_router(api_router, prefix="/api")
    return app


logger.setup_logging()
endpoint_logger = logging.getLogger("ENDPOINT")

app = get_application()


@app.middleware("http")
async def log_request_and_response(request: Request, call_next):
    client = request.client.host
    endpoint_logger.log(level=logging.INFO,
                        msg="REQUEST - Client: %s - Body: %s" % (client, request.query_params))
    response = await call_next(request)

    resp_body = [section async for section in response.__dict__['body_iterator']]
    # Repairing FastAPI response
    response.__setattr__('body_iterator', async_iterator_wrapper(resp_body))

    try:
        resp_body = json.loads(resp_body[0].decode())

    except:
        resp_body = str(resp_body)

    endpoint_logger.log(level=logging.INFO,
                        msg="RESPONSE - Client: %s - Body: %s" % (client, resp_body))

    return response


class async_iterator_wrapper:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
