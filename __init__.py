from os.path import join, dirname

import requests
from ovos_utils.parse import fuzzy_match
from ovos_utils.xml_helper import xml2dict
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    MediaType, PlaybackType, ocp_search


class SomaFmStation:
    def __init__(self, raw):
        self.raw = raw

    @property
    def station_id(self):
        return self.raw.get("id")

    @property
    def title(self):
        return self.raw.get("title") or self.station_id

    @property
    def image(self):
        return self.raw.get("xlimage") or \
               self.raw.get("largeimage") or \
               self.raw.get("image")

    @property
    def description(self):
        return self.raw.get("description", "")

    @property
    def genre(self):
        return self.raw.get("genre")

    @property
    def pls_stream(self):
        return f"http://somafm.com/m3u/{self.station_id}.pls"

    @property
    def m3u_stream(self):
        return f"http://somafm.com/m3u/{self.station_id}.m3u"

    @property
    def direct_stream(self):
        return f"http://ice2.somafm.com/{self.station_id}-128-mp3"

    @property
    def alt_direct_stream(self):
        return f"http://ice4.somafm.com/{self.station_id}-128-mp3"

    @property
    def streams(self):
        streams = []
        for stream in self.raw.get("fastpls", []):
            try:
                streams.append(stream["text"])
            except:
                continue
        for stream in self.raw.get("highestpls", []):
            try:
                streams.append(stream["text"])
            except:
                continue
        return streams

    @property
    def best_stream(self):
        for stream in self.raw.get("highestpls", []):
            try:
                return stream["text"]
            except:
                continue
        for stream in self.raw.get("fastpls", []):
            try:
                return stream["text"]
            except:
                continue

    @property
    def fastest_stream(self):
        for stream in self.raw.get("fastpls", []):
            try:
                return stream["text"]
            except:
                continue
        for stream in self.raw.get("highestpls", []):
            try:
                return stream["text"]
            except:
                continue

    def __str__(self):
        return self.fastest_stream

    def __repr__(self):
        return self.title + ":" + str(self)


class SomaFMSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super().__init__("SomaFM")
        self.supported_media = [MediaType.GENERIC,
                                MediaType.MUSIC,
                                MediaType.RADIO]
        self.skill_icon = join(dirname(__file__), "ui", "somafm.png")

    @staticmethod
    def get_stations():
        xml = requests.get("http://api.somafm.com/channels.xml").text
        for channel in xml2dict(xml)["channels"]["channel"]:
            yield SomaFmStation(channel)

    @ocp_search()
    def search_somafm(self, phrase, media_type):
        base_score = 0

        if media_type == MediaType.RADIO:
            base_score += 20
        elif media_type == MediaType.MUSIC:
            base_score += 10

        if self.voc_match(phrase, "somafm"):
            base_score += 70  # explicit request
            phrase = self.remove_voc(phrase, "somafm")

        for ch in self.get_stations():
            score = base_score + \
                    fuzzy_match(ch.title.lower(), phrase.lower()) * 100
            yield {
                "match_confidence": min(100, score),
                "media_type": MediaType.RADIO,
                "uri": ch.direct_stream,
                "playback": PlaybackType.AUDIO,
                "image": ch.image,
                "bg_image": ch.image,
                "skill_icon": self.skill_icon,
                "skill_logo": self.skill_icon,
                "title": ch.title,
                "author": "SomaFM",
                "length": 0
            }


def create_skill():
    return SomaFMSkill()
