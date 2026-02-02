#!/usr/bin/env python3
"""
Systematically extract BUDA ranges to find 640x400 screens
"""

import sys
from pathlib import Path
import math
from PIL import Image
import shutil

budas = [
  {
    "BUDA": 0,
    "START_OFFSET": 260,
    "TYPE": "IMAGE",
    "DESC": "CUADROCAMA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	  "offset" : 0
  },
  {
    "BUDA": 1,
    "START_OFFSET": 680,
    "TYPE": "IMAGE",
    "DESC": "CUADROCAMA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	  "offset" : 0
  },
  {
    "BUDA": 2,
    "START_OFFSET": 11150,
    "TYPE": "IMAGE",
    "DESC": "CUADROCAMA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 3,
    "START_OFFSET": 17616,
    "TYPE": "IMAGE",
    "DESC": "CUADROCAMA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 4,
    "START_OFFSET": 22598,
    "TYPE": "IMAGE",
    "DESC": "CUADROCAMA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 5,
    "START_OFFSET": 28766,
    "TYPE": "IMAGE",
    "DESC": "CUADROCAMA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 6,
    "START_OFFSET": 30890,
    "TYPE": "IMAGE",
    "DESC": "CUADROCAMA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 7,
    "START_OFFSET": 67758,
    "TYPE": "ANIM",
    "DESC": "ALFRED PEINANDO DERECHA",
    "WIDTH": 51,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 8,
    "START_OFFSET": 88404,
    "TYPE": "ANIM",
    "DESC": "ALFRED PEINANDO IZQUIERDA",
    "WIDTH": 51,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 9,
    "START_OFFSET": 109034,
    "TYPE": "IMAGE",
    "DESC": "ORDENADOR",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 10,
    "START_OFFSET": 112386,
    "TYPE": "IMAGE",
    "DESC": "ORDENADOR",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 11,
    "START_OFFSET": 132440,
    "TYPE": "IMAGE",
    "DESC": "ORDENADOR",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 12,
    "START_OFFSET": 139082,
    "TYPE": "IMAGE",
    "DESC": "ORDENADOR",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 13,
    "START_OFFSET": 145736,
    "TYPE": "IMAGE",
    "DESC": "ORDENADOR",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 14,
    "START_OFFSET": 152472,
    "TYPE": "IMAGE",
    "DESC": "ORDENADOR",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 15,
    "START_OFFSET": 170502,
    "TYPE": "IMAGE",
    "DESC": "ORDENADOR",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 16,
    "START_OFFSET": 192176,
    "TYPE": "IMAGE",
    "DESC": "ORDENADOR",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 17,
    "START_OFFSET": 212921,
    "TYPE": "SPRITE",
    "DESC": "PAREJA0",
    "WIDTH": 62,
    "START": "UNKNOWN",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 0,
  },
  {
    "BUDA": 18,
    "START_OFFSET": 236641,
    "TYPE": "ANIM",
    "DESC": "PAREJA",
    "WIDTH": 62,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 19,
    "START_OFFSET": 261445,
    "TYPE": "ANIM",
    "DESC": "FARAON CAMINA",
    "WIDTH": 64,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 20,
    "START_OFFSET": 280355,
    "TYPE": "ANIM",
    "DESC": "FARAON LEVANTA MANO",
    "WIDTH": 64,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 21,
    "START_OFFSET": 298585,
    "TYPE": "ANIM",
    "DESC": "PAREJA (2)",
    "WIDTH": 62,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 22,
    "START_OFFSET": 341225,
    "TYPE": "ANIM",
    "DESC": "GUARDA",
    "WIDTH": 43,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 23,
    "START_OFFSET": 360833,
    "TYPE": "ANIM",
    "DESC": "CHICA SE LAVA",
    "WIDTH": 49,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 24,
    "START_OFFSET": 381445,
    "TYPE": "ANIM",
    "DESC": "LLAMA",
    "WIDTH": 7,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 25,
    "START_OFFSET": 381821,
    "TYPE": "ANIM",
    "DESC": "CHICA SE LAVA 2",
    "WIDTH": 49,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 26,
    "START_OFFSET": 397661,
    "TYPE": "ANIM",
    "DESC": "RELOJ",
    "WIDTH": 13,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 27,
    "START_OFFSET": 398559,
    "TYPE": "ANIM",
    "DESC": "ALFREDCAMA",
    "WIDTH": 59,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 28,
    "START_OFFSET": 411587,
    "TYPE": "IMAGE",
    "DESC": "ALFRED CIRCULO",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : False,
    "isContinued":  True,
	  "offset" : 0
  },
  {
    "BUDA": 29,
    "START_OFFSET": 422789,
    "TYPE": "IMAGE",
    "DESC": "ALFRED CIRCULO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 30,
    "START_OFFSET": 432769,
    "TYPE": "IMAGE",
    "DESC": "ALFRED CIRCULO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 31,
    "START_OFFSET": 448051,
    "TYPE": "IMAGE",
    "DESC": "ALFRED CIRCULO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 32,
    "START_OFFSET": 457673,
    "TYPE": "IMAGE",
    "DESC": "RECETA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 33,
    "START_OFFSET": 460449,
    "TYPE": "IMAGE",
    "DESC": "RECETA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 34,
    "START_OFFSET": 466747,
    "TYPE": "IMAGE",
    "DESC": "RECETA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 35,
    "START_OFFSET": 475631,
    "TYPE": "IMAGE",
    "DESC": "RECETA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 36,
    "START_OFFSET": 482397,
    "TYPE": "IMAGE",
    "DESC": "RECETA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 37,
    "START_OFFSET": 488721,
    "TYPE": "IMAGE",
    "DESC": "RECETA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 38,
    "START_OFFSET": 494743,
    "TYPE": "IMAGE",
    "DESC": "RECETA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 39,
    "START_OFFSET": 503189,
    "TYPE": "IMAGE",
    "DESC": "RECETA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 40,
    "START_OFFSET": 505517,
    "TYPE": "IMAGE",
    "DESC": "DAILY",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  True,
	"offset" : 864
  },
  {
    "BUDA": 41,
    "START_OFFSET": 506841,
    "TYPE": "IMAGE",
    "DESC": "DAILY",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 42,
    "START_OFFSET": 511013,
    "TYPE": "IMAGE",
    "DESC": "DAILY",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 43,
    "START_OFFSET": 513977,
    "TYPE": "IMAGE",
    "DESC": "DAILY",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 44,
    "START_OFFSET": 517677,
    "TYPE": "IMAGE",
    "DESC": "DAILY",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 45,
    "START_OFFSET": 529943,
    "TYPE": "IMAGE",
    "DESC": "DAILY",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 46,
    "START_OFFSET": 544723,
    "TYPE": "IMAGE",
    "DESC": "DAILY",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 47,
    "START_OFFSET": 556911,
    "TYPE": "UNKNOWN",
    "DESC": "DAILY",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 48,
    "START_OFFSET": 558009,
    "TYPE": "ANIM",
    "DESC": "CHAFARDER BUG",
    "WIDTH": 640,
    "START": "UNKNOWN",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 768
  },
  {
    "BUDA": 49,
    "START_OFFSET": 558913,
    "TYPE": "ANIM",
    "DESC": "ALFRED LEE LIBRO",
    "WIDTH": 51,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 768
  },
  {
    "BUDA": 50,
    "START_OFFSET": 578939,
    "TYPE": "SPRITE",
    "DESC": "ALFRED LEE RECETa",
    "WIDTH": 51,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 51,
    "START_OFFSET": 598047,
    "TYPE": "IMAGE",
    "DESC": "THINKINGBALLOON",
    "WIDTH": 247,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 52,
    "START_OFFSET": 598907,
    "TYPE": "IMAGE",
    "DESC": "TABLA",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : False,
    "isContinued":  True,
	  "offset" : 0
  },
  {
    "BUDA": 53,
    "START_OFFSET": 604459,
    "TYPE": "IMAGE",
    "DESC": "TABLA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 54,
    "START_OFFSET": 623131,
    "TYPE": "IMAGE",
    "DESC": "TABLA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 55,
    "START_OFFSET": 642223,
    "TYPE": "IMAGE",
    "DESC": "TABLA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 56,
    "START_OFFSET": 661561,
    "TYPE": "IMAGE",
    "DESC": "TABLA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 57,
    "START_OFFSET": 679733,
    "TYPE": "IMAGE",
    "DESC": "TABLA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 58,
    "START_OFFSET": 698901,
    "TYPE": "IMAGE",
    "DESC": "TABLA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 59,
    "START_OFFSET": 718261,
    "TYPE": "IMAGE",
    "DESC": "TABLA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 60,
    "START_OFFSET": 724707,
    "TYPE": "IMAGE",
    "DESC": "MAPA",
    "WIDTH": 640,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  True,
	  "offset" : 778
  },
  {
    "BUDA": 61,
    "START_OFFSET": 749285,
    "TYPE": "IMAGE",
    "DESC": "MAPA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 62,
    "START_OFFSET": 778259,
    "TYPE": "IMAGE",
    "DESC": "MAPA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 63,
    "START_OFFSET": 807535,
    "TYPE": "IMAGE",
    "DESC": "MAPA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 64,
    "START_OFFSET": 834765,
    "TYPE": "IMAGE",
    "DESC": "MAPA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 65,
    "START_OFFSET": 855439,
    "TYPE": "IMAGE",
    "DESC": "MAPA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 66,
    "START_OFFSET": 873425,
    "TYPE": "IMAGE",
    "DESC": "MAPA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 67,
    "START_OFFSET": 894345,
    "TYPE": "IMAGE",
    "DESC": "MAPA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 68,
    "START_OFFSET": 909325,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  True,
	"offset" : 768
  },
  {
    "BUDA": 69,
    "START_OFFSET": 918951,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 70,
    "START_OFFSET": 942699,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 71,
    "START_OFFSET": 956557,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 72,
    "START_OFFSET": 973643,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 73,
    "START_OFFSET": 986445,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 74,
    "START_OFFSET": 1006481,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 75,
    "START_OFFSET": 1030041,
    "TYPE": "UNKNOWN",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 76,
    "START_OFFSET": 1041501,
    "TYPE": "IMAGE",
    "DESC": "UNKNOWN",
    "WIDTH": 72,
    "START": "UNKNOWN",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 77,
    "START_OFFSET": 1042753,
    "TYPE": "IMAGE",
    "DESC": "CUADRADO",
    "WIDTH": 637,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 78,
    "START_OFFSET": 1047519,
    "TYPE": "IMAGE",
    "DESC": "LIBRO",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : False,
    "isContinued":  True,
	  "offset" : 100
  },
  {
    "BUDA": 79,
    "START_OFFSET": 1050483,
    "TYPE": "IMAGE",
    "DESC": "LIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 80,
    "START_OFFSET": 1070619,
    "TYPE": "IMAGE",
    "DESC": "LIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 81,
    "START_OFFSET": 1090115,
    "TYPE": "IMAGE",
    "DESC": "LIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 82,
    "START_OFFSET": 1103745,
    "TYPE": "IMAGE",
    "DESC": "LIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	  "offset" : 0
  },
  {
    "BUDA": 83,
    "START_OFFSET": 1119391,
    "TYPE": "IMAGE",
    "DESC": "LIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 84,
    "START_OFFSET": 1134469,
    "TYPE": "IMAGE",
    "DESC": "LIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 85,
    "START_OFFSET": 1144071,
    "TYPE": "IMAGE",
    "DESC": "LIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 86,
    "START_OFFSET": 1147077,
    "TYPE": "IMAGE",
    "DESC": "UNKNOWN",
    "WIDTH": 640,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  True,
	  "offset" : 768
  },
  {
    "BUDA": 87,
    "START_OFFSET": 1155375,
    "TYPE": "IMAGE",
    "DESC": "UNKNOWN",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	  "offset" : 0
  },
  {
    "BUDA": 88,
    "START_OFFSET": 1174169,
    "TYPE": "IMAGE",
    "DESC": "UNKNOWN",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 89,
    "START_OFFSET": 1190857,
    "TYPE": "IMAGE",
    "DESC": "UNKNOWN",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 90,
    "START_OFFSET": 1206407,
    "TYPE": "IMAGE",
    "DESC": "UNKNOWN",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 91,
    "START_OFFSET": 1221291,
    "TYPE": "IMAGE",
    "DESC": "UNKNOWN",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 92,
    "START_OFFSET": 1236715,
    "TYPE": "IMAGE",
    "DESC": "UNKNOWN",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 93,
    "START_OFFSET": 1262291,
    "TYPE": "SPRITEMAP",
    "DESC": "UNKNOWN",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 94,
    "START_OFFSET": 1267951,
    "TYPE": "IMAGE",
    "DESC": "SIMBOLOS",
    "WIDTH": 119,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 768
  },
  {
    "BUDA": 95,
    "START_OFFSET": 1341231,
    "TYPE": "RAW",
    "DESC": "UNKNOWN",
    "WIDTH": 119,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 96,
    "START_OFFSET": 1347763,
    "TYPE": "RAW",
    "DESC": "UNKNOWN",
    "WIDTH": 146,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 97,
    "START_OFFSET": 1374808,
    "TYPE": "SPRITE",
    "DESC": "BALLOONS AGAIN",
    "WIDTH": 254,
    "START": "UNKNOWN",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : "UNKNOWN",
    "isContinued":  False,
	  "offset" : 14
  },
  {
    "BUDA": 98,
    "START_OFFSET": 1387140,
    "TYPE": "IMAGE",
    "DESC": "CUADRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 99,
    "START_OFFSET": 1387404,
    "TYPE": "IMAGE",
    "DESC": "CUADRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 100,
    "START_OFFSET": 1388712,
    "TYPE": "IMAGE",
    "DESC": "CUADRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 101,
    "START_OFFSET": 1396422,
    "TYPE": "IMAGE",
    "DESC": "CUADRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 102,
    "START_OFFSET": 1402748,
    "TYPE": "IMAGE",
    "DESC": "CUADRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 103,
    "START_OFFSET": 1409456,
    "TYPE": "IMAGE",
    "DESC": "CUADRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 104,
    "START_OFFSET": 1419432,
    "TYPE": "IMAGE",
    "DESC": "CUADRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 105,
    "START_OFFSET": 1425134,
    "TYPE": "ANIM",
    "DESC": "CUADRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 106,
    "START_OFFSET": 1425348,
    "TYPE": "MULTIANIM",
    "DESC": "ALFREDCAMA",
    "WIDTH": 76,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 768
  },
  {
    "BUDA": 107,
    "START_OFFSET": 1446090,
    "TYPE": "ANIM",
    "DESC": "NADADORAS",
    "WIDTH": 93, #68, 79, 54,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 768
  },
  {
    "BUDA": 108,
    "START_OFFSET": 1473188,
    "TYPE": "ANIM",
    "DESC": "TIPOS BEBIENDO",
    "WIDTH": 152,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 172
  },
  {
    "BUDA": 109,
    "START_OFFSET": 1512056,
    "TYPE": "ANIM",
    "DESC": "TIPOSBEBENYCAEN",
    "WIDTH": 172,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 110,
    "START_OFFSET": 1526428,
    "TYPE": "ANIM",
    "DESC": "SMOKE",
    "WIDTH": 196,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 111,
    "START_OFFSET": 1556536,
    "TYPE": "ANIM",
    "DESC": "COCODRILO",
    "WIDTH": 171,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 112,
    "START_OFFSET": 1583698,
    "TYPE": "ANIM",
    "DESC": "TRAMPILLA",
    "WIDTH": 113,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 113,
    "START_OFFSET": 1749470,
    "TYPE": "ANIM",
    "DESC": "ALFREDAGACHA",
    "WIDTH": 95,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 114,
    "START_OFFSET": 1761230,
    "TYPE": "ANIM",
    "DESC": "ALFREDESCALA",
    "WIDTH": 33,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 115,
    "START_OFFSET": 1766374,
    "TYPE": "ANIM",
    "DESC": "ALFREDESCALA 2",
    "WIDTH": 33,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 116,
    "START_OFFSET": 2060922,
    "TYPE": "ANIM",
    "DESC": "ALFREDMUNHECO",
    "WIDTH": 116,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 117,
    "START_OFFSET": 2115628,
    "TYPE": "ANIM",
    "DESC": "ALFREDMUNHECO",
    "WIDTH": 177,
    "START": "0",
    "OFFSET RLE DEC": " COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 118,
    "START_OFFSET": 2176932,
    "TYPE": "SPRITE",
    "DESC": "POPUP",
    "WIDTH": 247,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 119,
    "START_OFFSET": 2201878,
    "TYPE": "SPRITE",
    "DESC": "ICONOS MUSICA",
    "WIDTH": 198,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 120,
    "START_OFFSET": 2208282,
    "TYPE": "SPRITE",
    "DESC": "ICONOS MUSICA",
    "WIDTH": 66,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 121,
    "START_OFFSET": 2210444,
    "TYPE": "SPRITE",
    "DESC": "ICONOS MUSICA",
    "WIDTH": 66,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 122,
    "START_OFFSET": 2212842,
    "TYPE": "SPRITE",
    "DESC": "ICONOS MUSICA",
    "WIDTH": 66,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 123,
    "START_OFFSET": 2214704,
    "TYPE": "SPRITE",
    "DESC": "EN BLANCO",
    "WIDTH": 201,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 124,
    "START_OFFSET": 2214756,
    "TYPE": "IMAGE",
    "DESC": "UNKNOWN",
    "WIDTH": 213,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 125,
    "START_OFFSET": 2227414,
    "TYPE": "IMAGE",
    "DESC": "EN NEGRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 126,
    "START_OFFSET": 2227678,
    "TYPE": "IMAGE",
    "DESC": "EN NEGRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 127,
    "START_OFFSET": 2227942,
    "TYPE": "IMAGE",
    "DESC": "EN NEGRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 128,
    "START_OFFSET": 2228206,
    "TYPE": "IMAGE",
    "DESC": "EN NEGRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 129,
    "START_OFFSET": 2228470,
    "TYPE": "IMAGE",
    "DESC": "EN NEGRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 130,
    "START_OFFSET": 2228734,
    "TYPE": "IMAGE",
    "DESC": "EN NEGRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 131,
    "START_OFFSET": 2228998,
    "TYPE": "IMAGE",
    "DESC": "EN NEGRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 132,
    "START_OFFSET": 2229262,
    "TYPE": "PALETTE",
    "DESC": "EN NEGRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 133,
    "START_OFFSET": 2230248,
    "TYPE": "DUNNO",
    "DESC": "PALETTE",
    "WIDTH": 100,
    "START": "UNKNOWN",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 134,
    "START_OFFSET": 2230262,
    "TYPE": "IMAGE",
    "DESC": "ALFREDPELEA",
    "WIDTH": 71,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 135,
    "START_OFFSET": 2253652,
    "TYPE": "IMAGE",
    "DESC": "OTROLIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 136,
    "START_OFFSET": 2258828,
    "TYPE": "IMAGE",
    "DESC": "OTROLIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 137,
    "START_OFFSET": 2262630,
    "TYPE": "IMAGE",
    "DESC": "OTROLIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 138,
    "START_OFFSET": 2264882,
    "TYPE": "IMAGE",
    "DESC": "OTROLIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 139,
    "START_OFFSET": 2266764,
    "TYPE": "IMAGE",
    "DESC": "OTROLIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 140,
    "START_OFFSET": 2268656,
    "TYPE": "IMAGE",
    "DESC": "OTROLIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 141,
    "START_OFFSET": 2275860,
    "TYPE": "IMAGE",
    "DESC": "OTROLIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 142,
    "START_OFFSET": 2284460,
    "TYPE": "IMAGE",
    "DESC": "OTROLIBRO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 143,
    "START_OFFSET": 2284674,
    "TYPE": "ANIM",
    "DESC": "PALETTE",
    "WIDTH": 200,
    "START": "UNKNOWN",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 768
  },
  {
    "BUDA": 144,
    "START_OFFSET": 2285690,
    "TYPE": "IMAGE",
    "DESC": "ALFREDCAMA",
    "WIDTH": 71,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 145,
    "START_OFFSET": 2306534,
    "TYPE": "IMAGE",
    "DESC": "CENSORED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 146,
    "START_OFFSET": 2306798,
    "TYPE": "IMAGE",
    "DESC": "CENSORED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 147,
    "START_OFFSET": 2307118,
    "TYPE": "IMAGE",
    "DESC": "CENSORED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 148,
    "START_OFFSET": 2311128,
    "TYPE": "IMAGE",
    "DESC": "CENSORED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 149,
    "START_OFFSET": 2317890,
    "TYPE": "IMAGE",
    "DESC": "CENSORED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 150,
    "START_OFFSET": 2320318,
    "TYPE": "IMAGE",
    "DESC": "CENSORED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 151,
    "START_OFFSET": 2320582,
    "TYPE": "IMAGE",
    "DESC": "CENSORED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 152,
    "START_OFFSET": 2320846,
    "TYPE": "IMAGE",
    "DESC": "CENSORED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 153,
    "START_OFFSET": 2321060,
    "TYPE": "IMAGE",
    "DESC": "CODE",
    "WIDTH": 640,
    "START": "AFTER PALETTE",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 768
  },
  {
    "BUDA": 154,
    "START_OFFSET": 2361384,
    "TYPE": "IMAGE",
    "DESC": "CODE 2",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 155,
    "START_OFFSET": 2381078,
    "TYPE": "IMAGE",
    "DESC": "ARTWORK",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 156,
    "START_OFFSET": 2405262,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 157,
    "START_OFFSET": 2500216,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "UNKNOWN",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 158,
    "START_OFFSET": 2656194,
    "TYPE": "UI",
    "DESC": "MENU",
    "WIDTH": 198,
    "START": "UNKNOWN",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : "UNKNOWN",
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 159,
    "START_OFFSET": 2662584,
    "TYPE": "SPRITE",
    "DESC": "MENUCONTROL",
    "WIDTH": 66,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 160,
    "START_OFFSET": 2664742,
    "TYPE": "SPRITE",
    "DESC": "MENUCONTROL",
    "WIDTH": 66,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 161,
    "START_OFFSET": 2667136,
    "TYPE": "SPRITE",
    "DESC": "MENUCONTROL",
    "WIDTH": 66,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 162,
    "START_OFFSET": 2668994,
    "TYPE": "IMAGE",
    "DESC": "MENUCONTROL",
    "WIDTH": 66,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 163,
    "START_OFFSET": 2669046,
    "TYPE": "IMAGE",
    "DESC": "CODE 3",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 164,
    "START_OFFSET": 2688164,
    "TYPE": "IMAGE",
    "DESC": "CODE 4",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 165,
    "START_OFFSET": 2727560,
    "TYPE": "IMAGE",
    "DESC": "DISCO ALFRED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 166,
    "START_OFFSET": 2727824,
    "TYPE": "IMAGE",
    "DESC": "DISCO ALFRED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 167,
    "START_OFFSET": 2742300,
    "TYPE": "IMAGE",
    "DESC": "DISCO ALFRED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 168,
    "START_OFFSET": 2767184,
    "TYPE": "IMAGE",
    "DESC": "DISCO ALFRED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 169,
    "START_OFFSET": 2787502,
    "TYPE": "IMAGE",
    "DESC": "DISCO ALFRED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 170,
    "START_OFFSET": 2808956,
    "TYPE": "IMAGE",
    "DESC": "DISCO ALFRED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 171,
    "START_OFFSET": 2830578,
    "TYPE": "IMAGE",
    "DESC": "DISCO ALFRED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 172,
    "START_OFFSET": 2833058,
    "TYPE": "IMAGE",
    "DESC": "DISCO ALFRED",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 173,
    "START_OFFSET": 2833272,
    "TYPE": "IMAGE",
    "DESC": "PERGAMINO",
    "WIDTH": 640,
    "START": "AFTER PALETTE",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  True,
	"offset" : 768
  },
  {
    "BUDA": 174,
    "START_OFFSET": 2834304,
    "TYPE": "IMAGE",
    "DESC": "PERGAMINO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 175,
    "START_OFFSET": 2857816,
    "TYPE": "IMAGE",
    "DESC": "PERGAMINO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 176,
    "START_OFFSET": 2881590,
    "TYPE": "IMAGE",
    "DESC": "PERGAMINO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 177,
    "START_OFFSET": 2911516,
    "TYPE": "IMAGE",
    "DESC": "PERGAMINO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 178,
    "START_OFFSET": 2941462,
    "TYPE": "IMAGE",
    "DESC": "PERGAMINO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 179,
    "START_OFFSET": 2969166,
    "TYPE": "IMAGE",
    "DESC": "PERGAMINO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 180,
    "START_OFFSET": 2971582,
    "TYPE": "ANIM",
    "DESC": "PERGAMINO",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 181,
    "START_OFFSET": 2971796,
    "TYPE": "SPRITE",
    "DESC": "ALFREDDESCAMISA",
    "WIDTH": 51,
    "START": "AFTER PALETTE",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 768
  },
  {
    "BUDA": 182,
    "START_OFFSET": 2980868,
    "TYPE": "ANIM",
    "DESC": "OVERLAYMAPA",
    "WIDTH": 158,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 183,
    "START_OFFSET": 3006790,
    "TYPE": "SPRITE",
    "DESC": "HUMO",
    "WIDTH": 196,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 184,
    "START_OFFSET": 3037004,
    "TYPE": "ANIM",
    "DESC": "FLECHAS",
    "WIDTH": 36, #//,31,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 185,
    "START_OFFSET": 3038450,
    "TYPE": "IMAGE",
    "DESC": "ALFREDCAMA",
    "WIDTH": 71,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 186,
    "START_OFFSET": 3058222,
    "TYPE": "IMAGE",
    "DESC": "CONCHICA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 187,
    "START_OFFSET": 3066050,
    "TYPE": "IMAGE",
    "DESC": "CONCHICA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 188,
    "START_OFFSET": 3075630,
    "TYPE": "IMAGE",
    "DESC": "CONCHICA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 189,
    "START_OFFSET": 3094642,
    "TYPE": "IMAGE",
    "DESC": "CONCHICA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 190,
    "START_OFFSET": 3123460,
    "TYPE": "IMAGE",
    "DESC": "CONCHICA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 191,
    "START_OFFSET": 3143534,
    "TYPE": "IMAGE",
    "DESC": "CONCHICA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 192,
    "START_OFFSET": 3165032,
    "TYPE": "IMAGE",
    "DESC": "CONCHICA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 193,
    "START_OFFSET": 3179630,
    "TYPE": "ANIMS",
    "DESC": "CONCHICA",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 194,
    "START_OFFSET": 3185276,
    "TYPE": "ANIMS",
    "DESC": "PIERNAS, MANOS",
    "WIDTH": 114,
    # 55,
    "START": "MEDIO",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : True,
    "isContinued":  False,
	   "offset" : 36970
  },
  {
    "BUDA": 195,
    "START_OFFSET": 3271450,
    "TYPE": "IMAGE",
    "DESC": "CREDITOS",
    "WIDTH": 480,
    "START": "FINAL",
    "OFFSET RLE DEC": "UNKNOWN",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 256000
  }
]

