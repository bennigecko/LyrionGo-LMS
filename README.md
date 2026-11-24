# LyrionGo Transcode Rules – LMS-Plugin

Transcodierregeln für die Android-App **LyrionGo** (Lyrion Music Server Player).
LMS wandelt damit FLAC (und auf Wunsch MP3) in **Opus** oder **Ogg Vorbis** um,
sowohl beim Streamen als auch für Offline-Downloads.

## Installation

1. LMS → *Einstellungen* → *Plugins*.
2. Ganz unten unter *Weitere Repositorys* diese Adresse eintragen und speichern:
   ```
   https://raw.githubusercontent.com/bennigecko/LyrionGo-LMS/main/repo.xml
   ```
3. In der Liste **LyrionGo Transcode Rules** aktivieren, speichern und LMS neu starten.
4. Für Opus muss `opusenc` auf dem Server installiert sein (Debian/Ubuntu/Raspberry Pi: `apt install opus-tools`).

## So erkennt LMS die Einstellungen der App

LMS wählt Regeln nach Quellformat, Zielformat und Modellname des Players. LyrionGo meldet sich
je nach Einstellung z. B. als `LyrionGoO128M160` (Opus 128 kbps, MP3 → Opus 160 kbps) oder
`LyrionGoQ6M` (Ogg Vorbis Stufe 6 inkl. MP3). Downloads haben keinen Player und nutzen daher
private Typen (`op96` … `op192`, `lg6`, `lg8`, `lgx`), die kein anderer Player anbietet –
andere Player werden also nicht beeinflusst.

Aufbau der Regeln nach dem Vorbild von [MobileTranscode](https://github.com/mtxmiller/MobileTranscode).

## Neue Version veröffentlichen

`version.txt` erhöhen, `python3 build.py bennigecko/LyrionGo-LMS` ausführen, `dist/repo.xml`
nach `repo.xml` kopieren und die ZIP aus `dist/` als Release `v<version>` hochladen.
