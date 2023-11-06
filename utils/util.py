def create_configuration_fastapi(app,ErrorHandler):
    # Changes to the docs
    app.title = "Mi aplicación con  FastAPI"
    app.version = "0.0.1"
    app.add_middleware(ErrorHandler)
