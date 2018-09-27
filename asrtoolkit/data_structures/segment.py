#!/usr/bin/env python
"""
Class for holding a segment

"""


class segment(object):
  """
  Class for holding segment-specific information
  """

  # refer to some file if possible
  audiofile = ""
  # by default, use channel 1
  channel = 1
  # need a speaker id
  speaker = "UnknownSpeaker"
  # start at beginning of file
  start = 0.0
  # this should go the length of the file or the segment
  stop = 0.0
  # Arbitrarily choose a default gender since unknown does not play well with some programs
  label = "<o,f0,male>"
  # text to be populated from read class
  text = ""

  def __init__(self, segment_dict):
    """
    Stores and initializes audiofile, channel, speaker,  start & stop times, label, and text

    >>> seg = segment({"text":"this is a test"})

    """
    self.__dict__.update(segment_dict)

  def __str__(self, data_handler=None):
    """
      Returns the string corresponding to TXT format by default
      >>> seg = segment({"text":"this is a test"})
      >>> print(seg)
      this is a test
    """
    ret_str = data_handler.format_segment(self) if data_handler else self.text

    return ret_str


if __name__ == "__main__":
  import doctest
  doctest.testmod()