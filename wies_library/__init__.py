# -*- coding: utf-8 -*-

import os
import random

from wies_library.colorprint import ColorPrint, ColorLog
from wies_library.datadriver import DataDriver

__all__ = ['ColorPrint', 'ColorLog', 'DataDriver']


def Random_pLay(FilePath):
    """
    传入音频文件夹或目录，随机返回文件名
    :param FilePath:
    :return:
    """
    files = [os.path.join(FilePath, f) for f in os.listdir(FilePath)]
    return random.choice(files)


def TextToSpeech(Txt, SpeechName, SpeechPath=None, SpeechType='mp3'):
    """
    传入文本，返回音频
    :param Txt:
    :param SpeechName:
    :param SpeechPath:
    :param SpeechType:
    :return:
    """
    if not SpeechPath:
        SpeechPath = './'

    SpeechName = f'{SpeechName}.{SpeechType}'
    Path = os.path.join(SpeechPath, SpeechName)
    cmd = f'edge-tts --text {Txt} --write-media {Path} --voice zh-CN-YunxiaNeural'
    os.system(cmd)
