from os.path import join, dirname

from audiobooker.scrappers.darkerprojects import DarkerProjects
from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_utils.parse import fuzzy_match, MatchStrategy
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search


class DarkerProjectsSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super(DarkerProjectsSkill, self).__init__("DarkerProjects")
        self.supported_media = [MediaType.GENERIC,
                                MediaType.RADIO_THEATRE,
                                MediaType.AUDIOBOOK]
        self.skill_icon = join(dirname(__file__), "ui", "logo.png")

    def calc_score(self, phrase, match, idx=0, base_score=0):
        # idx represents the order from search
        score = base_score - idx  # - 1% as we go down the results list
        score += 100 * fuzzy_match(phrase.lower(), match.lower(),
                                   strategy=MatchStrategy.TOKEN_SET_RATIO)
        return min(100, score)

    # common play
    @ocp_search()
    def search_episodes(self, phrase, media_type):
        # match the request media_type
        base_score = 0
        if media_type == MediaType.AUDIOBOOK:
            base_score += 25
        else:
            base_score -= 15

        if self.voc_match(phrase, "darkerproject"):
            # explicitly requested skill
            base_score += 60
            phrase = self.remove_voc(phrase, "darkerproject")

        loyalbooks = DarkerProjects()

        # free search
        results = loyalbooks.search_audiobooks(title=phrase)
        for idx, book in enumerate(results):
            score = self.calc_score(phrase, book.title, idx=idx,
                                    base_score=base_score)
            yield self._book2ocp(book, score)

    @ocp_search()
    def search_collections(self, phrase, media_type):
        # match the request media_type
        base_score = 0
        if media_type == MediaType.AUDIOBOOK:
            base_score += 25
        else:
            base_score -= 15

        if self.voc_match(phrase, "darkerproject"):
            # explicitly requested skill
            base_score += 60
            phrase = self.remove_voc(phrase, "darkerproject")

        loyalbooks = DarkerProjects()
        # see if collection title was requested
        for tag in loyalbooks.scrap_tags():
            score = self.calc_score(phrase, tag, base_score=base_score)
            if score >= 85:
                col = loyalbooks.get_collection(tag)
                yield self._book2ocp(col, score)

    def _book2ocp(self, book, score):
        author = "Darker Projects"
        pl = [{
            "match_confidence": score,
            "media_type": MediaType.AUDIOBOOK,
            "uri": s,
            "artist": author,
            "playback": PlaybackType.AUDIO,
            "image": self.skill_icon,
            "bg_image": self.skill_icon,
            "skill_icon": self.skill_icon,
            "title": str(book.title) + f" (Episode {ch + 1})",
            "skill_id": self.skill_id
        } for ch, s in enumerate(book.streams)]

        return {
            "match_confidence": score,
            "media_type": MediaType.AUDIOBOOK,
            "playback": PlaybackType.AUDIO,
            "playlist": pl,  # return full playlist result
            "length": book.runtime * 1000,
            "image": self.skill_icon,
            "artist": author,
            "bg_image": self.skill_icon,
            "skill_icon": self.skill_icon,
            "title": book.title,
            "skill_id": self.skill_id
        }


def create_skill():
    return DarkerProjectsSkill()
