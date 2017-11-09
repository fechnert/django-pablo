# django-pablo

`django-pablo` is a pure **p**ython **a**sset **b**uilding **l**ibrary for **o**thers who want to avoid any javascript
dependencies and want to combine, minify, compile or build any of their assets with python

# Features

Commands like this will ensure you are up-to-date on the asset stuff:

```bash
# this will try to build your assets only once
python manage.py buildassets

# but this will continuously look for changed files and rebuid them
python manage.py watchassets
```

You *have* to run `python manage.py runserver` and `python manage.py watchassets` in parallel. Maybe there will be a
command in the future which runs both together

# Installation

Drop the `pablo` folder in your django project and add it to your project settings `INSTALLED_APPS` list.

```python
INSTALLED_APPS = [
    # django stuff before, also grappelli if you have it installed
    'pablo'
    # your apps after that
]
```

Soon django-pablo will be available via pip!
