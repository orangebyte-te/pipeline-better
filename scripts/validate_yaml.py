import os
import sys
import yaml

root = os.path.dirname(os.path.dirname(__file__))
errors = []
for cur, _, files in os.walk(root):
    for f in files:
        if f.endswith(('.yml', '.yaml')):
            path = os.path.join(cur, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    yaml.safe_load(fh)
            except Exception as e:
                errors.append((path, str(e)))

if errors:
    for path, err in errors:
        print(f'ERROR: {path} => {err}')
    sys.exit(1)
print('all yaml files parsed successfully')
