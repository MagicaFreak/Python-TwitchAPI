import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitch-MagicaFreak",
    version="1.0.0",
    author="MagicaFreak",
    author_email="magicafreak97@gmail.com",
    description="A Twitch Wrapper for Python 3.6 or higher for the new Twitch API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MagicaFreak/Python-TwitchAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["aiohhttp"],
    python_requires='>=3.6',
)
