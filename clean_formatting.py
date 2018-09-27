#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text line cleaning functions. For WER calculations, final text should be utf chars a-z and \'
"""

from __future__ import print_function
import num2words
import re
import sys
import os


def contains_digit(strIn):
  " check if string contains digit "
  if len(strIn) == 0:
    return False
  for char in strIn:
    if char.isdigit():
      return True
  return False


def ordinal_2string(strIn):
  " convert strings '1st', '2nd', '3rd', ... to a string/word with chars a-z "
  try:
    if contains_digit(strIn) and (strIn[-2:] == 'st' or strIn[-2:] == 'nd' or strIn[-2:] == 'rd' or strIn[-2:] == 'th'):
      return (num2words.num2words(int(strIn[:-2]), ordinal=True)).replace(',', '').replace('-', ' ')
    else:
      return strIn
  except:
    return strIn


def contains_dollar_sign(strIn):
  " check if string contains '$' "
  if len(strIn) == 0:
    return False
  for char in strIn:
    if char == '$':
      return True
  return False


def dollars_2string(strIn):
  " convert dollar strings '$2', '$2.56', '$10', '$1000000', ... to a string/word with chars a-z "
  try:
    if contains_dollar_sign(strIn):
      if not '.' in strIn:
        number = int(strIn.replace('$', ''))
      else:
        number = float(strIn.replace('$', ''))

      return (num2words.num2words(number) + ' dollars').replace(',', '').replace('-', ' ')
    else:
      return strIn
  except:
    return strIn


def contains_percent(strIn):
  " check if string contains '%' "
  if len(strIn) == 0:
    return False
  for char in strIn:
    if char == '%':
      return True
  return False


def percent_2string(strIn):
  " convert percent to string "
  try:
    if contains_percent(strIn) and len(strIn) > 1:  # case of strIn= '%'
      if not '.' in strIn:
        number = int(strIn.replace('%', ''))
        return (num2words.num2words(number) + ' percent').replace(',', '').replace('-', ' ')
      else:
        parts = strIn.replace('%', '').split('.')
        return (num2words.num2words(int(parts[0])) + \
          " point " + \
          " ".join([num2words.num2words(int(pa)) for pa in parts[1]]) +\
          " percent")\
            .replace(',', '').replace('-', ' ')
    else:
      if strIn == '%':
        return "percent"
      else:
        return strIn
  except:
    return strIn


def contains_all_digits(strIn):
  " integers "
  if len(strIn) == 0:
    return False
  for char in strIn:
    if not char.isdigit():
      return False
  return True


def alldigits_2string(strIn):
  try:
    if contains_all_digits(strIn):
      return num2words.num2words(int(strIn)).replace(',', '').replace('-', ' ')
    else:
      return strIn
  except:
    return strIn


def alldigits_decimal_2string(strIn):
  " convert float numbers to strings "
  try:
    if len(strIn) > 0:
      if "." in strIn and contains_all_digits(strIn.replace('.', '')) and not strIn[0] == '.':  # account for str  '.5'
        parts = strIn.split('.')
        return (
          num2words.num2words(int(parts[0])) + " point " + " ".join([num2words.num2words(int(pa)) for pa in parts[1]])
        ).replace(',', '').replace('-', ' ')
      else:
        if strIn[0] == '.' and contains_all_digits(strIn.replace('.', '')):
          parts = strIn.split('.')
          return ("point " + \
            " ".join([num2words.num2words(int(pa)) for pa in parts[1]]))\
          .replace(',','').replace('-', ' ')
        else:
          return strIn
    else:
      return strIn  #  empty string ? -> "." and  . will be removed later
  except:
    return strIn


def alldigits_slash_2string(strIn):
  ' fractions   1/5 -> "one fifth" '
  try:
    if len(strIn) > 0:
      if "/" in strIn and contains_all_digits(strIn.replace('/', '')) and not strIn[0] == '/':  # account for str  '/5'
        parts = strIn.split('/')
        return (num2words.num2words(int(parts[0])) + \
          " " + \
          " ".join([num2words.num2words(int(pa)) for pa in parts[1]])).replace(',', '').replace('-', ' ')
      else:
        if strIn[0] == '/':
          parts = strIn.split('/')
          return ("over " + \
            " ".join([num2words.num2words(int(pa)) for pa in parts[1]])).replace(',','').replace('-', ' ')
        else:
          return strIn
    else:
      return strIn
  except:
    return strIn


def alldigits_s_2string(strIn):
  " 80s, 8's.  years/decades "
  try:
    if len(strIn) > 0:
      if "s" in strIn and contains_all_digits(strIn.replace('s', '')) and not strIn[0] == 's':
        if len(strIn.replace('s', '')) == 4:  # case for four len number '1980s', '1660s'
          if strIn.replace('s', '')[2:] == '00':
            return num2words.num2words(int(strIn.replace('s', '')[0:2])) + " hundreds"  #case for ~1600s
          else:
            return num2words.num2words(int(strIn.replace('s', '')[0:2])) + \
              " " + num2words.num2words(int(strIn.replace('s', '')[2:])) + " s"
        else:
          parts = strIn.split('s')
          return (num2words.num2words(int(parts[0])) + " s").replace(',', '').replace('-', ' ')

      elif "'s" in strIn and contains_all_digits(strIn.replace("'s", "")) and not strIn[0:2] == "'s":
        if len(strIn.replace("'s", "")) == 4:  # case for four len number,  '1980s', '1660s'
          if strIn.replace("'s", "")[2:] == '00':
            return num2words.num2words(int(strIn.replace("'s", "")[0:2])) + " hundreds"  #case for ~1600s
          else:
            return num2words.num2words(int(strIn.replace("'s", "")[0:2])) + \
              " " + num2words.num2words(int(strIn.replace("'s", "")[2:])) + " s"
        else:
          parts = strIn.split("'s")
          return (num2words.num2words(int(parts[0])) + " s").replace(',', '').replace('-', ' ')
      else:
        return strIn
    else:
      return strIn
  except:
    return strIn


def alldigits_colon_2string(strIn):
  " 1:10,  time strings "
  try:
    if len(strIn) > 0:
      if ":" in strIn and contains_all_digits(strIn.replace(':', '')) and not strIn[0] == ':':  # account for str  ':5'
        parts = strIn.split(':')
        return ((num2words.num2words(int(parts[0])) + " " + \
          num2words.num2words(int(parts[1]))).replace(',','').replace('-', ' '))
      else:
        if strIn[0] == ':':
          parts = strIn.split(':')
          return (num2words.num2words(int(parts[1]))).replace(',', '').replace('-', ' ')
        else:
          return strIn
    else:
      return strIn
  except:
    return strIn


def find_digits_and_letters(strIn):  # 27abc123aaa'
  ' regex find digits mixed in with letters    "mo7", "27a" '
  try:
    if len(strIn) > 1:
      strOut = ""
      l1 = list(re.finditer('\d+', strIn))  # digit
      l2 = list(re.finditer('[a-z]+', strIn))  # not digit,  chars a-z

      if len(l1) > 0 and len(l2) > 0:
        l3 = l1 + l2  # combine lists
        l3_sorted = sorted(l3, key=lambda found: found.span()[0])  #sort by start of span

        for item in l3_sorted:
          if contains_all_digits(item.group(0)):
            strOut += " " + num2words.num2words(int(item.group(0))).replace(',', '').replace('-', ' ')
          else:
            strOut += " " + " ".join(list(item.group(0)))
        return strOut.strip()
      else:
        return strIn  #if no digits or letters found
    else:
      return strIn
  except:
    return strIn


def begins_with_dash(strIn):
  " dash. check for " - " at front,  ~ negative numbers "
  if len(strIn) == 0:
    return False
  if strIn[0] == "-":
    return True
  else:
    return False


def dash_split_number(strIn):
  'negatives   "-10.2"   -->   "negative 10.2".  only replaces "-" with "negative " '
  try:
    if len(strIn) > 1:
      if begins_with_dash(strIn):
        if contains_all_digits(strIn[1:]):  # case of all digits
          return "negative " + strIn[1:]
        elif contains_all_digits(strIn[1:].replace('.', '')):  # case of all digits with decimal points
          return "negetive " + strIn[1:]
        else:
          return strIn.replace('-', '')  # '-asdasdas'    remove -, add \space.   case of "-", replace "  "
      else:
        return strIn
    else:
      return strIn
  except:
    return strIn


# regex find consecutive consonants and space them apart.  bgc --> b g c ;  abc --> a b c.   'cat' will not be changed
def acronym_2str(strIn):
  # if 3 or more consecutive consonants in the entire string
  try:  #include 'y' as vowel.  'try' and 'why' was split
    if len(list(re.finditer('[b-df-hj-np-tv-xz]{3,}', strIn))[0].group(0)) == len(strIn):
      return " ".join(list(re.finditer('[b-df-hj-np-tv-xz]{3,}', strIn))[0].group(0))
    else:
      return strIn
  except:
    return strIn


#  ABC  -->  A B C
def capitals_expand(strIn):
  try:
    if strIn.isupper():
      return " ".join([x.lower() for x in strIn])
    else:
      return strIn.lower()
  except:
    return strIn.lower()


#   A.b.C.  -->  A b C
def acronym_dot2str(strIn):
  try:
    return re.sub(r'([a-zA-Z])\.', r'\g<1> ', strIn).strip()
  except:
    return strIn


### order of fixes
# rem ","
# negative numbers
# replace "-"," "   and "+", "plus"
# ordinal 1st/2nd, $, %
# alldigits
# alldigits with decimal
# alldigits with slash. (fractions)
# alldigits with colon.(time 1:10)
# find_digits_and_letters   aa27, m07
# replace "'s" with " 's"
# acronyms        'ngkf'  ,  gfi won't get split since a vowel appears
# contractions  it's  ->  it 's
# replace .com, .org, .gov, .net
# rem "."
# .
# .


def clean_up(lineIn):

  #line = lineIn[:-2]     # removing ending punctuation.  ### Note: lexical format does not have ending punctuation
  line = lineIn

  temp_words = line.strip().split(" ")
  temp_words = [w.replace(',', '').replace('*', '').replace('&', '') for w in temp_words]  # remove ',', '*', &
  temp_words = [capitals_expand(w) for w in temp_words]  # expand capital chars/ acronyms.  CEO,  NATO
  temp_words = [dash_split_number(w) for w in temp_words]  # split if have -[char],  len>1
  temp_words = " ".join(temp_words).replace(' - ', ' ').replace('-', ' ').replace('+', 'plus').split(" ")
  #[w.replace('-',' ') for w in temp_words]
  temp_words = [w for w in temp_words if len(w) > 0]
  temp_words = [ordinal_2string(w) for w in temp_words]
  temp_words = [dollars_2string(w) for w in temp_words]
  temp_words = [percent_2string(w) for w in temp_words]
  temp_words = [alldigits_2string(w) for w in temp_words]
  temp_words = [alldigits_decimal_2string(w) for w in temp_words]
  temp_words = [alldigits_slash_2string(w) for w in temp_words]
  temp_words = [alldigits_s_2string(w) for w in temp_words]
  temp_words = [alldigits_colon_2string(w) for w in temp_words]
  temp_words = [find_digits_and_letters(w) for w in temp_words]
  #temp_words = " ".join(temp_words).replace("'"," '").split(" ")  # keep contractions without space
  temp_words = [acronym_2str(w) for w in temp_words]
  temp_words = [
    w.replace('.com', ' dot com').replace('.net', ' dot net').replace('.org', ' dot org').replace('.gov', ' dot gov')
    for w in temp_words
  ]
  temp_words = [acronym_dot2str(w) for w in temp_words]
  # encode then decode (in case this is python 3)
  temp_words = [w.replace('.', '').encode().decode('utf-8') for w in temp_words]  # remove '.'

  out = " ".join(temp_words).lower()
  out = re.sub(r"[^a-z\-' ]", "", out)  # remove chars not a-z, "'", " "  ("-" already removed)

  return out


if __name__ == '__main__':
  fileName = sys.argv[1]

  with open(fileName, 'r') as f:
    lines = f.readlines()

  try:
    os.remove(fileName.replace('.txt', '') + '_cleaned.txt')
  except:
    pass

  cleaned = []
  for line in lines:
    cleaned.append(clean_up(line) + "\n")

  with open(fileName.replace('.txt', '') + '_cleaned.txt', 'w') as f2:
    f2.writelines(cleaned)

  print('File output: ' + fileName.replace('.txt', '') + '_cleaned.txt')
