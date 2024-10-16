import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="youtube-downloader",
    version="2.1.0",
    author="John Yoon",
    author_email="fedelejohn7008@gmail.com",
    description="A simple Youtube video downloading GUI application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fedele7008/YouTube-Downloader",
    license="MIT",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "youtube-downloader": [
            "resources/**/*",
            "external/**/*",
        ],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ],
    platforms="darwin, win32",
    python_requires=">=3.12",
)
