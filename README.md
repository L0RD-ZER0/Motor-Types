Motor-Types
===========
Python stubs for [Motor], a Non-Blocking [MongoDB] driver for [Python]'s [Tornado] and [AsyncIO] based applications.

About
------
Stubs for [Motor] (version 3.0.0+) for substituting the missing type-hints. These stubs are meant to be used along with
pycharm and mypy to facilitate static type-checking. Installing this package adds these `.pyi` files to
`libs/site-packages/motor`. Currently, only the stubs for [AsyncIO] are supported. You can contribute to stubs for
[Tornado] by opening a pull request for the same.

**Note:** This project is currently under development and is in no way affiliated with MongoDB. This is an unofficial
stub package.

How to use?
-----------

You can either install from [PyPI] using [pip] or add files to your project directories manually.

### Installing Using [pip]:
```commandline
pip install motor-types
```

### To install [Motor] (and [Dnspython]) alongside the package:
```commandline
pip install motor-types[motor]
```

### To add files to the project manually:
Use this command to clone the repository:
```commandline
git clone "https://github.com/L0RD-ZER0/Motor-Types"
```

Afterwards, you can do either of the following to use stubs:
* Copy the stubs manually to either ``libs/site-packages/motor`` or ``libs/site-packages/motor-stubs``, ideally the latter.
* Add these stubs manually to project directories.
  * [For MyPy][MyPy-Stubs].
  * [For PyCharm][PyCharm-Stubs].
  * For other static type-checking tools, consider referring to their corresponding documentation regarding stubs.

Examples:
---------
### Auto-Complete Example
**Without Stubs:**

![ACNS]

**With Stubs:**

![ACWS]

### Type-Checking Example
**Without Stubs:**

![TCNS]

**With Stubs:**

![TCWS]

Dependencies
------------
This package uses following dependencies:
* [Poetry] (For Packaging and Publishing)
* [PyMongo] (For PyMongo related types)
* [Motor] (For Referencing and for motor installation extra)
* [Dnspython] (For motor installation extra)
* [Pre-Commit] (For maintaining code quality)
* [Typing-Extensions] (For using the latest typing features)

How to Contribute?
------------------
The simplest contribution you can make is by opening a [GitHub Issue][GH-Issues] or by forking the repository and making
a pull request on the [GitHub Repository][GH-Repo] for the same. The changes can be as simple as improving the
documentation or as big as completing any incomplete section of the typings.

**Note:** All issues and pull-requests are subjected to a preliminary inspection.

License
-------
This repository is licensed under MIT License. The [license][License] can be found within the repository.


[Motor]: https://github.com/mongodb/motor
[MongoDB]: https://www.mongodb.com
[PyMongo]: https://github.com/mongodb/mongo-python-driver
[Poetry]: https://github.com/python-poetry/poetry
[pip]: https://pypi.org/project/pip/
[Dnspython]: https://www.dnspython.org/
[Pre-Commit]: https://pre-commit.com
[Typing-Extensions]: https://github.com/python/typing_extensions
[Python]: https://python.org
[Tornado]: https://www.tornadoweb.org/
[Asyncio]: https://docs.python.org/3/library/asyncio.html
[PyPI]: https://pypi.org/
[MyPy-Stubs]: https://mypy.readthedocs.io/en/stable/stubs.html#stub-files
[PyCharm-Stubs]: https://www.jetbrains.com/help/pycharm/stubs.html
[GH-Repo]: https://github.com/L0RD-ZER0/Motor-Types
[GH-Issues]: https://github.com/L0RD-ZER0/Motor-Types/issues
[License]: https://github.com/L0RD-ZER0/Motor-Types/blob/master/LICENSE
[ACNS]: https://github.com/L0RD-ZER0/Motor-Types/raw/master/examples/auto-complete-example-ns.png
[ACWS]: https://github.com/L0RD-ZER0/Motor-Types/raw/master/examples/auto-complete-example-ws.png
[TCNS]: https://github.com/L0RD-ZER0/Motor-Types/raw/master/examples/type-checking-example-ns.png
[TCWS]: https://github.com/L0RD-ZER0/Motor-Types/raw/master/examples/type-checking-example-ws.png