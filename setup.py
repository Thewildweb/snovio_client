from distutils.core import setup

setup(
    name="snovio_client",
    version="0.01",
    description="Client to get emails for domains with Snovio",
    author="Erik Meijer",
    author_email="erik@datadepartment.io",
    url="https://www.datadepartment.io",
    py_modules=["snovio_client"],
    install_requires=["requests", "pydantic"],
)
