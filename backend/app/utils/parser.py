from typing import Any, Dict
import json
import xmltodict

class Parser:
    """Converte texto (JSON/XML) em dict; não lê arquivo, só parseia."""
    def parse_json_text_to_dict(self, text: str) -> Dict[str, Any]:
        return json.loads(text)

    def parse_xml_text_to_dict(self, text: str) -> Dict[str, Any]:
        return xmltodict.parse(text)

    """ def parse_any(self, text: str, kind_hint: str | None = None) -> Dict[str, Any]:
        if kind_hint:
            k = kind_hint.lower()
            if "json" in k or k.endswith(".json"):
                return self.parse_json_text(text)
            if "xml" in k or k.endswith(".xml"):
                return self.parse_xml_text(text)

        # fallback: tenta JSON; se falhar, tenta XML
        try:
            return self.parse_json_text(text)
        except Exception:
            return self.parse_xml_text(text) """
