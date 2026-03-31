import requests

URLS = [
    "https://raw.githubusercontent.com/sreshtantbohidar/WATCH-LIVE-TV/refs/heads/main/o.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/refs/heads/main/ALL.m3u"
]

OUTPUT_FILE = "merged.m3u"


def fetch_m3u(url):
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        return res.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""


def merge_playlists():
    merged = ["#EXTM3U\n"]

    for url in URLS:
        content = fetch_m3u(url)
        if not content:
            continue

        lines = content.splitlines()

        # Skip header if present
        if lines and lines[0].startswith("#EXTM3U"):
            lines = lines[1:]

        merged.extend(lines)
        merged.append("\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged))


if __name__ == "__main__":
    merge_playlists()
