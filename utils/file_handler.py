import tempfile
import os

def create_version_directory():
    temp_dir = tempfile.mkdtemp(prefix='webdesign_versions_')
    return temp_dir

def save_design_version(content, version, base_dir):
    file_name = f'version_{version}.html'
    file_path = os.path.join(base_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path