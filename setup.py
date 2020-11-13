from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="cumulus_clone",
    version="0.1.0",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    license="3-Clause BSD",
    author="",
    author_email="",
    keywords="",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django :: 3.0",
        "Framework :: Django",
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[
        # Base
        "pytz",
        "python-slugify",
        "Pillow",
        "argon2-cffi",
        "redis",
        "hiredis",
        "fabric",
        "xkcdpass",
        "celery",
        "channels",
        "django",
        "django-environ",
        "django-model-utils",
        "django-allauth",
        "django-crispy-forms",
        "django-redis",
        "djangorestframework",
        "django-guardian",
        "django_extensions",
        "drf-yasg",
        # Production
        "gunicorn",
        "psycopg2",
        "Collectfast",
        # Local
        "Werkzeug",
        "ipdb",
        "psycopg2-binary",
        "mypy",
        "django-stubs",
        "pytest",
        "pytest-sugar",
        "sphinx",
        "sphinx-autobuild",
        "flake8",
        "flake8-isort",
        "coverage",
        "black",
        "pylint-django",
        "pre-commit",
        "factory-boy",
        "django-debug-toolbar",
        "django-coverage-plugin",
        "pytest-django"
    ],
)