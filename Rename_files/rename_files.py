import os

def get_common_prefix(strings):
    """Returnera gemensam inledning på en lista med strängar"""
    if not strings:
        return ""
    return os.path.commonprefix(strings)

def rename_files_in_directory(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        print("Inga filer hittades i mappen.")
        return

    print("\n📂 Filer i mappen:")
    for f in files:
        print(f" - {f}")

    # === Identifiera gemensam prefix ===
    common_prefix = get_common_prefix(files)
    remove_prefix = False

    if common_prefix:
        print(f"\n🔍 Gemensam start: '{common_prefix}'")
        remove_prefix = input("Vill du ta bort denna del? (j/n): ").strip().lower() == 'j'

    # === Användardefinierad suffixersättning ===
    suffix_to_replace = input("\nAnge suffix du vill ersätta (ex: _klar.txt): ").strip()
    replacement_suffix = input("Ersätt med (tryck Enter för att ta bort helt): ")

    # === Ersätt tecken ===
    from_char = input("\nVilket tecken vill du ersätta (ex: _)? Lämna tomt för att hoppa över: ").strip()
    to_char = None
    if from_char:
        to_char = input("Ersätt med vad (tryck på mellanslag för mellanslag): ")
        if to_char == "":
            print("⚠️  Inget ersättningstecken angavs – åtgärden hoppas över.")
            from_char = None

    # === Förhandsgranskning ===
    print("\n💡 Förhandsgranskning av nya filnamn:")
    new_names = {}
    for filename in files:
        new_name = filename
        if remove_prefix and new_name.startswith(common_prefix):
            new_name = new_name[len(common_prefix):]
        if suffix_to_replace and new_name.endswith(suffix_to_replace):
            new_name = new_name[:-len(suffix_to_replace)] + replacement_suffix
        if from_char and to_char is not None:
            new_name = new_name.replace(from_char, to_char)
        new_names[filename] = new_name
        print(f"'{filename}' ➜ '{new_name}'")

    confirm = input("\n⚠️ Vill du byta namn på filerna? (j/n): ").strip().lower()
    if confirm == 'j':
        for old, new in new_names.items():
            os.rename(os.path.join(directory, old), os.path.join(directory, new))
        print("✅ Filerna har bytt namn.")
    else:
        print("❌ Inga ändringar gjordes.")

if __name__ == "__main__":
    dir_path = input("📁 Ange sökväg till mapp med filer: ").strip()
    if os.path.isdir(dir_path):
        rename_files_in_directory(dir_path)
    else:
        print("🚫 Ogiltig sökväg.")
