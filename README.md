# JSON Text Extractor

Ein Python-Script zum Extrahieren von Textinhalten aus JSON- und JSONL-Dateien.

## Beschreibung

Dieses Tool liest JSON- oder JSONL-Dateien, extrahiert den Wert des Schlüssels `text` aus jedem JSON-Objekt und speichert diese Texte in einer neuen JSON-Datei als Liste von Objekten im Format `{"text": "extrahierter_text"}`.
## Eingabeformate

```json
[
  {"id": 1, "text": "Erster Text", "author": "User1"},
  {"id": 2, "text": "Zweiter Text", "author": "User2"}
  {"id": 3, "text": "Zweiter Text", "author": "User3"}
]
```

## Ausgabeformat

Das Script erstellt immer eine JSON-Datei mit folgendem Format:

```json
[
  {"text": "Erster Text"},
  {"text": "Zweiter Text"},
  {"text": "Dritter Text"}
]
```

## Features

- **Flexible Eingabe**: Unterstützt sowohl JSON- als auch JSONL-Dateien
- **Robuste Verarbeitung**: Automatische Erkennung des Dateiformats
- **Fehlerbehandlung**: Detaillierte Warnungen bei problematischen Einträgen
- **UTF-8 Unterstützung**: Vollständige Unicode-Unterstützung
- **Statistiken**: Ausgabe der Anzahl verarbeiteter und extrahierter Einträge

## Voraussetzungen

- Python 3.6 oder höher
- Keine externen Abhängigkeiten erforderlich (verwendet nur Standard-Bibliotheken)

## Installation

1. Laden Sie das Script herunter:
```bash
git clone https://github.com/Tirggel/extract_texts.git
cd extract_texts
```

2. Das Script ist sofort einsatzbereit - keine Installation zusätzlicher Pakete erforderlich.

## Verwendung

### Grundlegende Verwendung

```bash
python extract_texts.py input_file.json output_file.json
```

### Hilfe

Für Hilfe zur Verwendung:

```bash
python extract_texts.py --help
```

## Lizenz

MIT License - Siehe LICENSE-Datei für Details

## Autor

[Peter Rubin](https://github.com/Tirggel