direct = [
  {
  "start": 37000,
  "width": 45,
  "height": 87,
  "nframes": 3,
  },
  {
  "start": 48792,
  "width": 49,
  "height": 88,
  "nframes": 1
  },
  {
    "start": 53106,
    "width": 82,
    "height": 58,
    "nframes": 2
  },
  {
    "start": 1600956,
    "width": 208,
    "height": 102,
    "nframes": 7
  },
  {
    "start": 1770196,
    "width": 158,
    "height": 115,
    "nframes": 16
  },
  {
    "start": 2405266,
    "width": 640,
    "height": 400,
    "nframes": 1
  },
  {
    "start": 2532984,
    "width": 640,
    "height": 400,
    "nframes": 1
  },
  {
    "start": 3186048,
    "width": 20,
    "height": 20,
    "nframes": 2
  },
  {
    "start": 3187348,
    "width": 28,
    "height": 28,
    "nframes": 2
  },

  {
    "start": 212745,
    "width": 11,
    "height": 16,
    "nframes": 1
  }
]

raw = [
  {
    "start": 31876,
    "size": 324,
    "name": "unknown"
  },
  {
    "start": 0xBE69,
    "size": 0x2F,
    "name": "unknown"
  },
  {
    "start": 0xF49A,
    "size": 0x1414,
    "name": "unknown"
  },
  {
    "start": 0x308A2,
    "size": 0x13E,
    "name": "unknown"
  },
  {
    "start": 0x309E0,
    "size": 0x3526,
    "name": "libros"
  },
  {
    "start": 409885,
    "size": 1702,
    "name": "unknown"
  },
  {
    "start": 598731,
    "size": 176,
    "name": "unknown"
  },
  {
    "start": 1038909,
    "size": 672,
    "name": "code snippet"
  },
  {
    "start": 1039869,
    "size": 288,
    "name": "cursor1"
  },
  {
    "start": 1039581,
    "size": 288,
    "name": "cursor2"
  },
  {
    "start": 1040157,
    "size": 288,
    "name": "cursor3"
  },
  {
    "start": 1040445,
    "size": 768,
    "name": "palettemaybe"
  },
  {
    "start": 1041213,
    "size": 288,
    "name": "cursor4"
  },
  {
    "start": 3571440,
    "size": 288,
    "name": "cursor5"
  },
  {
    "start": 1047523,
    "size": 100,
    "name": "unknown"
  },
  {
    "start": 1361215,
    "size": 13593,
    "name": "englishBooks"
  },
  {
    "start": 1473192,
    "size": 172,
    "name": "unknown"
  },
  {
    "start": 3271454,
    "size": 256000,
    "name": "unknownimage"
  }
]


