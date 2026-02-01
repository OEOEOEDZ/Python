"""
Setup configuration for Algorithmic Trading Simulator
Author: Yacine Abdi
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="algorithmic-trading-simulator",
    version="1.0.0",
    author="Yacine Abdi",
    author_email="",
    description="A sophisticated algorithmic trading simulator with backtesting capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/algorithmic-trading-simulator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.1.4",
        "numpy>=1.26.2",
        "yfinance>=0.2.33",
        "matplotlib>=3.8.2",
        "plotly>=5.18.0",
        "streamlit>=1.29.0",
        "pytest>=7.4.3",
        "scipy>=1.11.4",
        "seaborn>=0.13.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.12.1",
            "flake8>=7.0.0",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "trading-sim=main:main",
        ],
    },
)
