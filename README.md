# Home TV playlists

A categorized M3U playlist for Next Gen and other compatible IPTV players.

- [Combined playlist](https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/merged.m3u)
- [Combined programme guide](https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/guide.xml.gz)
- Sources: Odia, Doordarshan, News, Hindi Music, English Music, Hindi Entertainment, English Entertainment, Movies, English Movies, Kids, Sports, Knowledge and Lifestyle under `sources/`.

## November 1, 2026: AXN / HBO / Star Movies / MGM research

Added **AXN Asia (English)** under a new English Entertainment group and **HBO Asia (English)** under English Movies. These are explicitly regional Asian feeds, not Indian channel feeds. Their audio tracks are tagged English and both passed audio/video probing plus eight-second decode samples. Matching Indonesian AXN and Singapore HBO guide mappings are included. Third-party public operator links can change and are not an official broadcaster promise of free distribution or stable access.

No Star Movies or MGM entry was added: the tested Star Movies candidates and MGM+/former Epix candidate failed. [Research and checks](reports/axn-hbo-star-mgm-2026-11-01.json). The combined playlist now has **237 streams**, including the two new NH channels below.

## November 1, 2026: NH Studioz follow-up

Added **NH BollyGold** under Movies and **NH BollyRaga** under Hindi Music, using direct RunnTV masters. Both yielded H264 video and AAC audio up to 1080p and passed short decode tests. NH BollyFlix was already present. The combined playlist now contains **235 streams**, all with local icons. Stingray channels remain at the bottom of English Music. No current public programme schedule was found for the two additions.

