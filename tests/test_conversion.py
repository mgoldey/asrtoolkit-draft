#!/usr/bin/env python
"""
Test file conversion using samples
"""
import subprocess


def test_conversion():
  " execute single test "

  from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
  input_file = time_aligned_text("../samples/BillGatesTEDTalk.stm")
  input_file.write("file_conversion_test.txt")
  reference_sha = subprocess.Popen(["sha1sum", "../samples/BillGatesTEDTalk.txt"],
                                   stdout=subprocess.PIPE).stdout.read().decode().split()[0]
  new_sha = subprocess.Popen(["sha1sum", "file_conversion_test.txt"],
                             stdout=subprocess.PIPE).stdout.read().decode().split()[0]
  assert reference_sha == new_sha


if __name__ == '__main__':
  import sys
  import pytest
  pytest.main(sys.argv)
