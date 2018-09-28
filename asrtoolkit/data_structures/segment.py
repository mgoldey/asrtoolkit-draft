#!/usr/bin/env python
"""
Class for holding a segment

"""


def std_float(number, num_decimals=2):
  """
    Print a number to string with n digits after the decimal point (default = 2)
  """
  return "{0:.{1:}f}".format(float(number), num_decimals)


def timestampToSeconds(timestamp):
  """
    Convert a timestamp to seconds
  """
  parts = timestamp.split(":")
  return std_float(float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2]), 3)


def secondsToTimestamp(seconds):
  """
    Convert from seconds to a timestamp
  """
  minutes, secondss = divmod(float(seconds), 60)
  hours, minutes = divmod(minutes, 60)
  return "%02d:%02d:%06.3f" % (hours, minutes, seconds)


def clean_float(input_float):
  """
    Return float in seconds (even if it was a timestamp originally)
  """
  return timestampToSeconds(input_float) if ":" in input_float else std_float(input_float)


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

  def __init__(self, input_dict=None):
    """
    Stores and initializes audiofile, channel, speaker,  start & stop times, label, and text

    >>> seg = segment({"text":"this is a test"})

    """
    self.__dict__.update(input_dict if input_dict else {})

  def __str__(self, data_handler=None):
    """
      Returns the string corresponding to TXT format by default
      >>> seg = segment({"text":"this is a test"})
      >>> print(seg)
      this is a test
    """
    ret_str = data_handler.format_segment(self) if data_handler else self.text

    return ret_str

  def validate(self):
    """
      Checks for common failure cases for if a line is valid or not
    """
    valid = self.speaker != "inter_segment_gap" and \
      self.text and \
      self.text != "ignore_time_segment_in_scoring" and \
      self.label in ["<o,f0,male>", "<o,f0,female>"]

    try:
      self.start = clean_float(self.start)
      self.stop = clean_float(self.stop)
    except Exception as exc:
      valid = False
      print(exc)

    if not valid:
      print("Skipping segment due to validation error: \n", " ".join(self.__dict__[_] for _ in self.__dict__))

    if "-" in self.audiofile:
      self.audiofile = self.audiofile.replace("-", "_")
      print("Please rename audio file to replace hyphens with underscores")

    return valid


if __name__ == "__main__":
  import doctest
  doctest.testmod()