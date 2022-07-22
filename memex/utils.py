import importlib.util
import sys

def parse_token(request):
    return request.headers.get('memex-token', '')

# In format /foo/bar/file.py
def load_module(path):
    spec = importlib.util.spec_from_file_location("module", path)
    foo = importlib.util.module_from_spec(spec)
    sys.modules["module"] = foo
    spec.loader.exec_module(foo)
    if not foo.main:
        raise Exception(f"Cannot find function 'main' in '{path}'")
    return foo.main