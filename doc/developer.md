dataprocessor library
=====================


Internal Data Structure
-----------------------
This library handle list of dictionary(**node**).
Here, we call the list **node_list**.

The **node** is a dictionary, which at least have following keys.

  + **path**  
      ID of this **node** and this **node** belong to its **path**.
  + **name**  
      Name of this **node**.
  + **parents**  
      Path list of upper level **node**.
  + **children**  
      Path list of lower level **node**.
  + **type**  
      Specify **node** type. Now, **run**, **project** and **figure** are supported.

Of course, additional keys are allowed.
This library add/delete some **node** to **node_list**,
add/delete some keys and values to each node.


Prepare development environment
------------------------------------
Please install `virtualenv` and `pip`.
On the top directory of this project, create virtual enveronment of development
and install the required libraries to the environment,

    $ virtualenv env && env/bin/pip install -r requirements.txt

If you want to specify python version,

    $ virtualenv env -p /usr/bin/python2.7 && env/bin/pip install -r requirements.txt

Please change the appropriate python path.

Enter the virtual environment,

    $ source env/bin/activate

Exit the environment.

    $ deactivate

TEST
----
You can run the test of this library by following command.

```sh
nosetests -v --with-doctest
```

API reference
-------------
You can read API reference at <http://kenbeese.github.io/DataProcessor>.


### build

After preparation of the above development environment,
you can update api reference of this library with following command.

    $ make -C doc gh-pages-clone
    $ make -C doc gh-pages-all


server API reference
====================

manip
-----

Do a manipulation on server.
(you should use POST)

### address
`/cgi-bin/api.cgi`

### Request

```
"type" : "manip"
"manip" : json_str
```

### Response
JSON will be returned.

If the manipulation succeed:

```json
{
    "exit_code" : 0
}
```

If the manipulation fails:

```json
{
    "exit_code" : exit_code,
    "message" : error_message
}
```

See also `handler.operation_sucess` and `handler.operation_fail`.

pipe
----

Do a manipulation s.t. [load, pipe, save].

### address
`/cgi-bin/api.cgi`

### Request

```
"type" : "pipe"
"name" : "name_of_pipe"
"args" : args_json  # JSON string of list
"kwds" : kwds_json  # JSON string of dictionary, optional
```

This will create a manipulation s.t.

```json
[
    {"name": "load_json", "args", ["data.json"]},
    {"name": "name_of_pipe", "args": json.loads(args_json), "kwds": json.loads(kwds_json)},
    {"name": "save_json", "args", ["data.json"], "kwds" : {"silent" : "True"}},
]
```

### Response
JSON will be returned (same as `manip`).

Projects
--------

Get a project list

### address
`/cgi-bin/body.cgi`

### Request

```
"type" : "Projects"
```

### Response
JSON will be returned.

```json
{
    "keys" : ["name", "comment", "tags", "path"]
    "table" : [
        {
            "path" : "path_of_project",
            "name" : "name_of_project",
            "tags" : ["tags",],
            "comment" : "comment_of_project"
        }, {
            "path" : "path_of_project",
            "name" : "name_of_project",
            "tags" : ["tags",],
            "comment" : "comment_of_project"
        }, ...
    ]
}
```

`table` contains a list of dictionaries
in which the properties of projects are described.

Widgets
-------

Get HTML parts

### address
`/cgi-bin/body.cgi`

### Request

```
"type" : "Widgets"
"path" : "path_of_node"
"table_type" : "children" or "parents"
```

If you want to generate a table in which the configures of children,
you should set `table_type` to be `children`.
See also `lib/dataprocessor/table.py`.

### Response

JSON will be returned.

In this version, only table widget is implemented.

```json
[
    "<table class='[table_type]TableWidget'>
        <thead>
        <tr>...</tr>
        </thead>
        <tbody>
        <tr>...</tr>
        ...
        </tbody>
    </table>",
]
```

In the future version, another type of widgets
such that figure widget will be implemented.
Then it will becomes as follows.

```json
[
    "<table class='[table_type]TableWidget'>
        <thead>
        <tr>...</tr>
        </thead>
        <tbody>
        <tr>...</tr>
        ...
        </tbody>
    </table>",
    "<div class='FigureWidget'>
        <img ... />
        ...
    </div>"
]
```
