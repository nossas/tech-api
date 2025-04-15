from fastapi import FastAPI


def create_application(router: any, settings: any, **kwargs):
    application = FastAPI(**kwargs)
    application.include_router(router)

    return application