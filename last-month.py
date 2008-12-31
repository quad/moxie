#!/usr/bin/env python

import operator
import urllib
import xml.etree.ElementTree as ET

api_key = '068e57ae9465c496f8c4ceecdc4ca644'

def lfm_call(method, **kwargs):
    url = "http://ws.audioscrobbler.com/2.0/?method=%s&%s&api_key=%s" % \
            (method,
             urllib.urlencode(kwargs),
             api_key)

    result = urllib.urlopen(url)

    return ET.parse(result)

def main():
    # Pull down the last four weekly charts indexes.

    charts_xml = lfm_call('user.getWeeklyChartList', user = 'quad')

    last_four_charts = [(chart.attrib['from'], chart.attrib['to'])
                        for chart in charts_xml.find('weeklychartlist')
                                               .findall('chart')[-4:]]

    # Download the last four weekly chart playcounts.
    tracks_xml = [lfm_call('user.getweeklytrackchart',
                           **{'from': time_from,
                              'to': time_to,
                              'user': 'quad'}).find('weeklytrackchart')
                                              .findall('track')
                  for time_from, time_to in last_four_charts]

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

    top_tracks = sorted(reduce(combine_tracks, parsed_tracks).iteritems(),
                        key = operator.itemgetter(1),
                        reverse = True)

    # Max out on three tracks per artist.

    def limit_artists(tracks, max_appearance):
        selected_artists = {}

        for index, playcount in tracks:
            artist, title = index

            selected_artists[artist] = selected_artists.get(artist, 0) + 1

            if (selected_artists[artist] <= max_appearance):
                yield artist, title

    for artist, title in list(limit_artists(top_tracks, 2))[:20]:
        print artist, title

if __name__ == '__main__':
    main()
