import importlib
import sys
import types
from pathlib import Path

import httpx


def remote_module_loader(url: str):
    resp = httpx.get(url)
    url = resp.url
    name = Path(url.path).name
    mod = sys.modules.setdefault(name, types.ModuleType(name))
    code = compile(resp.text, name, "exec")
    mod.__file__ = str(url)
    exec(code, mod.__dict__)
    return mod


if __name__ == "__main__":
    print(remote_module_loader("http://127.0.0.1:9998/code.py"))
    # <module 'code.py' from 'http://127.0.0.1:9998/code.py'>