def decompress_rle(data, offset, end_offset):
    # size = end_offset - offset
    # if size == 0x8000 or size == 0x6800:
        # Uncompressed block - read directly
        # return data[offset:offset+size]
    result = bytearray()
    pos = offset
    while pos + 2 <= min(end_offset, len(data)):
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break
        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2
    return bytes(result)

def find_budas(data):
    budas = []
    # budas.append(0)
    pos = 0
    while pos < len(data) - 4:
        if data[pos:pos+4] == b'BUDA':
            budas.append(pos)
        pos += 1
    return budas

def is_valid_palette(data, offset):
    if offset + 768 > len(data):
        return False
    pal_data = data[offset:offset+768]
    return all(b <= 63 for b in pal_data) and len(set(pal_data)) > 10

def extract_palette(data, offset):
    pal_data = data[offset:offset+768]
    palette = []
    for i in range(256):
        r = min(255, pal_data[i * 3] * 4)
        g = min(255, pal_data[i * 3 + 1] * 4)
        b = min(255, pal_data[i * 3 + 2] * 4)
        palette.extend([r, g, b])
    return palette

def save_bytes_as_png(data, palette, name, width):
    size = 0
    if(width == 640):
        size =  640 * 400
        height = 400
        realHeight = height
    else:
        size = len(data)
        realHeight = size / width
        height = math.ceil(size / width)
    # Create image
    img_data = bytes(data[:size])
    if len(img_data) < size:
        img_data += bytes([0] * (size - len(img_data)))

    img = Image.new('P', (width, height))
    img.putpalette(palette)
    img.putdata(img_data)

    output_file = output_path_thisbuda / f'buda{budas[start_buda]["BUDA"]}_offset_{budas[start_buda] + budas[offset]}.png'
    img.save(output_file)
