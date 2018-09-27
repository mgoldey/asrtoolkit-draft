#!/usr/bin/env python
"""
Class for holding time_aligned text

"""

import importlib


class time_aligned_text(object):
  """
  Class for storing time-aligned text and converting between formats
  """

  segments = []

  def __init__(self, input_var=None):
    """
    Instantiates a time_aligned text object from a file (if input_var is a string)

    >>> transcript = time_aligned_text()
    """
    self.file_extension = None
    if isinstance(input_var, str):
      self.read(input_var)

  def __str__(self):
    """
      Returns string representation of formatted segments as corresponding
      By default, use the extension of the file you loaded
    >>> transcript = time_aligned_text()
    >>> print(transcript.__str__()=="")
    True
    """
    data_handler = importlib.import_module(
      "asrtoolkit.data_handlers.{:}".format(self.file_extension if self.file_extension else 'txt')
    )
    return "\n".join(_.__str__(data_handler) for _ in self.segments)

  def read(self, file_name):
    """ Read a file using class-specific read function """
    self.file_extension = file_name.split(".")[-1]
    data_handler = importlib.import_module("asrtoolkit.data_handlers.{:}".format(self.file_extension))
    self.segments = data_handler.read_file(file_name)

  def write(self, file_name):
    """ Output to file using segment-specific __str__ function """
    file_extension = file_name.split(".")[-1] if '.' in file_name else 'stm'
    data_handler = importlib.import_module("asrtoolkit.data_handlers.{:}".format(file_extension))
    with open(file_name, 'w', encoding="utf-8") as f:
      f.writelines("\n".join(seg.__str__(data_handler) for seg in self.segments))


if __name__ == "__main__":
  import doctest
  doctest.testmod()