# coding=utf-8
"""Pipes of configure."""
import os.path
import yaml
from ConfigParser import SafeConfigParser

from ..filetype import FILETYPES
from ..filetype import FileType
from ..filetype import path_to_filetype
from ..utility import read_configure


def parse_ini(confpath, section):
    """
    Parse .ini and .conf to dictionary

    Parameters
    ----------
    confpath : str
        Path to config file.
    section : str
        Specify section name in configure file.

    Returns
    -------
    Specified section as a dictionary.
    """
    conf = SafeConfigParser()
    conf.optionxform = str
    conf.read(confpath)
    return {k: v for k, v in conf.items(section)}


def parse_yaml(confpath, section):
    """
    Parse .yaml to dictionary

    Parameters
    ----------
    confpath : str
        Path to config file.
    section : str
        Specify section name in configure file.

    Returns
    -------
    Specified section as a dictionary.
    """
    with open(confpath, "r") as f:
        d = yaml.load(f)
        if section not in d:
            Warning("No such section {} in {}".format(section, confpath))
            return {}
        return d[section]


def get_parser(filetype):
    """
    Get parser corresponding to the filetype

    Parameters
    ----------
    filetype : FileType
        see enum filetype.FileType

    Returns
    -------
    function that takes 2 args, confpath and section.
    """
    # check extension in case insensitive way
    if filetype == FileType.ini:
        return parse_ini
    elif filetype == FileType.yaml:
        return parse_yaml
    else:
        return None


def add(node_list, filename, filetype=None, section="parameters"):
    """
    Add configure to node_list.

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file does not exist, add null list.

    filetype : {'ini', 'yaml'}
        Filetype of parameter files. It must be consistent with
        `filetype.Filetype`. Parameter files are recognized as this
        filetype regardless of its filename extension.

    section : str
        Specify section name in configure file.

    Returns
    -------
    list
        node_list which is a list of dict.

    Examples
    --------
    >>> add(node_list, "configure.conf") # doctest:+SKIP
    >>> # Change load section.
    >>> add(node_list, "configure.conf", "defaults") # doctest:+SKIP

    """
    NODE_KEY = "configure"
    for node in node_list:
        confpath = os.path.join(node["path"], filename)
        conf_d = {}
        if os.path.exists(confpath):
            if filetype:
                ft = FileType[filetype]
            else:
                ft = path_to_filetype(confpath)
            parser = get_parser(ft)
            if parser:
                conf_d = parser(confpath, section)
        else:
            Warning("parameter file does not exist.")
        if NODE_KEY not in node:
            node[NODE_KEY] = conf_d
        else:
            for key in conf_d:
                if key in node[NODE_KEY]:
                    Warning("overwrite configures")
            node[NODE_KEY].update(conf_d)

    return node_list


def no_section(node_list, filename, split_char="=", comment_char=["#"]):
    """
    Add configure to node_list.

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file does not exist, add null list.
    split_char : str
        Specify the deliminator char.
    comment_char : str
        Specify the comment line signal char.

    Returns
    -------
    list
        node_list which is a list of dict.

    Examples
    --------
    >>> no_section(node_list, "foo.conf") # doctest:+SKIP
    >>> # Change deliminator and comment line signal
    >>> no_section(node_list, "foo.conf", split_char=":", comment_char="!")
    ... # doctest:+SKIP

    """
    for node in node_list:
        path = node["path"]
        cfg_path = os.path.join(path, filename)
        if not os.path.exists(cfg_path):
            continue
        cfg = read_configure(cfg_path, split_char, comment_char)
        if "configure" not in node:
            node["configure"] = {}
        node["configure"].update(cfg)
    return node_list


def register(pipes_dics):
    pipes_dics["configure"] = {
        "func": add,
        "args": ["filename"],
        "kwds": [("section", {"help": "section parameters are written"}),
                 ("filetype", {"help": "filetype. If not given, determined "
                                       "automatically by the filename "
                                       "extension.",
                               "choices": FILETYPES})],
        "desc": "Read parameter file (use ConfigParser)",
    }
    pipes_dics["configure_no_section"] = {
        "func": no_section,
        "args": ["filename"],
        "kwds": ["split_char", "comment_char"],
        "desc": "Read parameter file (without section)",
    }
