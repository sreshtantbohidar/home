"""Bounded, non-destructive HTTP checks. Reachability does not prove playback rights or decoding."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlsplit, parse_qsl
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import merge_m3u


def check(entry, timeout):
    result = {"name": entry.name, "url": entry.url, "epg_id": entry.attrs.get('tvg-id', ''), "logo": entry.attrs.get('tvg-logo', '')}
    base, _, extra = entry.url.partition('|')
    if not base.startswith(('https://', 'http://')):
        result['status'] = 'not_http'; return result
    headers = {'User-Agent': 'Mozilla/5.0 NextGenPlaylistAudit/1.0'}
    headers.update(dict(parse_qsl(extra)))
    for directive in entry.directives:
        if directive.startswith('#EXTVLCOPT:http-referrer='): headers['Referer'] = directive.split('=',1)[1]
        if directive.startswith('#EXTVLCOPT:http-user-agent='): headers['User-Agent'] = directive.split('=',1)[1]
    try:
        with urlopen(Request(base, headers=headers), timeout=timeout) as response:
            content = response.read(1024*1024)
            final = response.url
            result['http_status'] = response.status
        text = content.decode('utf-8-sig', errors='replace').lstrip()
        if text.startswith('#EXTM3U'):
            # Resolve one child rendition, without downloading video segments.
            if '#EXT-X-STREAM-INF' in text:
                child = next((line.strip() for line in text.splitlines() if line.strip() and not line.startswith('#')), None)
                if child:
                    with urlopen(Request(urljoin(final, child), headers=headers), timeout=timeout) as response:
                        child_text = response.read(1024*1024).decode('utf-8-sig', errors='replace').lstrip()
                    if not child_text.startswith('#EXTM3U'): raise ValueError('Child rendition is not an HLS playlist')
            result['status'] = 'hls_manifest_ok'
        elif '<MPD' in text[:2048]: result['status'] = 'dash_manifest_ok'
        elif content.startswith(b'G') or content[4:8] == b'ftyp': result['status'] = 'media_response'
        else: result['status'] = 'unexpected_response'
    except Exception as error:
        result['status'] = 'unavailable_at_check'
        result['error'] = str(error)[:250]
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout', type=int, default=12)
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--output', default='reports/stream-health.json')
    args=parser.parse_args()
    entries=merge_m3u.parse((merge_m3u.ROOT/'merged.m3u').read_text(encoding='utf-8'))
    with ThreadPoolExecutor(max_workers=max(1,min(12,args.workers))) as pool:
        results=list(pool.map(lambda e:check(e,args.timeout),entries))
    output=merge_m3u.ROOT/args.output; output.parent.mkdir(exist_ok=True,parents=True)
    output.write_text(json.dumps({'checked_at':datetime.now(timezone.utc).isoformat(), 'note':'One network vantage point; transient or geo-blocked errors do not prove permanent channel failure. Media manifests checked, not a full playback test.', 'channels':results},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    from collections import Counter
    print(dict(Counter(result['status'] for result in results)))

if __name__=='__main__': main()
