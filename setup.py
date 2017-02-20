from setuptools import setup, find_packages

setup(
    name="jmbo-calendar",
    version="2.0.2",
    description="Jmbo calendar app.",
    long_description = open("README.rst", "r").read() + open("AUTHORS.rst", "r").read() + open("CHANGELOG.rst", "r").read(),
    author="Praekelt Foundation",
    author_email="dev@praekelt.com",
    license="BSD",
    url="http://github.com/praekelt/jmbo-calendar",
    packages = find_packages(),
    install_requires = [
        # "jmbo>=3.0.0", uncomment when released
        "django-simplemde",
    ],
    tests_require=[
        "tox",
        "psycopg2",
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
