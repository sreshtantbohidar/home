import unittest
import tempfile
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import merge_m3u as m

class MergeTests(unittest.TestCase):
    def test_bom_wrapping_headers_and_duration(self):
        entries=m.parse('\ufeff#EXTM3U\n#EXTINF:0 tvg-id="One"\n tvg-logo="https://image.test/a.png",Channel, One\n#EXTVLCOPT:http-referrer=https://example.test/\nhttps://example.test/live.m3u8\n','News')
        self.assertEqual(1,len(entries));self.assertEqual('Channel, One',entries[0].name)
        self.assertEqual('0',entries[0].duration);self.assertEqual('News',entries[0].attrs['group-title'])
        self.assertEqual(['#EXTVLCOPT:http-referrer=https://example.test/'],entries[0].directives)
    def test_does_not_attach_next_channel_url_to_orphan(self):
        with self.assertRaises(ValueError):m.parse('#EXTM3U\n#EXTINF:-1,Broken\n#EXTINF:-1,Other\nhttps://test/live')
    def test_missing_final_url_and_orphan_url_rejected(self):
        for content in ['#EXTM3U\n#EXTINF:-1,Broken', '#EXTM3U\nhttps://test/live']:
            with self.assertRaises(ValueError):m.parse(content)
    def test_dedupe_by_url_keeps_distinct_backups(self):
        e=[m.Entry('One','https://test/one'),m.Entry('Duplicate','https://test/one'),m.Entry('Backup','https://test/two')]
        self.assertEqual(['One','Backup'],[r.name for r in m.parse(m.render(e))])
    def test_quoted_comma_and_protocol_prefix(self):
        self.assertEqual('Name',m.parse('#EXTINF:-1 tvg-name="Name, English",Name\nhttps://test/live')[0].name)
        self.assertFalse(m.stream_url('httpx://test/live'));self.assertTrue(m.stream_url('https://test/live|User-Agent=Player'))
    def test_metadata_preserves_quality_specific_guide_and_directives(self):
        entries=m.parse('#EXTINF:-1 tvg-id="One.in@HD",One HD\n#KODIPROP:inputstream=adaptive\nhttps://test/one')
        m.enrich(entries[0],{'by_name':{'One HD':{'tvg-id':'One.HD.in','tvg-logo':'https://test/logo.png'}}})
        output=m.render(entries)
        self.assertIn('tvg-id="One.HD.in"',output);self.assertIn('#KODIPROP:inputstream=adaptive',output)
        self.assertIn('x-tvg-url=',output)
    def test_failed_source_does_not_overwrite_last_good_playlist(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'sources').mkdir()
            for filename in m.SOURCES.values():(root/'sources'/filename).write_text('#EXTM3U\n',encoding='utf-8')
            target=root/'merged.m3u';target.write_text('previous good playlist',encoding='utf-8')
            (root/'sources/o.m3u').write_text('invalid',encoding='utf-8')
            with self.assertRaises(ValueError):m.merge_playlists(root)
            self.assertEqual('previous good playlist',target.read_text(encoding='utf-8'))
    def test_real_sources_render_and_build_deterministically(self):
        first=m.merge_playlists(); target=m.ROOT/'merged.m3u';before=target.stat().st_mtime_ns
        self.assertEqual(first,m.merge_playlists());self.assertEqual(before,target.stat().st_mtime_ns)
        entries=m.parse(first);self.assertGreater(len(entries),100);self.assertEqual(len(entries),len({r.url for r in entries}))

if __name__=='__main__':unittest.main()
