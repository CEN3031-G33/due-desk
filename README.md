# Due Desk

## Overview

The virtual space that helps you get assignments done in a fun and rewarding way.

## Using

1. Grab the latest release file. Download it to your local machine.

2. Decompress the tarball (.tar.gz) and open the terminal at the new folder.

3. Install DueDesk through pip.

```
$ pip install .
```

4. Verify DueDesk installed properly.

```
$ duedesk
```

## Contributing

1. Clone this repository to your local machine.

```
$ git clone https://github.com/CEN3031-G33/due-desk.git 
```

2. Build the development version.

```
$ pip install -e ./due-desk
```

3. Run unit tests locally.

```
$ python -m unittest discover due_desk -v -p "*.py"
```

4. Run integration tests locally.

```
$ python -m unittest discover tests -v -p "main.py"
```

5. Check out a new branch to write code.

```
$ git checkout -b <name>
```