from setuptools import setup, find_packages


def read_version(module_name):
    from re import match, S
    from os.path import join, dirname

    f = open(join(dirname(__file__), module_name, "__init__.py"))
    return match(r".*__version__ = (\"|')(.*?)('|\")", f.read(), S).group(2)


setup(
    name="otpx",
    version=read_version("otpx"),
    description="Simple OTP Client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/meyt/otpx",
    author="MeyT",
    install_requires=[
        "pyotp >= 2.6.0",
        "pyperclip >= 1.8.2",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["otpx = otpx.cli:main"]},
    license="MIT",
    keywords="cli 2fa otp totp hotp",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
        "Topic :: Utilities",
        "Environment :: Console :: Curses",
        "Environment :: Console",
    ],
)
