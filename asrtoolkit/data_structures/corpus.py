#!/usr/bin/env python
"""
Module for organizing SPH, STM files from a corpus
"""

import os
import glob
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tqdm import tqdm

from asrtoolkit.data_structures.audio_file import audio_file
from asrtoolkit.data_structures.time_aligned_text import time_aligned_text


def get_files(data_dir, extension):
  """
    Gets all files in a data directory with given extension
  """
  files = []
  if data_dir and os.path.exists(data_dir):
    files = glob.glob(data_dir + "/*." + extension)
  return files


class exemplar(object):
  """
    Create an exemplar class to pair one audio file with one transcript file
  """
  audio_file = None
  transcript_file = None

  def __init__(self, input_dict=None):
    self.__dict__.update(input_dict if input_dict else {})

  def validate(self):
    " validate exemplar object by constraining that the filenames before the extension are the same "

    valid = True
    audio_filename = ".".join(self.audio_file.location.split(".")[:-1])
    transcript_filename = ".".join(self.transcript_file.location.split(".")[:-1])
    if audio_filename != transcript_filename:
      print(
        "Mismatch between audio and transcript filename - please check the following: \n" +
        ", ".join((audio_filename, transcript_filename))
      )
      valid = False

    return valid


class corpus(object):
  """
    Create a corpus object for storing information about where files are and how many
  """
  location = None
  exemplars = []

  def __init__(self, input_dict=None):
    """
      Initialize from location and populate list of SPH and STM files into segments
    """
    self.__dict__.update(input_dict if input_dict else {})
    if not self.exemplars:
      audio_files = [audio_file(_) for _ in sorted(get_files(self.location, "sph"))]
      transcript_files = [time_aligned_text(_) for _ in sorted(get_files(self.location, "stm"))]
      self.exemplars = [
        exemplar({
          "audio_file": af,
          "transcript_file": tf
        }) for af, tf in zip(audio_files, transcript_files)
      ]

  def validate(self):
    """
      Check to see if any audio/transcript files are unpaired and report which ones
    """

    return sum(_.validate() for _ in self.exemplars)

  def prepare_for_training(self, target=None):
    """
      Run validation and audio file preparation steps
    """

    # write corpus back in place if no target
    target = self.location if target is None else target

    # clean up
    basename = lambda file_name: file_name.split("/")[-1]

    executor = ThreadPoolExecutor()

    # process audio files concurrently for speed
    futures = [
      executor.submit(partial(_.audio_file.prepare_for_training, target + "/" + basename(_.audio_file.location)))
      for _ in self.exemplars
    ]

    # trigger conversion and gather results
    audio_files = [future.result() for future in tqdm(futures)]

    transcript_files = [
      _.transcript_file.write(target + "/" + basename(_.transcript_file.location)) for _ in self.exemplars
    ]

    new_corpus = corpus(
      {
        "location":
          target,
        "exemplars":
          [exemplar({
            "audio_file": af,
            "transcript_file": tf
          }) for af, tf in zip(audio_files, transcript_files)],
      }
    )
    new_corpus.validate()

  def __add__(self, other):
    """ Allow addition of corpora via + operator """
    return corpus({"location": None, "exemplars": self.exemplars + other.exemplars})

  def __iadd__(self, other):
    """ Allow addition of corpora via += operator """
    self.exemplars = self.exemplars + other.exemplars
    return self

  def __sub__(self, other):
    """ Allow addition of corpora via - operator """
    return corpus({"location": None, "exemplars": [_ for _ in self.exemplars if _ not in other.exemplars]})

  def __isub__(self, other):
    """ Allow subtraction of corpora via -= operator """
    self.exemplars = [_ for _ in self.exemplars if _ not in other.exemplars]
    return self

  def __getitem__(self, given):
    """ Allow slicing of corpora via [] """
    return corpus(
      {
        "location": self.location,
        "exemplars": [self.exemplars[given]] if not isinstance(given, slice) else self.exemplars[given]
      }
    )
