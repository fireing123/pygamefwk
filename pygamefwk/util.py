import json5
from pygamefwk.error import JsonSerializableError
from pygamefwk.error import ImmutableAttributeError

class const(property):
    def settar(self, value):
        raise ImmutableAttributeError("이 속성은 불변입니다 값을 할당하려 하지 마십시오")

class getter(property):
    def settar(self, value):
        raise ImmutableAttributeError("이 속성은 할당할수없습니다 값을 할당하려 하지 마십시오")

def string_insert(string: str, insert_string: str, index: int):
    if len(string) < index or index < 0:
        raise ValueError(f"index 가 문자열에 유효한 위치가 아닙니다 string len: {len(string)} index: {index}")
    return f"{string[:index]}{insert_string}{string[index:]}"

def string_cut(string: str, range: tuple[int, int]):
    if range[0] > range[1]:
        raise ValueError("범위에 끝은 처음보다 크거나 같아야합니다")
    return f"{string[:range[0]]}{string[range[1]:]}"

def jsopen(path: str) -> dict:
    with open(path, 'r') as f:
        json = json5.loads(f.read())
    return json

def is_numeric_array(arr):
    return isinstance(arr, list) and all(isinstance(item, (int, float)) or item is None for item in arr)

def custom_stringify(obj, indent=4, level=0):
    pad = ' ' * (indent * level)

    if isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            item_str = f'{pad}{" " * indent}"{key}": {custom_stringify(value, indent, level + 1)}'
            items.append(item_str)
        return '{\n' + ',\n'.join(items) + f'\n{pad}}}'

    elif isinstance(obj, list):
        if is_numeric_array(obj):
            return '[' + ', '.join('null' if x is None else str(x) for x in obj) + ']'
        else:
            items = [custom_stringify(item, indent, level + 1) for item in obj]
            return '[\n' + ',\n'.join(f'{" " * (indent * (level + 1))}{item}' for item in items) + f'\n{pad}]'

    elif isinstance(obj, str):
        return json5.dumps(obj)

    elif obj is None:
        return 'null'

    else:
        return str(obj)

def jsave(data: dict, path: str):
    with open(path, 'w') as f:
        f.write(custom_stringify(data))

def replaced_jgetter(data):
    if isinstance(data, dict):
        return {key: replaced_jgetter(value) for key, value in data.items()}

    elif isinstance(data, list):
        return [replaced_jgetter(item) for item in data]

    elif isinstance(data, str):
        if data.startswith("gamefs://"):
            path = data.replace("gamefs:/", ".")
            return replaced_jgetter(jsopen(path))
        return data

    else:
        return data

types = (str, int, float, list, bool)

def check_json_serializable(dic: dict):
    for value in list(dic.values()):
        if isinstance(value, types):
            pass
        elif isinstance(value, dict):
            check_json_serializable(value)
        else:
            raise JsonSerializableError(f"{type(value)} 타입은 json 에 저장할수 있는 타입이 아닙니다")

