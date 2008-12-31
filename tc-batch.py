#!/usr/bin/env python

import fileinput
import logging

import moxie.transcode

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)

    transcoders = [moxie.transcode.Transcoder(fn.strip(), '%.2u.mp3' % tracknum)
                   for tracknum, fn in enumerate(fileinput.input())]

    for t in transcoders:
        t.run()
