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
Currently, the package is under development and is not yet available on [PyPI]. It can only be used by means of cloning
the repository applying these stubs to path manually.

Use this command to clone the repository:
```commandline
git clone "https://github.com/L0RD-ZER0/Motor-Types"
```

Afterwards, you can do either of the following to use stubs:
* Copy the stubs manually to either `libs/site-packages/motor` or `libs/site-packages/motor-stubs`
* Add these stubs manually to project directories.
  * [For MyPy][MyPy-Stubs].
  * [For PyCharm][PyCharm-Stubs].
  * For other static type-checking tools, consider referring to their corresponding documentation regarding stubs.

Dependencies
------------
This package uses following dependencies:
* [Poetry] (For Packaging and Publishing)
* [PyMongo] (For PyMongo related types)
* [Motor] (For Referencing and as an installation shorthand)
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
[License]: ./LICENSE