from lxml import etree

def extract_x83_data(file_path):
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()

        result = []

        # Projektinformationen
        prj_info = root.find(".//{http://www.gaeb.de/GAEB_DA_XML/DA83/3.2}PrjInfo")
        if prj_info is not None:
            project_name = prj_info.find(".//{http://www.gaeb.de/GAEB_DA_XML/DA83/3.2}LblPrj")
            if project_name is not None:
                result.append(f"Projekt: {project_name.text.strip()}")

        # Positionen auslesen
        for boq in root.findall(".//{http://www.gaeb.de/GAEB_DA_XML/DA83/3.2}BoQ"):
            for item in boq.findall(".//{http://www.gaeb.de/GAEB_DA_XML/DA83/3.2}Item"):
                pos_id = item.attrib.get("ID", "Unbekannt")
                short_text = item.find("{http://www.gaeb.de/GAEB_DA_XML/DA83/3.2}ShortText")
                description = item.find("{http://www.gaeb.de/GAEB_DA_XML/DA83/3.2}Description")

                # Langtexte extrahieren
                detailed_texts = []
                if description is not None:
                    for sub_text in description.iter():
                        if sub_text.text and sub_text.text.strip():
                            detailed_texts.append(sub_text.text.strip())

                # Zusammenfassung der Position
                position_summary = f"Position {pos_id}:"
                if short_text is not None and short_text.text:
                    position_summary += f" {short_text.text.strip()}"
                if detailed_texts:
                    position_summary += f" Details: {' '.join(detailed_texts)}"

                result.append(position_summary)

        return "\n".join(result)

    except Exception as e:
        return f"Fehler bei der Verarbeitung der Datei: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Fehler: Kein Pfad zur X83-Datei angegeben.")
        sys.exit(1)

    file_path = sys.argv[1]
    print(extract_x83_data(file_path))

