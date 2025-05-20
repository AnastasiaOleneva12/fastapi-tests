import os

structure = {
    'project_root': [
        'requirements.txt',
        'pytest.ini',
        '.gitignore'
    ],
    'project_root/src': [
        '__init__.py',
        'main.py',
        'models.py',
        'schemas.py'
    ],
    'project_root/tests': [
        '__init__.py'
    ],
    'project_root/tests/unit': [
        'test_models.py'
    ],
    'project_root/tests/functional': [
        'test_api.py'
    ],
    'project_root/tests': [
        'locustfile.py'
    ]
}

for folder, files in structure.items():
    os.makedirs(folder, exist_ok=True)
    for file in files:
        open(os.path.join(folder, file), 'w').close()