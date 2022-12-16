
from collections import defaultdict
from typing import List
import pandas as pd
from .individual_mapper import IndividualMapper
import re


from enum import Enum

AgeEncodingType = Enum('AgeEncodingType', ['YEAR', 'ISO8601', 'CUSTOM'])
ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"


class IndentifierColumnMapper(IndividualMapper):
    super.__init__(individual_type="identifier")