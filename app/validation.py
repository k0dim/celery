import os
from werkzeug.datastructures import FileStorage

from mapping import ApiError

EXTENSION = [".png", ".jpg"]

def validation(filename_ext: FileStorage | None):
    if filename_ext:
        filename, file_extension = os.path.splitext(str(filename_ext.filename))
    else:
        raise ApiError(404, f"File not received")
    if file_extension in EXTENSION:
        return filename_ext
    else:
        raise ApiError(404, f"Invalid file extension, the application only supports the following file extensions: {EXTENSION}")
    

def rename_file(filename_ext: str):
    filename, file_extension = os.path.splitext(filename_ext)
    return os.rename(filename_ext, filename+'_upscale'+file_extension)