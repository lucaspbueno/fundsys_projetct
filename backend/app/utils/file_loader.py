from fastapi import UploadFile

class FileLoader:
    """Lê conteúdo de UploadFile (upload direto, sem salvar em disco)."""
    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding

    async def load_text(self, upload: UploadFile) -> str:
        """Lê o conteúdo de um UploadFile e retorna como string"""
        data = await upload.read()
        return data.decode(self.encoding)

    async def load_bytes(self, upload: UploadFile) -> bytes:
        """Lê o conteúdo de um UploadFile e retorna como bytes"""
        return await upload.read()
