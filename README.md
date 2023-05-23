# Env-Freeze 

### Abstract
In a perfect world, we should never need this package. However, when dealing with some legacy applications, it is possible for builds to start failing due to underlying dependencies being changed. While the right course of action would be to updated the Python version and all packages, this can be a real headache for old poorly written applications. So, the idea here is to clone/port/move a Python virtual env so that reinstalling packages is not needed. Just installing the same packages with the same versions does not result in an 1 to 1 copy due to the fact the the versioning of dependency packages can change at any given time.
Example (piptree):
```bash
    autoflake 2.1.1
    └── pyflakes
    └── tomli
    black 23.3.0
    └── click
    └── mypy-extensions
    └── packaging
    └── pathspec
    └── platformdirs
    └── tomli
```
    While we can lock version of packages installed directly via pip, the versions of the dependencies of these packages are subject to change.
    
    
