import os, zipfile

def convert_str_to_bool(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_str_to_bool(value)
    elif isinstance(data, list):
        data = [convert_str_to_bool(item) for item in data]
    elif isinstance(data, str):
        if data.lower() == "true":
            return True
        elif data.lower() == "false":
            return False
    return data

def backup_project():
    zip_path = os.path.join(os.getcwd(), f'{os.path.basename(os.getcwd())}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if not file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.getcwd())
                    zipf.write(file_path, arcname)
    return "Saved"