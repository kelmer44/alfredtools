#!/usr/bin/env python3
"""
Systematically extract BUDA ranges to find 640x400 screens
"""

import sys
from pathlib import Path
import math
from PIL import Image

metadata = [
#   {
#     "BUDA": 0,
#     "OFFSET": 0,
#     "TYPE": "IMAGE",
#     "DESC": "CUADROCAMA",
#     "WIDTH": 640,
#     "offset": 0,
#     "START": "0",
#     "OFFSET RLE DEC": "COMPLETO",
#     "isPalette" : False,
#     "isContinued":  True,
	# "offset" : 0,
#   },
  {
    "BUDA": 0,
    "OFFSET": 260,
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
    "OFFSET": 680,
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
    "OFFSET": 11150,
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
    "OFFSET": 17616,
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
    "OFFSET": 22598,
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
    "OFFSET": 28766,
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
    "OFFSET": 30890,
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
    "OFFSET": 31104,
    "TYPE": "ANIM",
    "DESC": "ALFRED PEINANDO DERECHA",
    "WIDTH": 51,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
    "blockList" : [
        {
            "offset" : 0,
            "type": "PALETTE",
        },
        {
            "offset" : 768,
            "type" : "UNKNOWN",
        },
        {
            "offset" : 5895,
            "type": "RAW",
            "width": 45
        },
        {
            "offset" : 17738,
            "type": "RAW",
            "width": 49
        },
        {
            "offset" : 22002,
            "type": "RAW",
            "width": 82
        },
        {
            "offset" : 31842,
            "type": "RAW",
            "width": 86
        },
        {
            "offset" : 36650,
            "type": "RAW",
            "width": 49
        },
    ],
	"offset" : 36650
  },
  {
    "BUDA": 8,
    "OFFSET": 88404,
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
    "OFFSET": 109034,
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
    "OFFSET": 112386,
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
    "OFFSET": 132440,
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
    "OFFSET": 139082,
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
    "OFFSET": 145736,
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
    "OFFSET": 152472,
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
    "OFFSET": 170502,
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
    "OFFSET": 192176,
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
    "OFFSET": 198046,
    "TYPE": "?",
    "DESC": "?",
    "WIDTH": 1,
    "START": "?",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 18,
    "OFFSET": 236641,
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
    "OFFSET": 261445,
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
    "OFFSET": 280355,
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
    "OFFSET": 298585,
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
    "OFFSET": 341225,
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
    "OFFSET": 360833,
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
    "OFFSET": 381445,
    "TYPE": "ANIM",
    "DESC": "LLAMA?",
    "WIDTH": 7,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 25,
    "OFFSET": 381821,
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
    "OFFSET": 397661,
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
    "OFFSET": 398559,
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
    "OFFSET": 409881,
    "TYPE": "IMAGE",
    "DESC": "ALFRED CIRCULO",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 1702
  },
  {
    "BUDA": 29,
    "OFFSET": 422789,
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
    "OFFSET": 432769,
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
    "OFFSET": 448051,
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
    "OFFSET": 457673,
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
    "OFFSET": 460449,
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
    "OFFSET": 466747,
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
    "OFFSET": 475631,
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
    "OFFSET": 482397,
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
    "OFFSET": 488721,
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
    "OFFSET": 494743,
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
    "OFFSET": 503189,
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
    "OFFSET": 505517,
    "TYPE": "IMAGE",
    "DESC": "DAILY",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  True,
	"offset" : 864
  },
  {
    "BUDA": 41,
    "OFFSET": 506841,
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
    "OFFSET": 511013,
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
    "OFFSET": 513977,
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
    "OFFSET": 517677,
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
    "OFFSET": 529943,
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
    "OFFSET": 544723,
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
    "OFFSET": 556911,
    "TYPE": "?",
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
    "OFFSET": 558009,
    "TYPE": "ANIM",
    "DESC": "?",
    "WIDTH": 1,
    "START": "?",
    "OFFSET RLE DEC": "?",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 49,
    "OFFSET": 558913,
    "TYPE": "ANIM",
    "DESC": "ALFRED LEE",
    "WIDTH": 51,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  True,
	  "offset" : 768
  },
  {
    "BUDA": 50,
    "OFFSET": 578939,
    "TYPE": "SPRITE",
    "DESC": "ALFRED LEE",
    "WIDTH": 51,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 51,
    "OFFSET": 598047,
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
    "OFFSET": 598727,
    "TYPE": "IMAGE",
    "DESC": "TABLA",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : False,
    "isContinued":  True,
	  "offset" : 176
  },
  {
    "BUDA": 53,
    "OFFSET": 604459,
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
    "OFFSET": 623131,
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
    "OFFSET": 642223,
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
    "OFFSET": 661561,
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
    "OFFSET": 679733,
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
    "OFFSET": 698901,
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
    "OFFSET": 718261,
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
    "OFFSET": 724707,
    "TYPE": "IMAGE",
    "DESC": "MAPA",
    "WIDTH": 640,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  True,
	  "offset" : 778
  },
  {
    "BUDA": 61,
    "OFFSET": 749285,
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
    "OFFSET": 778259,
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
    "OFFSET": 807535,
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
    "OFFSET": 834765,
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
    "OFFSET": 855439,
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
    "OFFSET": 873425,
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
    "OFFSET": 894345,
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
    "OFFSET": 909325,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  True,
	"offset" : 768
  },
  {
    "BUDA": 69,
    "OFFSET": 918951,
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
    "OFFSET": 942699,
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
    "OFFSET": 956557,
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
    "OFFSET": 973643,
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
    "OFFSET": 986445,
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
    "OFFSET": 1006481,
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
    "OFFSET": 1030041,
    "TYPE": "?",
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
    "OFFSET": 1038137,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 201,
    "START": "?",
    "OFFSET RLE DEC": "?",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 77,
    "OFFSET": 1042753,
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
    "OFFSET": 1047519,
    "TYPE": "IMAGE",
    "DESC": "LIBRO",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : False,
    "isContinued":  True,
	 "offset" : 100
  },
  {
    "BUDA": 79,
    "OFFSET": 1050483,
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
    "OFFSET": 1070619,
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
    "OFFSET": 1090115,
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
    "OFFSET": 1103745,
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
    "OFFSET": 1119391,
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
    "OFFSET": 1134469,
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
    "OFFSET": 1144071,
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
    "OFFSET": 1147077,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 640,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  True,
	  "offset" : 768
  },
  {
    "BUDA": 87,
    "OFFSET": 1155375,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	  "offset" : 0
  },
  {
    "BUDA": 88,
    "OFFSET": 1174169,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 89,
    "OFFSET": 1190857,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 90,
    "OFFSET": 1206407,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 91,
    "OFFSET": 1221291,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 92,
    "OFFSET": 1236715,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 93,
    "OFFSET": 1262291,
    "TYPE": "SPRITEMAP",
    "DESC": "?",
    "WIDTH": 640,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 94,
    "OFFSET": 1267951,
    "TYPE": "IMAGE",
    "DESC": "SIMBOLOS",
    "WIDTH": 119,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 768
  },
  {
    "BUDA": 95,
    "OFFSET": 1341231,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 119,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 96,
    "OFFSET": 1347763,
    "TYPE": "?",
    "DESC": "NaN",
    "WIDTH": 146,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 97,
    "OFFSET": 1361211,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 201,
    "START": "?",
    "OFFSET RLE DEC": "?",
    "isPalette" : "?",
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 98,
    "OFFSET": 1387140,
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
    "OFFSET": 1387404,
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
    "OFFSET": 1388712,
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
    "OFFSET": 1396422,
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
    "OFFSET": 1402748,
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
    "OFFSET": 1409456,
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
    "OFFSET": 1419432,
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
    "OFFSET": 1425134,
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
    "OFFSET": 1425348,
    "TYPE": "MULTIANIM",
    "DESC": "ALFREDCAMA",
    "WIDTH": 76,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 107,
    "OFFSET": 1446090,
    "TYPE": "ANIM",
    "DESC": "NADADORAS",
    "WIDTH": 93, #68, 79, 54,
    "START": "FINAL (After palette)",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 768
  },
  {
    "BUDA": 108,
    "OFFSET": 1473188,
    "TYPE": "ANIM",
    "DESC": "TIPOS BEBIENDO",
    "WIDTH": 152,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 172
  },
  {
    "BUDA": 109,
    "OFFSET": 1512056,
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
    "OFFSET": 1526428,
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
    "OFFSET": 1556536,
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
    "OFFSET": 1583698,
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
    "OFFSET": 1600952,
    "TYPE": "ANIM",
    "DESC": "ALFREDAGACHA",
    "WIDTH": 95,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 0
  },
  {
    "BUDA": 114,
    "OFFSET": 1761230,
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
    "OFFSET": 1766374,
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
    "OFFSET": 1770192,
    "TYPE": "ANIM",
    "DESC": "ALFREDMUNHECO",
    "WIDTH": 116,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 290730
  },
  {
    "BUDA": 117,
    "OFFSET": 2115628,
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
    "OFFSET": 2176932,
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
    "OFFSET": 2201878,
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
    "OFFSET": 2208282,
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
    "OFFSET": 2210444,
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
    "OFFSET": 2212842,
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
    "OFFSET": 2214704,
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
    "OFFSET": 2214756,
    "TYPE": "IMAGE",
    "DESC": "?",
    "WIDTH": 213,
    "START": "0",
    "OFFSET RLE DEC": "COMPLETO",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 125,
    "OFFSET": 2227414,
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
    "OFFSET": 2227678,
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
    "OFFSET": 2227942,
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
    "OFFSET": 2228206,
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
    "OFFSET": 2228470,
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
    "OFFSET": 2228734,
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
    "OFFSET": 2228998,
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
    "OFFSET": 2229262,
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
    "OFFSET": 2229476,
    "TYPE": "ANIM",
    "DESC": "PALETTE",
    "WIDTH": 1,
    "START": "NaN",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 134,
    "OFFSET": 2230262,
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
    "OFFSET": 2253652,
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
    "OFFSET": 2258828,
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
    "OFFSET": 2262630,
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
    "OFFSET": 2264882,
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
    "OFFSET": 2266764,
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
    "OFFSET": 2268656,
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
    "OFFSET": 2275860,
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
    "OFFSET": 2284460,
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
    "OFFSET": 2284674,
    "TYPE": "ANIM",
    "DESC": "PALETTE",
    "WIDTH": 20,
    "START": "NaN",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 768
  },
  {
    "BUDA": 144,
    "OFFSET": 2285690,
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
    "OFFSET": 2306534,
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
    "OFFSET": 2306798,
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
    "OFFSET": 2307118,
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
    "OFFSET": 2311128,
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
    "OFFSET": 2317890,
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
    "OFFSET": 2320318,
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
    "OFFSET": 2320582,
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
    "OFFSET": 2320846,
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
    "OFFSET": 2321060,
    "TYPE": "IMAGE",
    "DESC": "CODE",
    "WIDTH": 640,
    "START": "AFTER PALETTE",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
	  "offset" : 768
  },
  {
    "BUDA": 154,
    "OFFSET": 2361384,
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
    "OFFSET": 2381078,
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
    "OFFSET": 2405262,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : False,
    "isContinued":  True,
	"offset" : 0
  },
  {
    "BUDA": 157,
    "OFFSET": 2500216,
    "TYPE": "IMAGE",
    "DESC": "MENU",
    "WIDTH": 640,
    "START": "NaN",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : False,
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 158,
    "OFFSET": 2563262,
    "TYPE": "SPRITE",
    "DESC": "MENU?",
    "WIDTH": 640,
    "START": "?",
    "OFFSET RLE DEC": "?",
    "isPalette" : "?",
    "isContinued":  False,
	"offset" : 0
  },
  {
    "BUDA": 159,
    "OFFSET": 2662584,
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
    "OFFSET": 2664742,
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
    "OFFSET": 2667136,
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
    "OFFSET": 2668994,
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
    "OFFSET": 2669046,
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
    "OFFSET": 2688164,
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
    "OFFSET": 2727560,
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
    "OFFSET": 2727824,
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
    "OFFSET": 2742300,
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
    "OFFSET": 2767184,
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
    "OFFSET": 2787502,
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
    "OFFSET": 2808956,
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
    "OFFSET": 2830578,
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
    "OFFSET": 2833058,
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
    "OFFSET": 2833272,
    "TYPE": "IMAGE",
    "DESC": "PERGAMINO",
    "WIDTH": 640,
    "START": "AFTER PALETTE",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  True,
	"offset" : 768
  },
  {
    "BUDA": 174,
    "OFFSET": 2834304,
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
    "OFFSET": 2857816,
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
    "OFFSET": 2881590,
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
    "OFFSET": 2911516,
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
    "OFFSET": 2941462,
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
    "OFFSET": 2969166,
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
    "OFFSET": 2971582,
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
    "OFFSET": 2971796,
    "TYPE": "SPRITE",
    "DESC": "ALFREDDESCAMISA",
    "WIDTH": 51,
    "START": "AFTER PALETTE",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
	"offset" : 768
  },
  {
    "BUDA": 182,
    "OFFSET": 2980868,
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
    "OFFSET": 3006790,
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
    "OFFSET": 3037004,
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
    "OFFSET": 3038450,
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
    "OFFSET": 3058222,
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
    "OFFSET": 3066050,
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
    "OFFSET": 3075630,
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
    "OFFSET": 3094642,
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
    "OFFSET": 3123460,
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
    "OFFSET": 3143534,
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
    "OFFSET": 3165032,
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
    "OFFSET": 3179630,
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
    "OFFSET": 3185276,
    "TYPE": "ANIMS",
    "DESC": "PIERNAS, MANOS",
    "WIDTH": 114,
    # 55,
    "START": "MEDIO",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : True,
    "isContinued":  False,
	   "offset" : 36970
  },
  {
    "BUDA": 195,
    "OFFSET": 3271450,
    "TYPE": "IMAGE",
    "DESC": "CREDITOS",
    "WIDTH": 480,
    "START": "FINAL",
    "OFFSET RLE DEC": "NaN",
    "isPalette" : False,
    "isContinued":  False,
	  "offset" : 256000
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

    output_file = output_path_thisbuda / f'buda{start_buda:03d}_offset_{budas[start_buda]}.png'
    img.save(output_file)
def main():
    alfred7 = sys.argv[1] if len(sys.argv) > 1 else "ALFRED.7"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "alfred7"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred7, 'rb') as f:
        data = f.read()

    budas = find_budas(data)
    print(f"Found {len(budas)} BUDAs\n")

    # Find all palette BUDAs
    palettes = {}
    for i, buda in enumerate(budas):
        if is_valid_palette(data, buda + 4):
            palettes[i] = extract_palette(data, buda + 4)
            print(f"BUDA {i}: palette")

    print(f"\nFound {len(palettes)} palettes\n")
    print("="*70)


    for start_buda in range(len(budas) - 1):
        # Skip palette BUDAs
        # real_start = start_buda


        # for i in range(start_buda, min(real_start + 20, len(budas) - 1)):
        #     if i in palettes:
        #         # Found a palette, stop here
        #         break
        # real_start = budas[start_buda] if isPalette else budas[start_buda] + 768
        width =  metadata[start_buda]["WIDTH"]
        isPalette = metadata[start_buda]["isPalette"]
        isContinued = metadata[start_buda]["isContinued"]
        type = metadata[start_buda]["TYPE"]
        offset = metadata[start_buda]["offset"]

        if start_buda>0 and metadata[start_buda - 1]["isContinued"] == True:
            continue

        print(f'Decompressing {budas[start_buda]} to {budas[start_buda + 1]}, width = {width}, isPalette = {isPalette}, offset = {offset}')

        combined = bytearray()

        if start_buda == 0:
             print(f'Adding block at 0')
             combined.extend(decompress_rle(data, 0, budas[start_buda]))

        block = decompress_rle(data, budas[start_buda] + 4 + offset, budas[start_buda+1])
        combined.extend(block)

        curIndex = 0
        shouldContinue = isContinued
        totalBudas = 0

        if shouldContinue:
            curIndex = start_buda + 1
        if shouldContinue:
            while True:
                combined.extend(decompress_rle(data, budas[curIndex] + 4, budas[curIndex+1]))
                shouldContinue = metadata[curIndex]["isContinued"]
                print(f'For buda = {start_buda} adding also buda {curIndex}')
                curIndex+=1
                totalBudas +=1
                if(shouldContinue == False):
                    break

        print(f'For buda = {start_buda} used {totalBudas}')


        output_path_thisbuda = Path(f'{output_dir}/buda{start_buda:03d}')
        output_path_thisbuda.mkdir(parents=True, exist_ok=True)

        # Find nearest palette
        pal_buda = 1000
        for p_idx in palettes.keys():
            if p_idx > start_buda and p_idx < pal_buda: # and p_idx <= start_buda + budas_used + 10:
                pal_buda = p_idx

        if pal_buda == 1000:
            print(f'Fallback palette')
            pal_buda = 7

        if pal_buda:
            size = 0
            if(type == "IMAGE" and width == 640):
                size =  640 * 400
                height = 400
                realHeight = height
            else:
                size = len(combined)
                realHeight = size / width
                height = math.ceil(size / width)
            print(f"SAVING BUDA {start_buda}-{curIndex}: {len(combined)} bytes, palette {pal_buda}, w={width}, h={height}, realH={realHeight}")
            # Create image
            img_data = bytes(combined[:size])
            if len(img_data) < size:
                img_data += bytes([0] * (size - len(img_data)))

            img = Image.new('P', (width, height))
            img.putpalette(palettes[pal_buda])
            img.putdata(img_data)

            output_file = output_path_thisbuda / f'buda{start_buda:03d}_offset_{budas[start_buda]}.png'
            img.save(output_file)

if __name__ == "__main__":
    main()
