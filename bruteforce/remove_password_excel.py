import os
import zipfile
import shutil
import tempfile
import re

def remove_protection_tags(xml_text):
    """Tar bort olika typer av skyddstaggar från XML"""
    xml_text = re.sub(r'<sheetProtection[^>]*/>', '', xml_text)
    xml_text = re.sub(r'<workbookProtection[^>]*/>', '', xml_text)
    xml_text = re.sub(r'<protection[^>]*/>', '', xml_text)
    return xml_text

def process_xlsx_file(file_path):
    print(f"🔍 Bearbetar: {file_path}")
    with tempfile.TemporaryDirectory() as tmpdir:
        # Extrahera xlsx (zip) till tempmapp
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        # Lista på XML-filer som kan innehålla skyddstaggar
        candidate_files = []

        # Sök efter relevanta filer
        for root, _, files in os.walk(tmpdir):
            for file in files:
                if file.startswith('sheet') and file.endswith('.xml'):
                    candidate_files.append(os.path.join(root, file))
                elif file in ('workbook.xml', 'styles.xml'):
                    candidate_files.append(os.path.join(root, file))

        # Ta bort skyddstaggar
        for file in candidate_files:
            with open(file, 'r', encoding='utf-8') as f:
                xml = f.read()
            cleaned_xml = remove_protection_tags(xml)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(cleaned_xml)

        # Skapa nytt xlsx (zip) från mapp
        output_path = file_path.replace('.xlsx', '_unprotected.xlsx')
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for root, _, files in os.walk(tmpdir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, tmpdir)
                    zip_out.write(full_path, rel_path)

        print(f"✅ Skydd borttaget: {output_path}")

def process_folder(folder_path):
    print(f"\n📁 Söker efter .xlsx-filer i: {folder_path}\n")
    for file in os.listdir(folder_path):
        if file.endswith('.xlsx'):
            full_path = os.path.join(folder_path, file)
            process_xlsx_file(full_path)

if __name__ == "__main__":
    folder = input("Ange sökväg till mapp med .xlsx-filer: ").strip('"')
    if os.path.isdir(folder):
        process_folder(folder)
    else:
        print("🚫 Ogiltig mapp.")
