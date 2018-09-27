#!/usr/bin/env python
"""
Class for holding a segment

"""


class segment(object):
  """
  Class for holding segment-specific information
  """
  data = {
    'audiofile': "",  # refer to some file if possible
    'channel': 1,  # by default, use channel 1
    'speaker': "UnknownSpeaker",  # need a speaker id
    'start': 0.0,  # start at beginning of file
    'stop': 0.0,  # this should go the length of the file or the segment
    'gender': "male",  # Arbitrarily choose a default gender since unknown does not play well with some programs
    'label': "",
    'text': ""  # text to be populated from read class
  }

  def __init__(self, segment_dict):
    """
    Stores and initializes audiofile, channel, speaker,  start & stop times, label, and text

    >>> seg = segment({"text":"this is a test"})

    """
    self.data = segment_dict

  def __str__(self, data_handler=None):
    """
      Returns the string corresponding to TXT format by default
      >>> seg = segment({"text":"this is a test"})
      >>> print(seg)
      this is a test
    """
    ret_str = ""

    if data_handler is not None:
      ret_str = data_handler.format_segment(self)
    else:
      ret_str = self.data['text']

    return ret_str


if __name__ == "__main__":
  import doctest
  doctest.testmod()