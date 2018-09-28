#!/usr/bin/env python
"""
Utility for sanitizing file names to remove hyphens
"""


def sanitize_hyphens(file_name):
  """
    Replace hyphens with underscores if present in file name
  """
  if "-" in file_name.split("/")[-1]:
    print(
      "Replacing hyphens with underscores in SPH file output- check to make sure your audio files and transcript files match"
    )
    file_name = "/".join(file_name.split("/")[:-1]) + file_name.split("/")[-1].replace("-", "_")
  return file_name
