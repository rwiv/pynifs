import urllib3


def disable_warning_log():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def to_dir_path(path: str):
    result = path.lstrip("/")
    if result == "":
        return ""
    if result[-1] == "/":
        return result
    else:
        return result + "/"
