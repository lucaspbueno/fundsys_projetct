from typing import List, Union

def convert_to_list(node: Union[dict, list, None]) -> List[dict]:
    """Garante que o nó possa ser iterado como lista."""
    if node is None:
        return []
    if isinstance(node, list):
        return node
    if isinstance(node, dict):
        return [node]
    return []
