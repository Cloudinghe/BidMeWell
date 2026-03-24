#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Precision Bidding - Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bidmewell",
    version="0.3.0",
    author="BidMeWell Project",
    description="现代精确叫牌练习系统 - Bridge Precision Bidding Practice System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/BidMeWell",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Games/Entertainment :: Board Games",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies required
        # redeal is bundled with practice_bidding
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "color": [
            "colorama>=0.4.6",
        ],
    },
    entry_points={
        "console_scripts": [
            "bidmewell=scripts.run_practice:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.xml", "*.xlsx", "*.docx"],
    },
    zip_safe=False,
)
