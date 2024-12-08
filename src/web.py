from fastapi import FastAPI


def init_app():
    app = FastAPI(docs_url="/api/v1/docs", debug=True)
    return app
