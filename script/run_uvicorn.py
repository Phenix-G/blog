import os
import uvicorn


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
    uvicorn.run(
        "myblog.asgi:application",
        host="localhost",
        port=8000,
        log_level="debug",
        reload=True,
    )


if __name__ == "__main__":
    main()