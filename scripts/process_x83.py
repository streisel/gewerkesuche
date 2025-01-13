from lxml import etree
import sys

def extract_x83_data(file_path):
    try:
        # XML-Datei parsen
        tree = etree.parse(file_path)
        root = tree.getroot()

        # Relevante Informationen sammeln
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
                short_text = item.find(".//{http://www.gaeb.de/GAEB_DA_XML/DA83/3.2}ShortText")
                pos_info = f"Position {pos_id}:"
                if short_text is not None:
                    pos_info += f" {short_text.text.strip()}"
                result.append(pos_info)

        return "\n".join(result)

    except Exception as e:
        return f"Fehler bei der Verarbeitung der Datei: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Fehler: Kein Pfad zur X83-Datei angegeben.")
        sys.exit(1)

    file_path = sys.argv[1]
    print(extract_x83_data(file_path))

