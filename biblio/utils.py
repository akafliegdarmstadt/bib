from enum import IntEnum

class CopyType(IntEnum):
  PDF = 1
  REAL = 2
  SOFTWARE = 3
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