def main():
    alfred7 = sys.argv[1] if len(sys.argv) > 1 else "ALFRED.7"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "alfred7"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred7, 'rb') as f:
      data = f.read()

    # Extract raw entries as .bin files
    output_base_raw = Path(f'{output_dir}/raw')
    output_base_raw.mkdir(parents=True, exist_ok=True)
    for idx, entry in enumerate(raw):
        start_offset = entry["start"]
        size = entry["size"]
        name = entry.get("name", "noname")
        output_path_raw = output_base_raw / f'entry_{idx}_{start_offset}'
        output_path_raw.mkdir(parents=True, exist_ok=True)
        print(f'Extracting raw entry {idx}: offset={start_offset}, size={size}, name={name}')
        raw_data = data[start_offset:start_offset+size]
        output_file = output_path_raw / f'raw_{idx}_{name}_{start_offset}.bin'
        with open(output_file, 'wb') as f:
            f.write(raw_data)

    with open(alfred7, 'rb') as f:
        data = f.read()


    buda_offsets = find_budas(data)
    print(f"Found {len(buda_offsets)} BUDAs\n")

    # Find all palette BUDAs
    palettes = {}
    for i, buda_offset in enumerate(buda_offsets):
      if is_valid_palette(data, buda_offset + 4):
        palettes[i] = extract_palette(data, buda_offset + 4)
        print(f"BUDA {i}: palette")

    print(f"\nFound {len(palettes)} palettes\n")
    print("="*70)


