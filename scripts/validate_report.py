from pathlib import Path
import json
import urllib.request
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)
from jsonschema import Draft7Validator, RefResolver

cache = {}
def remote(uri):
    uri = uri.replace('schema.embedded.json', 'schema-embedded.json')
    if uri not in cache:
        with urllib.request.urlopen(uri, timeout=30) as response:
            cache[uri] = json.load(response)
            cache[uri]['$id'] = uri
    return cache[uri]

root = Path(__file__).resolve().parents[1] / 'RetailRevenue.Report'
count = 0
for path in root.rglob('*.json'):
    if '.pbi' in path.parts:
        continue
    obj = json.loads(path.read_text(encoding='utf-8'))
    uri = obj.get('$schema')
    if not uri: continue
    schema = remote(uri)
    resolver = RefResolver(uri,schema,handlers={'https':remote})
    errors = list(Draft7Validator(schema,resolver=resolver).iter_errors(obj))
    if errors:
        for error in errors[:5]: print(path, list(error.absolute_path), error.message)
        raise SystemExit(1)
    count+=1
print(f'{count} PBIR JSON files validated against Microsoft schemas')
