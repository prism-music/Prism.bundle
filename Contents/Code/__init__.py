# local media assets agent

import audiohelpers
import config
import helpers
import localmedia
import mutagen


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
        results.Append(MetadataSearchResult(id='null', score=100))

    def update(self, metadata, media, lang):
        update_album(metadata, media, lang)


def add_album_image(meta_set, meta_type, data_file, root_file, data, digest):
    if digest not in meta_set:
        meta_set[digest] = Proxy.Media(data)
        Log('Local asset image added (%s): %s, for file: %s', meta_type, data_file, root_file)
    else:
        Log("Skipping local %s since it's already added", meta_type)


def parse_tags(track):
    # TODO: error handling
    return mutagen.File(track.file).tags


def update_album(metadata, media, lang):
    Log("UPDATE ALBUM")
    Log(media.title)

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

    Log(data)
