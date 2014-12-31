import enum
import os


FileType = enum.Enum("FileType", "NONE ini conf yaml json")


def str_to_filetype(filetype):
    """
    Get filetype from str.

    Parameters
    ----------
    filetype: str
        filetype as string

    Returns
    -------
    FileType enum. If unknown filetype is given, throw warning.
    """
    try:
        return FileType[filetype]
    except KeyError:
        # TODO update warning (#169)
        Warning("Unknown filetype " + filetype)
        return FileType.NONE


def path_to_filetype(path):
    """
    Get filetype from path (filename extension).

    Parameters
    ----------
    path: str
        path to a file

    Returns
    -------
    FileType enum. If unknown filename extension is given, throw warning
    """
    _, ext = os.path.splitext(path)

    # check extension in case insensitive way
    ext = ext.lower()
    if ext in (".ini", ".conf"):
        return FileType.ini
    elif ext in (".yml", ".yaml"):
        return FileType.yaml
    else:
        # TODO update warning (#169)
        Warning("Unknown filename extension " + ext)
        return FileType.NONE
