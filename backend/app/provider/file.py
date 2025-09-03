from app.utils import FileLoader

def get_file_loader() -> FileLoader:
    return FileLoader(encoding="utf-8")
