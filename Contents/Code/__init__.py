# local media assets agent

import mutagen
import json


# noinspection PyPep8Naming
def Start():
    Log('PRISM START')


class LocalMediaAlbum(Agent.Album):
    name = 'Prism'
    languages = [Locale.Language.NoLanguage]
    primary_provider = False
    persist_stored_files = False
    contributes_to = ['com.plexapp.agents.discogs', 'com.plexapp.agents.lastfm', 'com.plexapp.agents.plexmusic',
                      'com.plexapp.agents.none']

    def search(self, results, media, lang):
        pass

    def update(self, metadata, media, lang):
        update_album(metadata, media)


def parse_tags(track):
    # TODO: error handling
    return mutagen.File(track.file).tags


def update_album(metadata, media):
    Log("UPDATE ALBUM")

    tracks = media.children

    items = [parse_tags(part)
             for track in tracks
             for item in track.items
             for part in item.parts]

    assert(len(tracks) == len(items))

    data = {
        'version': 1,
        'items': [
            {
                # Identifier
                'id': track.id,

                # Composers
                'composers': [composers
                              for tag in item.getall('TCOM')
                              for composers in tag.text]
            }
            for track, item in zip(tracks, items)]
    }

    s = json.dumps(data)
    metadata.studio = s
    Log(s)
