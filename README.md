# Home TV playlists

A categorized M3U playlist for Next Gen and other compatible IPTV players.

- [Combined playlist](https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/merged.m3u)
- Guide: https://epgshare01.online/epgshare01/epg_ripper_IN1.xml.gz
- Sources: Odia, Doordarshan, News, Music, Hindi Entertainment, Movies, English Movies, Kids, Sports, Knowledge and Lifestyle under `sources/`.

## October 24, 2026: English Movies

Added **English Movies**, containing **18 channel identities across 19 stream entries** (Action Hollywood Movies includes a second regional feed). The combined playlist now contains **195 unique stream URLs**. Sixteen URLs are new; three existing English streams were moved from Movies so global deduplication cannot hide them in the old category.

The category includes 24 Hour Free Movies, 30A TV Classic Movies, Action Hollywood Movies, ARTFLIX Movie Classics, Dark Matter TV, Ebony TV by Lionsgate, FilmRise Western, FrightFlix, Gravitas Movies, Hallmark Movies & More, Maverick Black Cinema, MovieSphere, MyTime Movie Network, NOST, OuterSphere, TVS Drive In Movie, Watch it Scream! and Whiplash Cinema. Movie-focused channels can also schedule related series or other programming.

Research used the current [IPTV-org channel, feed, stream and logo indexes](https://github.com/iptv-org/api) and provider pages, including [30A TV](https://30a-tv.com/m3u8-channels/), [MyTime](https://mytimemovienetwork.com/) and [Lionsgate](https://lionsgatechannels.com/where-to-watch). Selected feed language is English. Each included URL passed an HLS master/media-playlist check and a small media-segment request from the development network. Failed or geo-blocked candidates were not added. These are point-in-time reachability checks, not guarantees of future or worldwide playback.

All entries have validated local WebP logos with original sources recorded in `logo-sources.json`. 30A Classic Movies uses the broadcaster's network mark. Canonical channel IDs are retained, but the existing India XMLTV feed is not claimed to provide their English schedules. The old stream labeled **My Cinema** was corrected to **MyTime Movie Network**, matching its actual endpoint and current stream index. Research, selected streams, identity corrections and unsuccessful candidates are recorded in `reports/english-movies.json`.

Source: `sources/english_movies.m3u`. Refresh channels in Next Gen to load the category; an APK update is not required.

## October 20, 2026 audit

The combined playlist contains **179 unique stream URLs**, including backup renditions of some channels. **25 additional channel identities** were added across nine categories. Doordarshan already included all 35 available channel entries in the checked public index, so no invented additions were made there.

**11 failing URLs** were replaced with alternatives whose HLS manifests responded successfully. Exact URL duplicates are removed globally, so the total grew from 158 to 179 rather than 183. Twelve movie entries were moved out of Hindi Entertainment into Movies, and a music entry was moved out of Movies. The stream labeled FOX NEWS was corrected to LiveNOW from FOX, which is what its URL carries.

**178 of 179 streams have a logo**, served as small, validated WebP images from this repository. Music Reload remains text-only because its identity/logo could not be verified. The malformed concatenated Playboy logo URL was repaired. Logos retain their respective owners' identities; the original image sources are listed in `logo-sources.json`.

**117 streams have an exact channel ID present in the selected India XMLTV feed.** Other entries retain a known channel identity where available, without pretending a schedule exists. Some regional, international and FAST channels have no matching schedule in this feed. `reports/metadata-coverage.json` lists these entries. HD/SD variants use separate IDs where a corresponding feed exists.

The measured stream results were 167 successful HLS manifests, 2 media responses, and 10 unavailable responses/timeouts. These checks come from one network and do not prove continuous playback or worldwide access. Unresolved entries are retained in `reports/stream-health.json` rather than silently deleted after a transient or regional failure. Search and replacement provenance is in `reports/playlist-changes.json`.

## Build and check

Python 3.11+ is sufficient; merging and stream audits use the standard library.

```sh
python -m unittest discover -s tests -v
python merge_m3u.py
python tools/audit_playlist.py --workers 8 --timeout 12
```

The merge reads checked-in files, preserves stream headers/options, validates each EXTINF/URL pair, enriches metadata, removes exact URL duplicates and atomically publishes the result. An invalid or missing source fails the build and preserves the previous output. The output is deterministic: no timestamp-only commits, no downloads of this repository's own source files, and no partial output when a source cannot be read.

The GitHub workflow tests before publishing, runs for source/metadata changes and on the existing two-hour schedule, and commits only actual changes. A manual run can optionally audit stream reachability. It does not automatically remove failures or guess replacement URLs.

## Maintaining channels

Edit the appropriate source playlist. Keep one EXTINF and one URL per entry; directives such as `#EXTVLCOPT` and `#KODIPROP` belong between them. Use a matching `tvg-id`, `tvg-name` and `tvg-logo` when known. Every source file includes the guide URL. `channel-metadata.json` stores the curated per-name mappings applied during a merge. Update that mapping when renaming a channel or changing a guide feed; do not assign a similar but different station's schedule.

Channel identities, candidate stream URLs and logo references were researched using the public [IPTV-org API/database](https://github.com/iptv-org/api), broadcaster websites where available, and the channel list in the selected XMLTV feed. Regional aliases include DD Odia / DD Oriya, DD Tamil / DD Podhigai and News18 Odia / News18 Oriya. Public source metadata can change, so recheck URLs and channel identity when updating them.
