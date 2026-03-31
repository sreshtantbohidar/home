import requests
import re

URLS = {
    "Odia": "https://raw.githubusercontent.com/sreshtantbohidar/WATCH-LIVE-TV/refs/heads/main/o.m3u",
    "Sports": "https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/refs/heads/main/ALL.m3u"
}

OUTPUT_FILE = "merged.m3u"


def fetch_m3u(url):
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        return res.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""


def add_group_title(extinf_line, category):
    """
    Inject group-title into EXTINF line.
    If already exists → replace it
    """
    if 'group-title=' in extinf_line:
        return re.sub(r'group-title=".*?"', f'group-title="{category}"', extinf_line)
    else:
        return extinf_line.replace(
            "#EXTINF:-1",
            f'#EXTINF:-1 group-title="{category}"'
        )


def merge_playlists():
    merged = ["#EXTM3U"]

    for category, url in URLS.items():
        content = fetch_m3u(url)
        if not content:
            continue

        lines = content.splitlines()

        # Skip header
        if lines and lines[0].startswith("#EXTM3U"):
            lines = lines[1:]

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith("#EXTINF"):
                # Modify EXTINF with category
                extinf = add_group_title(line, category)

                # Next line should be URL
                if i + 1 < len(lines):
                    stream_url = lines[i + 1].strip()
                    merged.append(extinf)
                    merged.append(stream_url)
                    i += 2
                    continue

            i += 1

        merged.append("")  # spacing between playlists

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged))


if __name__ == "__main__":
    merge_playlists()
