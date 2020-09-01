import os
import uvicorn


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
    uvicorn.run(
        "myblog.asgi:application",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )


if __name__ == "__main__":
    main()
# gunicorn example:app -w 4 -k uvicorn.workers.UvicornWorker
# gunicorn myblog.asgi:application -w 4 -k uvicorn.workers.UvicornWorker
# gunicorn -w 4 -k uvicorn.workers.UvicornH11Worker