import sys
from scripts.process_x83 import extract_x83_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Fehler: Kein Pfad zur Datei angegeben.")
        sys.exit(1)

    file_path = sys.argv[1]

    # Verarbeitung starten
    if file_path.lower().endswith(".x83"):
        print(extract_x83_data(file_path))
    else:
        print("Fehler: Dateityp wird nicht unterstützt.")

