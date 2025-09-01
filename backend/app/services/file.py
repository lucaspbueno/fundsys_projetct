# app/services/xml_service.py
from typing import Dict, Any, List
from xml.etree import ElementTree as ET

class XmlService:
    ALLOWED_TYPES = {"application/xml", "text/xml"}

    def _analyze_single(self, xml_bytes: bytes) -> Dict[str, Any]:
        """
        Lê o XML e retorna um resumo simples:
        - root_tag: nome da tag raiz do XML
        - titprivado_count: quantos nós <titprivado> existem (comum em posições ANBIMA)
        """
        root = ET.fromstring(xml_bytes)  # lança ParseError se inválido
        titprivado_count = len(root.findall(".//titprivado"))
        return {"root_tag": root.tag, "titprivado_count": titprivado_count}

    async def analyze_many(
        self,
        files: List,  # List[UploadFile], mas deixamos genérico para facilitar testes
    ) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []
        for f in files:
            # Validação leve de content-type (não é segurança forte; é só UX)
            if getattr(f, "content_type", None) not in self.ALLOWED_TYPES:
                results.append({
                    "filename": getattr(f, "filename", None),
                    "ok": False,
                    "error": f"Tipo não suportado: {getattr(f, 'content_type', None)}. Envie XML."
                })
                continue

            try:
                data = await f.read()  # carrega na memória; depois podemos trocar por streaming
                info = self._analyze_single(data)
                results.append({
                    "filename": getattr(f, "filename", None),
                    "size_bytes": len(data),
                    "ok": True,
                    **info
                })
            except Exception as e:
                results.append({
                    "filename": getattr(f, "filename", None),
                    "ok": False,
                    "error": str(e)
                })

        return {
            "received": len(files),
            "processed": sum(1 for r in results if r["ok"]),
            "results": results,
        }
