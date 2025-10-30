#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
    name="novashield",
    version="1.0.0",
    author="NovaShield Contributors",
    description="Next-generation CIS compliance analytics platform",
    packages=find_packages(include=["backend", "backend.*"]),
    py_modules=["cis_audit"],
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.111.0",
        "uvicorn[standard]>=0.30.0",
        "pydantic>=2.7.0",
    ],
    extras_require={
        "dev": ["pytest>=8.2.0", "httpx>=0.27.0", "pytest-asyncio>=0.23.0"],
    },
)
