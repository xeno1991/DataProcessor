from .scan import directory
from .configure import add
from ..filetype import FILETYPES


def scan_configure(node_list, root, whitelist, followlinks=False,
                   filetype=None, section="parameters"):
    """Scan then configure.

    see pipes.scan.directory and pipes.configure.add.

    Parameters
    ----------
    root : str
        Scan directories recursively under the directory `root`.
    whitelist : list of str or str
        Run node has one or more file or directory
        which satisfies run_node_dir/`whitelist`.
        And project nodes satisfy project_dir/run_node_dir/`whitelist`.
        str can be specified by wildcard.
    followlinks : {'False', 'True'}, optional
        Whether scan in symbolic link.
        Be aware that setting this to True may lead to infinite recursion.
    filetype : {'ini', 'yaml'}, optional
        see pipes.configure.add
    section : str
        Specify section name in configure file.

    Returns
    -------
    list
        node_list which is a list of dict.
    """
    if isinstance(whitelist, str):
        whitelist = [whitelist]
    node_list = directory(node_list, root, whitelist, followlinks)
    for filename in whitelist:
        node_list = add(node_list, filename, filetype, section)
    return node_list


def register(pipe_dics):
    pipe_dics["scan_configure"] = {
        "func": scan_configure,
        "args": [("root", {"help": "path of root directory"}),
                 ("whitelist",
                  {"help": "list of filenames (e.g. parameter.ini)",
                   "nargs": "+", }),
                 ],
        "kwds": [("followlinks", {"help": "whether scan in symbolic link"}),
                 ("section", {"help": "section parameters are written"}),
                 ("filetype", {"help": "filetype. If not given, determined "
                                       "automatically by the filename "
                                       "extension.",
                  "choices": FILETYPES})],
        "desc": "Scan nodes from all directories under the directory 'root'.",
    }
