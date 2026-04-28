from dataclasses import dataclass
from itertools import dropwhile
import os
import gitlab

@dataclass
class Diff:
    path: str
    diff: str

def sanitize_diff_content(diff: str) -> str:
    if not diff:
        return ''
    content = ''.join(list(dropwhile(lambda x: x != '@', diff[2:]))[2:])
    return content[:5000]

def main():
    token = os.environ['GITLAB_API_TOKEN']
    base_url = os.environ.get('GITLAB_BASE_URL', 'http://gitlab.example.internal')
    gl = gitlab.Gitlab(url=base_url, private_token=token)
    project = gl.projects.get(os.environ['CI_PROJECT_PATH'])
    mr = project.mergerequests.get(os.environ['CI_MERGE_REQUEST_IID'])
    changes = mr.changes()
    diffs = [Diff(c['new_path'], sanitize_diff_content(c['diff'])) for c in changes['changes']]
    for item in diffs:
        print(f'FILE: {item.path}')
        print(item.diff)
        print('-' * 80)

if __name__ == '__main__':
    main()
