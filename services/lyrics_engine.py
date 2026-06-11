

class LyricsEngine:

    def __init__(self):
        self.lyrics = []
        self.index = 0
    # LOAD PARSED LYRICS
    def set_lyrics(self, lyrics):

        self.lyrics = lyrics

    # FIND CURRENT LINE
    def get_current_lines(self, current_time):

        if not self.lyrics:
            return "", "No Lyrics", ""

        current_index = 0

        # =====================================================
        # FIND CURRENT LINE
        # =====================================================

        for i, entry in enumerate(self.lyrics):

            # NORMAL TEXT MODE
            if isinstance(entry, str):

                current_index = i
                break

            # TIMED LYRICS MODE
            else:

                timestamp, line = entry

                if current_time >= timestamp:
                    current_index = i

        # =====================================================
        # PREVIOUS LINE
        # =====================================================

        previous_line = ""

        if current_index > 0:

            prev_entry = self.lyrics[current_index - 1]

            if isinstance(prev_entry, str):
                previous_line = prev_entry
            else:
                previous_line = prev_entry[1]

        # =====================================================
        # CURRENT LINE
        # =====================================================

        current_entry = self.lyrics[current_index]

        if isinstance(current_entry, str):
            current_line = current_entry
        else:
            current_line = current_entry[1]

        # =====================================================
        # NEXT LINE
        # =====================================================

        next_line = ""

        if current_index < len(self.lyrics) - 1:

            next_entry = self.lyrics[current_index + 1]

            if isinstance(next_entry, str):
                next_line = next_entry
            else:
                next_line = next_entry[1]

        return (
            previous_line,
            current_line,
            next_line
        )