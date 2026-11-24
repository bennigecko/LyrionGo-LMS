#!/usr/bin/env python3
"""Baut das LMS-Plugin "LyrionGo Transcode": install.xml, ZIP und repo.xml.

Aufruf: python3 lms-plugin/build.py <owner/repo>   (öffentliches GitHub-Repo für die Releases)
Ergebnis in dist/: LyrionGoTranscode-<version>.zip und repo.xml.
Veröffentlichen: ZIP nach releases/ und repo.xml ins Wurzelverzeichnis des öffentlichen Repos legen.
"""
import hashlib, os, sys, zipfile

here = os.path.dirname(os.path.abspath(__file__))
name = "LyrionGoTranscode"
repo = sys.argv[1] if len(sys.argv) > 1 else "OWNER/REPO"
version = open(os.path.join(here, "version.txt")).read().strip()
src = os.path.join(here, name)

with open(os.path.join(src, "install.xml"), "w") as f:
    f.write(f"""<?xml version="1.0"?>
<extension>
  <name>PLUGIN_LYRIONGOTRANSCODE</name>
  <module>Plugins::{name}::Plugin</module>
  <version>{version}</version>
  <description>PLUGIN_LYRIONGOTRANSCODE_DESC</description>
  <creator>Benjamin Friedrich</creator>
  <homepageURL>https://github.com/{repo}</homepageURL>
  <defaultState>enabled</defaultState>
  <type>2</type>
  <targetApplication>
    <id>SlimServer</id>
    <minVersion>7.9</minVersion>
    <maxVersion>9.*</maxVersion>
  </targetApplication>
</extension>
""")

dist = os.path.join(here, "dist")
os.makedirs(dist, exist_ok=True)
zpath = os.path.join(dist, f"{name}-{version}.zip")
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    # Feste Zeitstempel -> gleiche Dateien ergeben immer dieselbe ZIP (und SHA1 in repo.xml)
    d = zipfile.ZipInfo(f"{name}/", (2026, 1, 1, 0, 0, 0)); d.external_attr = 0o40755 << 16
    z.writestr(d, "")
    for fn in sorted(os.listdir(src)):
        zi = zipfile.ZipInfo(f"{name}/{fn}", (2026, 1, 1, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o644 << 16
        z.writestr(zi, open(os.path.join(src, fn), "rb").read())
sha = hashlib.sha1(open(zpath, "rb").read()).hexdigest()

with open(os.path.join(dist, "repo.xml"), "w") as f:
    f.write(f"""<?xml version="1.0"?>
<extensions>
  <details>
    <title lang="EN">LyrionGo Plugin Repository</title>
  </details>
  <plugins>
    <plugin name="{name}" version="{version}" minTarget="7.9" maxTarget="9.*">
      <title lang="EN">LyrionGo Transcode Rules</title>
      <title lang="DE">LyrionGo Transcodierregeln</title>
      <desc lang="EN">Transcode rules for the Android app LyrionGo: FLAC/MP3 to Opus or Ogg Vorbis for streaming and offline downloads.</desc>
      <desc lang="DE">Transcodierregeln für die Android-App LyrionGo: FLAC/MP3 zu Opus oder Ogg Vorbis für Streaming und Offline-Downloads.</desc>
      <url>https://raw.githubusercontent.com/{repo}/main/releases/{name}-{version}.zip</url>
      <sha>{sha}</sha>
      <link>https://github.com/{repo}</link>
      <creator>Benjamin Friedrich</creator>
    </plugin>
  </plugins>
</extensions>
""")
print(zpath, sha)
