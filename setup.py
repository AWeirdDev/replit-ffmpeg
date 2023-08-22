from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
  name="replit-ffmpeg",
  author="AWeirdDev",
  version="0.1",
  license="MIT License",
  description="Installs FFmpeg for you on Replit.",
  long_description=readme,
  long_description_content_type="text/markdown",
  author_email="aweirdscratcher@gmail.com",
  packages=['replit_ffmpeg'],
  classifiers=[
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Environment :: Console",
  ],
  keywords=["replit", "ffmpeg", "opus", "youtube-dl"],
  entry_points={
    "console_scripts": [
      "replit-ffmpeg=replit_ffmpeg.installer:main"
    ]
  }
)
