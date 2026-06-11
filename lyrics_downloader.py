import os
import syncedlyrics

from metadata_utils import get_song_metadata


# ==========================================
# DOWNLOAD LRC
# ==========================================

def download_lrc(mp3_path):

    # --------------------------------------
    # GET METADATA
    # --------------------------------------

    meta = get_song_metadata(mp3_path)

    artist = meta["artist"]
    title = meta["title"]

    # --------------------------------------
    # SEARCH QUERY
    # --------------------------------------

    query = f"{artist} {title}"

    print("\nSearching:", query)

    # --------------------------------------
    # SEARCH ONLINE
    # --------------------------------------

    lyrics = syncedlyrics.search(
        query,
        synced_only=True
    )

    # --------------------------------------
    # FOUND
    # --------------------------------------

    if lyrics:

        base = os.path.splitext(mp3_path)[0]

        lrc_path = base + ".lrc"

        with open(
            lrc_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(lyrics)

        print("Saved:", lrc_path)

        return True

    # --------------------------------------
    # NOT FOUND
    # --------------------------------------

    print("No synced lyrics found.")

    return False