"""Build a small, explicitly mapped XMLTV guide; preserve last good output on failure."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import gzip
import io
import json
from pathlib import Path
import sys
import tempfile
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import merge_m3u

def xml_time(value):
    return datetime.strptime(value.strip(), '%Y%m%d%H%M%S %z').astimezone(timezone.utc)

def source_programmes(data, channel_map, now):
    if data[:2] == b'\x1f\x8b':
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
            data = stream.read(256 * 1024 * 1024 + 1)
    if len(data) > 256 * 1024 * 1024:
        raise ValueError('Guide exceeds decompressed size limit')
    if b'<!DOCTYPE' in data or b'<!ENTITY' in data:
        raise ValueError('DTD/entity declarations are not supported')
    result = []
    for event, element in ET.iterparse(io.BytesIO(data), events=('end',)):
        if element.tag == 'programme':
            targets = channel_map.get(element.get('channel'), [])
            if targets:
                try:
                    start, stop = xml_time(element.get('start', '')), xml_time(element.get('stop', ''))
                except (ValueError, TypeError):
                    raise ValueError('Invalid mapped programme time')
                if stop > start and stop > now - timedelta(hours=4) and start < now + timedelta(days=8) and element.findtext('title', '').strip():
                    for target in targets:
                        copy = deepcopy(element)
                        copy.set('channel', target)
                        result.append(copy)
            element.clear()
        elif element.tag == 'channel':
            element.clear()
    return result

def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temp = Path(stream.name)
        stream.write(data)
    try:
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)

def build(config, fetch, now=None):
    now = now or datetime.now(timezone.utc)
    mappings = config['channels']
    grouped = defaultdict(lambda: defaultdict(list))
    for target, item in mappings.items():
        if not target or not item['source_channel']:
            raise ValueError('Guide IDs must not be blank')
        grouped[item['source']][item['source_channel']].append(target)
    programmes = []
    for source, channel_map in sorted(grouped.items()):
        programmes.extend(source_programmes(fetch(source), channel_map, now))
    unique = {}
    for p in programmes:
        key = (p.get('channel'), p.get('start'), p.get('stop'), p.findtext('title'))
        unique[key] = p
    programmes = sorted(unique.values(), key=lambda p: (p.get('channel'), xml_time(p.get('start')), p.findtext('title', '')))
    future = Counter(p.get('channel') for p in programmes if xml_time(p.get('stop')) > now)
    if not mappings or len(future) < max(1, len(mappings) * 0.8):
        raise ValueError('Guide lost more than 20% of mapped channels; preserve previous guide')
    tv = ET.Element('tv', {'generator-info-name': 'Home TV mapped public guides'})
    for target in sorted(future):
        channel = ET.SubElement(tv, 'channel', {'id': target})
        ET.SubElement(channel, 'display-name').text = mappings[target]['name']
    for programme in programmes:
        if programme.get('channel') in future:
            tv.append(programme)
    data = ET.tostring(tv, encoding='utf-8', xml_declaration=True)
    encoded = gzip.compress(data, mtime=0)
    return encoded, dict(sorted(future.items()))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-dir', type=Path)
    args = parser.parse_args()
    config = json.loads((ROOT / 'epg-mappings.json').read_text(encoding='utf-8'))
    def fetch(url):
        if args.cache_dir:
            return (args.cache_dir / url.rsplit('/', 1)[-1]).read_bytes()
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 HomeTVGuide/1.0'}), timeout=45) as response:
            data = response.read(25 * 1024 * 1024 + 1)
        if len(data) > 25 * 1024 * 1024:
            raise ValueError('Compressed guide exceeds size limit')
        return data
    encoded, counts = build(config, fetch)
    entries = merge_m3u.parse((ROOT / 'merged.m3u').read_text(encoding='utf-8'))
    covered = [e.name for e in entries if e.attrs.get('tvg-id') in counts]
    missing = [e.name for e in entries if e.attrs.get('tvg-id') not in counts]
    report = {'guide_url': merge_m3u.EPG_URL, 'playlist_streams': len(entries), 'streams_with_current_guide': len(covered), 'unique_guide_channels': len(counts), 'programmes': sum(counts.values()), 'covered': covered, 'no_current_guide': missing, 'programme_counts': counts, 'note': 'Only source programmes with valid times and titles are included. Missing/stale channels get no invented programmes. Counts are point-in-time, not a promise of continuous schedule availability.'}
    atomic_write(ROOT / 'guide.xml.gz', encoded)
    atomic_write(ROOT / 'reports/epg-coverage.json', (json.dumps(report, indent=2, ensure_ascii=False) + '\n').encode())
    print(f'Guide: {len(counts)} channel IDs, {len(covered)}/{len(entries)} playlist streams, {sum(counts.values())} future/current programmes')

if __name__ == '__main__':
    main()