# Extract direct entries first
    output_base_direct = Path(f'{output_dir}/direct')
    output_base_direct.mkdir(parents=True, exist_ok=True)

    for idx, entry in enumerate(direct):
        start_offset = entry["start"]
        width = entry["width"]
        height = entry["height"]
        nframes = entry.get("nframes", 1)

        # Find nearest palette
        pal_buda = 7  # Default
        for p_idx in palettes.keys():
            pal_buda = p_idx
            break

        palette_data = palettes[pal_buda]

        frame_size = width * height
        total_size = frame_size * nframes

        print(f"Direct entry {idx}: offset={start_offset}, w={width}, h={height}, frames={nframes}, size={total_size}")

        # Extract raw bytes directly
        raw_data = data[start_offset:start_offset + total_size]

        output_path_direct = Path(f'{output_base_direct}/entry_{idx}')
        output_path_direct.mkdir(parents=True, exist_ok=True)
        if nframes == 1:
            # Single frame
            img_data = bytes(raw_data)
            if len(img_data) < frame_size:
                img_data += bytes([0] * (frame_size - len(img_data)))

            img = Image.new('P', (width, height))
            img.putpalette(palette_data)
            img.putdata(img_data)

            output_file = output_path_direct / f'direct_{idx}_offset_{start_offset}.png'
            img.save(output_file)
        else:
            # Multiple frames
            for frame_idx in range(nframes):
                frame_start = frame_idx * frame_size
                frame_end = frame_start + frame_size
                frame_data = raw_data[frame_start:frame_end]

                img_data = bytes(frame_data)
                if len(img_data) < frame_size:
                    img_data += bytes([0] * (frame_size - len(img_data)))

                img = Image.new('P', (width, height))
                img.putpalette(palette_data)
                img.putdata(img_data)

                output_file = output_path_direct / f'direct_{idx}_frame_{frame_idx}_offset_{start_offset + frame_start}.png'
                img.save(output_file)


    for start_buda in range(len(budas) - 1):
      # Use the original 'budas' list for metadata, and 'buda_offsets' for file offsets
      start_offset = budas[start_buda]["START_OFFSET"]
      next_offset = budas[start_buda + 1]["START_OFFSET"]
      width =  budas[start_buda]["WIDTH"]
      isPalette = budas[start_buda]["isPalette"]
      isContinued = budas[start_buda]["isContinued"]
      type = budas[start_buda]["TYPE"]
      offset = budas[start_buda]["offset"]

      if start_buda>0 and budas[start_buda - 1]["isContinued"] == True:
        continue

      print(f'Decompressing {start_offset} to {next_offset}, width = {width}, isPalette = {isPalette}, offset = {offset}')

      combined = bytearray()

      if start_buda == 0:
         print(f'Adding block at 0')
         combined.extend(decompress_rle(data, 0, start_offset))

      block = decompress_rle(data, start_offset + 4 + offset, next_offset)
      combined.extend(block)

      curIndex = 0
      shouldContinue = isContinued
      totalBudas = 0

      if shouldContinue:
        curIndex = start_buda + 1
      if shouldContinue:
        while True:
          combined.extend(decompress_rle(data, budas[curIndex]["START_OFFSET"] + 4, budas[curIndex+1]["START_OFFSET"]))
          shouldContinue = budas[curIndex]["isContinued"]
          print(f'For buda = {start_buda} adding also buda {curIndex} (offset {budas[curIndex+1]["START_OFFSET"]})')
          curIndex+=1
          totalBudas +=1
          if(shouldContinue == False):
            break

      print(f'For buda = {start_buda} used {totalBudas}')

      output_path_thisbuda = Path(f'{output_dir}/buda{budas[start_buda]["BUDA"]}_{budas[start_buda]["DESC"]}')
      output_path_thisbuda.mkdir(parents=True, exist_ok=True)

      # Find nearest palette
      pal_buda = 1000
      for p_idx in palettes.keys():
        if p_idx > start_buda and p_idx < pal_buda:
          pal_buda = p_idx

      if pal_buda == 1000:
        print(f'Fallback palette')
        pal_buda = 7

      if type == "RAW":
          # Save decompressed data as .bin
          output_file = output_path_thisbuda / f'buda{budas[start_buda]["BUDA"]}_{budas[start_buda]["DESC"]}_offset_{start_offset}.bin'
          print(f"SAVING BUDA {budas[start_buda]['BUDA']}-{curIndex}: as raw")
          with open(output_file, 'wb') as f:
            f.write(combined)
      if pal_buda and type != "RAW":
        size = 0
        if(type == "IMAGE" and width == 640):
          size =  640 * 400
          height = 400
          realHeight = height
        else:
          size = len(combined)
          realHeight = size / width
          height = math.ceil(size / width)

        print(f"SAVING BUDA {budas[start_buda]['BUDA']}-{curIndex}: {len(combined)} bytes, palette {pal_buda}, w={width}, h={height}, realH={realHeight}")
        # Create image
        img_data = bytes(combined[:size])
        if len(img_data) < size:
          img_data += bytes([0] * (size - len(img_data)))

        img = Image.new('P', (width, height))
        img.putpalette(palettes[pal_buda])
        img.putdata(img_data)

        output_file = output_path_thisbuda / f'buda{budas[start_buda]["BUDA"]}_offset_{start_offset}.png'
        img.save(output_file)
        print(f"Saved image to {output_file}")

if __name__ == "__main__":
    main()
