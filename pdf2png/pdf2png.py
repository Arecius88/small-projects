import os
from pdf2image import convert_from_path

def pdf_to_png(pdf_path: str, output_folder: str = ".", dpi: int = 300):
    """
    Konverterar en PDF till en PNG per sida.

    Args:
        pdf_path (str): Sökväg till PDF-filen.
        output_folder (str): Var PNG-filerna ska sparas.
        dpi (int): Upplösning i dots-per-inch (standard: 300)
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Filen '{pdf_path}' hittades inte.")
        return

    try:
        print("📄 Läser PDF...")
        images = convert_from_path(pdf_path, dpi=dpi)

        basename = os.path.splitext(os.path.basename(pdf_path))[0]
        for i, image in enumerate(images, start=1):
            output_path = os.path.join(output_folder, f"{basename}_page_{i}.png")
            image.save(output_path, "PNG")
            print(f"✅ Sparade: {output_path}")

        print(f"✅ Alla sidor konverterade, från {pdf_path}.")
    except Exception as e:
        print(f"❌ Ett fel inträffade: {e}")


if __name__ == "__main__":
    # Ändra denna sökväg till din egen PDF
    pdf_path = "/home/arecius/Documents/SynologyDrive/LinusDokument/RPG/MutantÅrNoll/Mutanten/Zonen/spelarkartor_zonkompendium.pdf"    

    lst_of_paths =[]
    for i in range(1,6):
        lst_of_paths.append(f"/home/arecius/Documents/SynologyDrive/LinusDokument/RPG/MutantÅrNoll/Mutanten/Zonen/spelarkartor_zonkompendium{i}.pdf")
    
    for path_str in lst_of_paths:        
        pdf_to_png(pdf_path=path_str, output_folder="/home/arecius/Documents/SynologyDrive/ObsidianVaults/RPGMutant/z_Assets/Bilder/SärkskildaSektorer/")
