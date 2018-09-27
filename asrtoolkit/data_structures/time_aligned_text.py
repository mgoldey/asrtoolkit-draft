#!/usr/bin/env python
"""
Class for holding time_aligned text

"""

import importlib


class time_aligned_text(object):
  """
  Class for storing time-aligned text and converting between formats
  """

  def __init__(self, input_vars=None):
    """ Instantiates a time_aligned text object from either segments (if list) or a file (if string) """
    self.file_extension = None
    if input_vars is None:
      self.segments = []
    elif isinstance(input_vars, list):
      self.segments = input_vars
    elif isinstance(input_vars, str):
      self.read(input_vars)

  def __str__(self):
    """
      Returns string representation of formatted segments as corresponding
      By default, use the extension of the file you loaded
    """
    data_handler = importlib.import_module(
      ".data_handlers.{:}".format(self.file_extension if self.file_extension else 'txt'), package='asrtoolkit'
    )
    return "\n".join(_.__str__(data_handler) for _ in self.segments)

  def read(self, file_name):
    """ Read a file using class-specific read function """
    self.file_extension = file_name.split(".")[-1]
    data_handler = importlib.import_module(".data_handlers.{:}".format(self.file_extension), package='asrtoolkit')
    self.segments = data_handler.read_file(file_name)

  def write(self, file_name):
    """ Output to file using segment-specific __str__ function """
    file_extension = file_name.split(".")[-1] if '.' in file_name else 'stm'
    data_handler = importlib.import_module(".data_handlers.{:}".format(file_extension), package='asrtoolkit')
    with open(file_name, 'w', encoding="utf-8") as f:
      f.writelines("\n".join(seg.__str__(data_handler) for seg in self.segments))