The [official NH Studioz directory](https://www.nhstudioz.tv/our-channels) identifies the other requested brands, including NH Holly Flix, NH Prime and the records/music brands, as YouTube destinations. No verified standalone live HLS links were found for those; YouTube watch/channel pages were not inserted as IPTV stream URLs. NH Golden Plaza and NH BollyGold are distinct destinations. The [research report](reports/nh-studioz-2026-11-01.json) records every requested name and its official destination.

## November 1, 2026: music groups

Music is now split into **Hindi Music** and **English Music**. Regional Indian music is included with Hindi Music as requested. All Stingray-branded channels, including Qello Concerts by Stingray, appear at the bottom of English Music. Relative order within the other music channels is preserved.

## November 1, 2026: complete stream, icon and guide audit

Audited all **235 previous stream entries**. **8 failing entries were replaced** after the alternatives passed audio/video probes and short decode tests: RT, Nazara, HUM TV, Sony Entertainment Television (two entries), B4U Movies, FashionTV Paris and Documentary+. Repairing duplicate Sony/FashionTV entries leaves **233 unique stream URLs**. **209** yielded audio and video in the initial/retry checks; **24 remain unresolved** and are retained, with reasons and tested alternatives in [the full audit](reports/full-audit-2026-11-01.json). A working manifest alone was not counted as playback, and a supposed Zee Cinema alternative carrying National Geographic was rejected. Checks are point-in-time from one network, not a guarantee of continuous playback or permission to redistribute.

**Every entry now has a valid, locally stored icon.** Trace UK uses its broadcaster logo via Wikimedia Commons. Music Reload, Goldmines 2 and MH One Movies use newly created channel-name badges because an exact downloadable logo could not be verified; these are not claimed as official logos. Provenance is recorded in `logo-sources.json`.

The compact [combined XMLTV guide](https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/guide.xml.gz) currently covers **151 of 233 streams** across **140 guide IDs**, using explicit mappings from Indian, UK, US, Plex and Rakuten public guides. The remaining **82 entries** have no verified current programme data in the checked sources. No placeholder schedules, nearby-channel schedules or invented programme titles were added. Some published channel records are empty or stale and are excluded. [Coverage](reports/epg-coverage.json) and [source mappings](epg-mappings.json) are recorded separately.

The existing two-hour GitHub workflow rebuilds this mapped guide. Source fetch/parse failures or a large coverage loss fail the build and preserve the previously published guide. Time zones and original programme titles are preserved. To use the expanded guide, set your player EPG URL to `https://raw.githubusercontent.com/sreshtantbohidar/home/refs/heads/main/guide.xml.gz`; playlist headers now advertise it too. Players with a separately saved EPG setting need that setting updated.

## November 1, 2026: Hindi music follow-up

Added **Epic Music** (formerly ShowBox), **Zoom** (music plus entertainment news/interviews), and **Insync** (Indian classical, ghazal, Sufi and allied music) under Music. These are Hindi-feed additions; Insync is not a Bollywood-only channel and programs may include other languages. Existing Mastiii and 9X Jalwa were not duplicated. The combined playlist now contains **235 unique streams**.

Checked 14 candidate URLs and confirmed audio and video for all three selected streams. Punjabi/Haryanvi-focused channels, signed account-dependent links, proxy-only links and candidates failing TLS/timeouts were left out. The [research report](reports/hindi-music-2026-11-01.json) records candidates, codec results and broadcaster references. Availability and permissions remain provider-dependent.

## November 1, 2026: more music and movie channels

Added **37 new channel identities and stream URLs**: **22** in Music, **7** in English Movies and **8 Hindi movie channels** in Movies. The combined playlist now contains **232 unique stream URLs**. Existing channel URLs and categories are preserved; Goldmines Movies was skipped because its stream already exists as Gold Mines Movie.

Music additions include California Music Channel, CMC-USA Country Music Channel, Clubbing TV, LIVExLIVE, Now 90s00s, Qello Concerts, The Country Network, Trace UK, V2BEAT TV, Vevo Pop, Video Mix TV, XITE 90's Throwback, and ten Stingray song channels spanning classic rock, pop, country, oldies and the 1970s–1990s. The Stingray song channels show artwork rather than continuous music videos. English is the selected feed language; individual songs and occasional programs may use other languages.

English Movies adds Cinevault 80s, GREAT! movies, GREAT! romance, KidsFlix, Nolly Africa, Wu Tang Collection and Grjngo Western Movies (UK English feed). These include Hollywood classics, romance, family films, English-language African cinema and dubbed martial-arts/Western films; some channels also schedule series or seasonal programming. Movies adds All Time Movies, Goldmines 2, Goldmines Action, Maha Movie, Manoranjan Grand, MH One Movies, Shemaroo Josh and Zee South Flix.

Research covered the current [IPTV-org public channel/feed/stream indexes](https://github.com/iptv-org/api), [Vevo](https://www.hq.vevo.com/press/vevo-partners-with-sling-launches-music-video-channels-on-sling-freestream), [Stingray](https://support.stingray.com/hc/en-us/articles/47976651564955-TV-Channels-Free-Streaming-FAST), and [Grjngo](https://www.grjngo.com/). **108 candidate URLs** received bounded HLS/media-segment checks; the additional Grjngo English feed was probed separately. Each selected URL yielded video and audio in ffprobe. Some Amagi feeds use ad-tracking redirects without a video filename extension; the probe was configured to accept these HTTP segments. Stable master URLs are stored, not generated session renditions. Failing, encrypted, and proxy-only candidates were excluded.

These are point-in-time checks from one network, not sustained playback, availability in every region, or redistribution-rights certification. No login, DRM or geographic restriction was bypassed. Publicly indexed links do not by themselves establish permission for commercial redistribution. **34 additions have validated local WebP logos**; Goldmines 2, MH One Movies and Trace UK remain text-only because an exact downloadable logo could not be verified. Channel IDs are retained without claiming schedules exist in the India XMLTV guide. Full selected-feed metadata, codec results, logo provenance and candidate failures are in [the research report](reports/channel-expansion-2026-11-01.json).

Refresh the existing combined-playlist URL in Next Gen to load the additions; no APK update is needed.

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
