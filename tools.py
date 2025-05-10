import os, zipfile, inspect, math

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


def calculate_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle = math.atan2(delta_y, delta_x)  # Angle in radians
    angle_degrees = math.degrees(angle)  # Convert to degrees

    #correct angle to be between 0 and 360 degrees
    angle_degrees += 90
    if angle_degrees < 0:
        angle_degrees += 360
    elif angle_degrees > 360:
        angle_degrees -= 360
    return angle_degrees


def fprint(*args, **kwargs):
    frame = inspect.currentframe().f_back
    filename = os.path.basename(frame.f_globals['__file__'])
    line_number = frame.f_lineno

    line_number_str = str(line_number)
    if len(line_number_str) == 0:
        line_number_str = "000" + line_number_str
    elif len(line_number_str) == 1:
        line_number_str = "00" + line_number_str
    elif len(line_number_str) == 2:
        line_number_str = "0" + line_number_str

    print(f"[{filename}: {line_number_str}]", *args, **kwargs)
