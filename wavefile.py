#!/usr/bin/env python
#-*- coding: utf8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import struct


class WaveFile(object):
    """
    Wave file worker class
    """

    def __init__(self, sample_rate):
        self.subchunk_size = 16   # subchunk data size (16 for PCM)
        self.compression_type = 1 # compression (PCM = 1 [linear quantization])
        self.channels_num = 1     # channels (mono = 1, stereo = 2)
        self.bits_per_sample = 16
        self.block_alignment = self.channels_num * self.bits_per_sample / 8
        self.sample_rate = sample_rate
        self.byte_rate = self.sample_rate * self.channels_num * self.bits_per_sample / 8
        self.duration = 0
        self.data = []

    def add_data_subchunk(self, duration, data):
        self.duration += duration
        self.data += data

    def save(self, filename):
        self.samples_num = int(self.duration * self.sample_rate)
        self.subchunk2_size = self.samples_num * self.channels_num * self.bits_per_sample / 8
        with open(filename, 'wb') as f:
            # write RIFF header
            f.write(bytes('RIFF', 'UTF-8'))
            length = 4 + (8 + self.subchunk_size) + (8 + self.subchunk2_size)
            f.write(struct.pack('<i', int(length)))
            f.write(bytes('WAVE', 'UTF-8'))
            # write fmt subchunk
            f.write(bytes('fmt ', 'UTF-8'))                                     # chunk type
            f.write(struct.pack('<i', int(self.subchunk_size))  )    # data size
            f.write(struct.pack('<h', int(self.compression_type)))   # compression type
            f.write(struct.pack('<h', int(self.channels_num))   )    # channels
            f.write(struct.pack('<i', int(self.sample_rate))    )    # sample rate
            f.write(struct.pack('<i', int(self.byte_rate))      )    # byte rate
            f.write(struct.pack('<h', int(self.block_alignment)))    # block alignment
            f.write(struct.pack('<h', int(self.bits_per_sample)))    # sample depth
            # write data subchunk
            f.write(bytes('data', 'UTF-8'))
            f.write(struct.pack ('<i', int(self.subchunk2_size)))
            for d in self.data:
                sound_data = struct.pack('<h', d)
                f.write(sound_data)
