"""Build the public playlist deterministically from checked-in sources and metadata."""
from __future__ import annotations
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
SOURCES = {"Odia": "o.m3u", "Doordarshan": "dd.m3u", "News": "n.m3u",
           "Music": "m.m3u", "Hindi Entertainment": "he.m3u", "Movies": "mo.m3u",
           "English Movies": "english_movies.m3u",
           "Kids": "k.m3u", "Sports": "spo.m3u", "Knowledge": "kno.m3u", "Lifestyle": "f.m3u"}
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
EPG_URL = "https://epgshare01.online/epgshare01/epg_ripper_IN1.xml.gz"

@dataclass
class Entry:
    name: str
    url: str
    attrs: dict = field(default_factory=dict)
    directives: list = field(default_factory=list)
    duration: str = "-1"


def normalize(name):
    name = re.sub(r"\([^)]*\)|\[[^]]*\]", "", name)
    name = re.sub(r"(?:@(?:HD|SD|4K)|\b(?:HD|SD|FHD|UHD|4K|HDR)\b)", "", name, flags=re.I)
    return re.sub(r"[^a-z0-9]", "", name.lower())


def split_info(line):
    quoted = False
    for i, char in enumerate(line):
        if char == '"': quoted = not quoted
        elif char == ',' and not quoted: return line[:i], line[i+1:].strip()
    raise ValueError("EXTINF requires a comma and channel name: " + line[:100])


def stream_url(line):
    return urlsplit(line.split('|', 1)[0]).scheme.lower() in {"http", "https", "rtmp", "rtsp", "udp"}


def parse(content, category=""):
    result, pending, directives = [], None, []
    for number, raw in enumerate(content.lstrip('\ufeff').splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#EXTM3U'): continue
        if line.startswith('#EXTINF:'):
            if pending is not None: raise ValueError(f"Line {number}: previous channel has no stream URL")
            pending, directives = line, []
        elif stream_url(line):
            if pending is None: raise ValueError(f"Line {number}: URL without EXTINF")
            info, name = split_info(pending)
            attrs = dict(ATTR.findall(info))
            if category: attrs['group-title'] = category
            result.append(Entry(name, line, attrs, directives, info.split(':', 1)[1].split()[0]))
            pending, directives = None, []
        elif pending is not None:
            if line.startswith('#'): directives.append(line)
            else: pending += ' ' + line  # continued EXTINF attributes / name
    if pending is not None: raise ValueError("Last channel has no stream URL")
    return result


def all_sources(root=ROOT):
    entries = []
    for category, filename in SOURCES.items():
        content = (root / 'sources' / filename).read_text(encoding='utf-8-sig')
        if not content.strip().startswith('#EXTM3U'): raise ValueError(f"Invalid source: {filename}")
        entries.extend(parse(content, category))
    return entries


def enrich(entry, metadata):
    key = entry.attrs.get('tvg-id', '').split('@')[0]
    info = metadata.get('by_id', {}).get(key, {})
    named = metadata.get('by_name', {}).get(entry.name, {})
    # A name-specific mapping preserves HD/SD guide variants of one channel.
    entry.attrs.update(info)
    entry.attrs.update(named)
    entry.attrs.setdefault('tvg-name', re.sub(r"\s*\([^)]*\)|\s*\[[^]]*\]", "", entry.name).strip())
    return entry


def render(entries):
    lines = [f'#EXTM3U x-tvg-url="{EPG_URL}" url-tvg="{EPG_URL}"']
    seen = set()
    for entry in entries:
        if entry.url in seen: continue
        seen.add(entry.url)
        attrs = ' '.join(f'{key}="{str(value).replace(chr(34), chr(39))}"' for key, value in sorted(entry.attrs.items()))
        lines.append(f'#EXTINF:{entry.duration} {attrs},{entry.name}')
        lines.extend(entry.directives)
        lines.append(entry.url)
    return '\n'.join(lines) + '\n'


def merge_playlists(root=ROOT):
    metadata_path = root / 'channel-metadata.json'
    metadata = json.loads(metadata_path.read_text(encoding='utf-8')) if metadata_path.exists() else {}
    entries = [enrich(entry, metadata) for entry in all_sources(root)]
    output = render(entries)
    if not parse(output): raise ValueError("Refusing to publish an empty playlist")
    target = root / 'merged.m3u'
    if not target.exists() or target.read_text(encoding='utf-8') != output:
        temporary = target.with_suffix('.m3u.tmp')
        temporary.write_text(output, encoding='utf-8', newline='\n')
        temporary.replace(target)
    print(f"Merged {len(parse(output))} unique streams ({len(entries)-len(parse(output))} exact duplicates removed)")
    return output


if __name__ == '__main__':
    merge_playlists()
