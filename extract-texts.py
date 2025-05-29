import json
import argparse
import os


def extract_texts_to_json_objects(input_filepath, output_filepath):
    """
    Liest eine JSON- oder JSONL-Datei, extrahiert den Wert des Schlüssels 'text'
    aus jedem JSON-Objekt und speichert diese Texte in einer neuen JSON-Datei
    als Liste von Objekten, wobei jedes Objekt die Form {"text": "extrahierter_text"} hat.
    Gibt am Ende die Anzahl der extrahierten Einträge aus.

    Args:
        input_filepath (str): Pfad zur Eingabe-JSON- oder JSONL-Datei.
        output_filepath (str): Pfad zur Ausgabe-JSON-Datei.
    """
    extracted_data = []
    processed_objects = 0
    found_texts = 0

    if not os.path.exists(input_filepath):
        print(f"Fehler: Eingabedatei '{input_filepath}' nicht gefunden.")
        return

    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            # Zuerst versuchen, die Datei als einzelnes JSON-Objekt oder Array zu laden
            try:
                data = json.load(infile)
                if isinstance(data, list):
                    # Es ist ein Array von JSON-Objekten
                    for item in data:
                        processed_objects += 1
                        if isinstance(item, dict) and 'text' in item:
                            extracted_data.append({"text": item['text']})
                            found_texts += 1
                        elif isinstance(item, dict):
                            print(f"Warnung: Objekt in Liste hat keinen 'text'-Schlüssel: {
                                  item.get('id', 'Unbekanntes Objekt')}")
                elif isinstance(data, dict):
                    # Es ist ein einzelnes JSON-Objekt
                    processed_objects += 1
                    if 'text' in data:
                        extracted_data.append({"text": data['text']})
                        found_texts += 1
                    else:
                        print(
                            f"Warnung: Das JSON-Objekt hat keinen 'text'-Schlüssel.")
                else:
                    print(f"Warnung: Die Datei '{
                          input_filepath}' enthält weder ein JSON-Objekt noch ein JSON-Array an der Wurzel.")
                    # Wenn es kein Objekt oder Array ist, aber auch kein JSONDecodeError auslöst (selten),
                    # könnte es hier sein, dass wir trotzdem versuchen sollten, als JSONL zu parsen.
                    # Aber json.load() hätte wahrscheinlich schon einen Fehler geworfen.
                    # Für den Moment belassen wir es so, da der JSONL-Pfad unten greift, wenn json.load() fehlschlägt.

            except json.JSONDecodeError as e:
                # Wenn json.load fehlschlägt, könnte es JSONL sein oder ungültiges JSON.
                # Wir setzen den Dateizeiger zurück und versuchen Zeile für Zeile.
                print(f"Info: Konnte Datei nicht als einzelnes JSON-Objekt/-Array laden (Fehler: {
                      e}). Versuche als JSONL...")
                infile.seek(0)  # Dateizeiger an den Anfang setzen
                for i, line in enumerate(infile):
                    line = line.strip()
                    if not line:  # Leere Zeilen überspringen
                        continue
                    try:
                        json_obj = json.loads(line)
                        processed_objects += 1
                        if isinstance(json_obj, dict) and 'text' in json_obj:
                            extracted_data.append({"text": json_obj['text']})
                            found_texts += 1
                        elif isinstance(json_obj, dict):
                            print(
                                f"Warnung (Zeile {i+1}): JSON-Objekt hat keinen 'text'-Schlüssel.")
                        else:
                            print(
                                f"Warnung (Zeile {i+1}): Zeile ist kein JSON-Objekt: {line[:80]}...")
                    except json.JSONDecodeError:
                        print(f"Warnung (Zeile {
                              i+1}): Konnte Zeile nicht als JSON interpretieren: {line[:80]}...")

        if not extracted_data and processed_objects == 0 and found_texts == 0:
            # Diese Bedingung fängt ab, wenn die Datei komplett leer war oder nur ungültige Zeilen enthielt
            # und keine Objekte verarbeitet wurden.
            print(f"Warnung: Keine verarbeitbaren JSON-Objekte in '{
                  input_filepath}' gefunden oder Datei ist leer/ungültig.")
            # Es wird keine Ausgabedatei erstellt, wenn extracted_data leer ist, aber es ist gut, das explizit zu machen.
            # Wenn extracted_data leer ist, aber Objekte verarbeitet wurden (nur ohne 'text'),
            # wird eine leere Liste [] in die Ausgabedatei geschrieben.
            if not extracted_data:
                print(f"Es werden keine Einträge in '{
                      output_filepath}' geschrieben, da keine Texte gefunden wurden.")
                # Man könnte hier entscheiden, ob man eine leere JSON-Datei ([]) schreiben will oder nicht.
                # Aktuell wird eine leere Liste geschrieben, wenn found_texts == 0 aber processed_objects > 0.
                # Wenn wir hier returnen, wird gar nichts geschrieben, auch keine leere Liste.
                # Ich lasse es so, dass eine leere Liste geschrieben wird, falls Objekte verarbeitet wurden,
                # aber kein Textfeld hatten.
                # Die obige Bedingung zielt mehr auf "komplett nichts gefunden/verarbeitet".

        # Speichere die extrahierten Daten in der Ausgabedatei
        # Auch wenn extracted_data leer ist (weil keine Texte gefunden wurden),
        # wird eine Datei mit einer leeren Liste `[]` erstellt.
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            json.dump(extracted_data, outfile, ensure_ascii=False, indent=4)

        print(f"Erfolgreich {found_texts} Texte aus {
              processed_objects} verarbeiteten Objekten extrahiert.")
        print(f"Ergebnisse gespeichert in '{output_filepath}'.")
        # len(extracted_data) ist hier gleich found_texts
        print(f"Die Ausgabedatei '{output_filepath}' enthält {
              len(extracted_data)} Einträge.")

    except FileNotFoundError:
        print(f"Fehler: Eingabedatei '{input_filepath}' nicht gefunden.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extrahiert Texte aus einer JSON- oder JSONL-Datei und speichert sie in einer neuen JSON-Datei als Liste von {'text': ...} Objekten."
    )
    parser.add_argument(
        "input_file",
        help="Pfad zur Eingabe-JSON- oder JSONL-Datei."
    )
    parser.add_argument(
        "output_file",
        help="Pfad zur Ausgabe-JSON-Datei, in der die extrahierten Texte gespeichert werden."
    )

    args = parser.parse_args()

    extract_texts_to_json_objects(args.input_file, args.output_file)
