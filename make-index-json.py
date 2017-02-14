#!/usr/bin/env python3

import argparse
import glob
import json
import os.path
import subprocess
import sys

FFPROBE_ARGS = [
    'ffprobe',
    '-hide_banner',
    '-v', 'warning',
    '-show_format',
    '-of', 'json'
]

class Manifest:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            manifest = json.load(f)

            self.title = manifest.get('title', 'A Moxie Mixtape!')
            self.subtitle = manifest.get('subtitle', 'Make a manifest.json')
            self.url = manifest.get('url', 'http://github.com/quad/moxie')

class Tags:
    def __init__(self, filename):
        with subprocess.Popen(FFPROBE_ARGS + [filename], stdout=subprocess.PIPE) as ffprobe:
            data = ffprobe.stdout.read().decode()
            results = json.loads(data)

            self.basename = os.path.basename(filename)
            self.artist = results['format']['tags']['artist']
            self.title = results['format']['tags']['title']
            self.duration = float(results['format']['duration'])

def extract(source_directory):
    manifest_filename = os.path.join(source_directory, 'manifest.json')

    manifest = Manifest(manifest_filename)
    tags = [Tags(fn) for fn in glob.iglob(os.path.join(source_directory, '*.mp3'))]

    return manifest, tags

def transform(prefix, manifest, tags):
    return {
        'title': manifest.title,
        'subtitle': manifest.subtitle,
        'url': manifest.url,
        'tracks': [{'url': os.path.join(prefix, t.basename),
            'artist': t.artist,
            'title': t.title,
            'duration': t.duration}
            for t in tags],
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make a JSON index for moxie from a directory with .mp3 files and an (optional) manifest.json')
    parser.add_argument('--prefix', nargs='?', default='', help='prefix references with PATH', metavar='PATH')
    parser.add_argument('--output', nargs='?', default='index.json', help='output to FILE', metavar='FILE')
    parser.add_argument('source_directory', help='directory with .mp3 files')

    args = parser.parse_args()

    if not os.path.isdir(args.source_directory):
        raise Exception("{0} is not a directory".format(args.source_directory))

    with open(args.output, 'w') as f:
        json.dump(transform(args.prefix, *extract(args.source_directory)), f)
