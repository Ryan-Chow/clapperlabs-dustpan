"""
Setup script for CapCut CLI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="capcut-cli",
    version="1.0.0",
    description="AI-powered command-line interface for CapCut video editing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/capcut-cli",
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    install_requires=[
        "click>=8.0.0",
        "anthropic>=0.21.0",
        "requests>=2.31.0",
        "opencv-python>=4.8.0",
        "ffmpeg-python>=0.2.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.66.0",
        "colorama>=0.4.6",
        "rich>=13.0.0"
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0"
        ]
    },
    
    entry_points={
        "console_scripts": [
            "capcut-cli=cli:cli",
            "ccli=cli:cli"  # Short alias
        ]
    },
    
    python_requires=">=3.8",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Content Creators",
        "Topic :: Multimedia :: Video :: Non-Linear Editor",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    
    keywords="capcut video editing ai cli automation",
    
    project_urls={
        "Bug Reports": "https://github.com/yourusername/capcut-cli/issues",
        "Source": "https://github.com/yourusername/capcut-cli",
        "Documentation": "https://github.com/yourusername/capcut-cli#readme"
    },
    
    include_package_data=True,
    package_data={
        "": ["config/*.json", "templates/*.json", "assets/music/*"]
    }
)