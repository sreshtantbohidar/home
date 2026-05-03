import requests
import re
from datetime import datetime
import time

URLS = {
    "Odia": "https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/sources/o.m3u",
    "News": "https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/sources/n.m3u",
    "Music": "https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/sources/m.m3u",
    "Hindi Entertainment": "https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/sources/he.m3u",
    "Movies": "https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/sources/mo.m3u",
    "Kids": "https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/sources/k.m3u",
    "Lifestyle": "https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/sources/f.m3u"
}

OUTPUT_FILE = "merged.m3u"
SUPPORTED_PROTOCOLS = ("http", "https", "rtmp", "rtsp", "udp")
OVERWRITE_GROUP_TITLE = True


# 🔁 Retry-enabled fetch
def fetch_m3u(url):
    for attempt in range(3):
        try:
            print(f"Fetching ({attempt+1}/3): {url}")
            res = requests.get(url, timeout=30)
            res.raise_for_status()
            return res.text
        except Exception as e:
            print(f"Retry {attempt+1} failed: {e}")
            time.sleep(2)
    print(f"❌ Failed to fetch after retries: {url}")
    return ""


def is_stream_url(line):
    return line.startswith(SUPPORTED_PROTOCOLS)


def add_group_title(extinf_line, category):
    if 'group-title=' in extinf_line:
        if OVERWRITE_GROUP_TITLE:
            return re.sub(r'group-title=".*?"', f'group-title="{category}"', extinf_line)
        return extinf_line
    else:
        return extinf_line.replace(
            "#EXTINF:-1",
            f'#EXTINF:-1 group-title="{category}"'
        )


def merge_playlists():
    merged = ["#EXTM3U"]

    # 🕒 Force update (ensures commit always happens)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    merged.append(f"# Updated: {timestamp}")

    seen_urls = set()

    for category, url in URLS.items():
        print(f"\n📂 Processing category: {category}")

        content = fetch_m3u(url)
        if not content:
            continue

        lines = content.splitlines()

        # Remove header if exists
        if lines and lines[0].startswith("#EXTM3U"):
            lines = lines[1:]

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # =========================
            # CASE 1: EXTINF block
            # =========================
            if line.startswith("#EXTINF"):
                extinf = add_group_title(line, category)
                block_lines = [extinf]

                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()

                    if is_stream_url(next_line):
                        if next_line not in seen_urls:
                            merged.extend(block_lines)
                            merged.append(next_line)
                            seen_urls.add(next_line)
                        i += 1
                        break

                    elif next_line.startswith("#"):
                        block_lines.append(next_line)
                        i += 1
                    else:
                        i += 1

                continue

            # =========================
            # CASE 2: URL without EXTINF
            # =========================
            elif is_stream_url(line):
                if line not in seen_urls:
                    merged.append(f'#EXTINF:-1 group-title="{category}",Unknown Channel')
                    merged.append(line)
                    seen_urls.add(line)

            i += 1

        merged.append("")  # spacing between categories

    # Write file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged))

    print(f"\n✅ Merged playlist written to {OUTPUT_FILE}")
    print(f"📊 Total unique streams: {len(seen_urls)}")


if __name__ == "__main__":
    merge_playlists()
