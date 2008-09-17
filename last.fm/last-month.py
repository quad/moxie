#!/usr/bin/env python

import urllib
import xml.etree.ElementTree as ET

api_key = '068e57ae9465c496f8c4ceecdc4ca644'

def lfm_call(method, **kwargs):
    url = "http://ws.audioscrobbler.com/2.0/?method=%s&%s&api_key=%s" % (method,
                                                                         urllib.urlencode(kwargs),
                                                                         api_key)

    result = urllib.urlopen(url)

    return ET.parse(result)

def main():
    # Pull down the last five weekly charts indexes.

    charts_xml = lfm_call('user.getWeeklyChartList', user = 'quad')

    last_five_charts = [(chart.attrib['from'], chart.attrib['to'])
                        for chart in charts_xml.find('weeklychartlist')
                                               .findall('chart')[-5:]]

    # Download the last five weekly chart playcounts.

    tracks_xml = [lfm_call('user.getweeklytrackchart',
                           **{'from': time_from,
                              'to': time_to,
                              'user': 'quad'}).find('weeklytrackchart')
                                              .findall('track')
                  for time_from, time_to in last_five_charts]

    # Parse the weekly charts for their artist, title, and playcount.

    parsed_tracks = [dict([((track.find('artist').text, track.find('name').text),
                            int(track.find('playcount').text))
                           for track in tracks])
                     for tracks in tracks_xml]

    # Combine the weekly charts.

    def combine_tracks(source, victim):
        for index, playcount in source.items():
            victim[index] = victim.get(index, 0) + playcount

        return victim

    top_tracks = sorted([(playcount, index)
                         for index, playcount in reduce(combine_tracks, parsed_tracks).items()])

    for playcount, index in reversed(top_tracks[-10:]):
        print playcount, index

if __name__ == '__main__':
    main()
