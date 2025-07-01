import uno
import itertools
import string
import os
from com.sun.star.beans import PropertyValue
from com.sun.star.connection import NoConnectException

# === Inställningar ===
file_path = os.path.abspath("file-path-here")  # <-- Ändra till din fil
charset = string.ascii_letters + string.digits + string.punctuation
max_length = 10
tested_dir = "tested_passwords"
found_dir = "found_passwords"
batch_write_interval = 500  # <-- Ändrad till 500

# === Skapa mappar om de inte finns ===
os.makedirs(tested_dir, exist_ok=True)
os.makedirs(found_dir, exist_ok=True)

def get_uno_ctx():
    """Anslut till redan körande LibreOffice"""
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx)
    try:
        context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        return context
    except NoConnectException:
        raise RuntimeError("Kunde inte ansluta till LibreOffice. Är soffice igång i headless-läge?")

def open_calc_doc(ctx, path):
    """Öppna dokument i headless-läge"""
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    file_url = uno.systemPathToFileUrl(path)
    props = [PropertyValue(Name="Hidden", Value=True)]
    return desktop.loadComponentFromURL(file_url, "_blank", 0, tuple(props))

def password_generator():
    """Genererar alla kombinationer av lösenord"""
    for length in range(1, max_length + 1):
        for pwd_tuple in itertools.product(charset, repeat=length):
            yield ''.join(pwd_tuple)

def select_sheet(doc):
    """Visa lista över blad och låt användaren välja"""
    print("\nTillgängliga blad:")
    for idx, name in enumerate(doc.Sheets.ElementNames):
        print(f"{idx+1}. {name}")
    while True:
        try:
            choice = int(input("Välj ett blad att testa (nummer): "))
            if 1 <= choice <= len(doc.Sheets.ElementNames):
                return doc.Sheets.ElementNames[choice - 1]
        except ValueError:
            pass
        print("Ogiltigt val, försök igen.")

# === Start ===
ctx = get_uno_ctx()
doc = open_calc_doc(ctx, file_path)

selected_sheet = select_sheet(doc)
print(f"\n🔍 Brute-force startar för blad: {selected_sheet}")  

sheet = doc.Sheets.getByName(selected_sheet)

# === Loggfiler ===
tested_log = os.path.join(tested_dir, f"{selected_sheet}.txt")
found_log = os.path.join(found_dir, f"{selected_sheet}.txt")

tested = set()
if os.path.exists(tested_log):
    with open(tested_log, "r", encoding="utf-8") as f:
        tested = set(line.strip() for line in f)

tested_buffer = []
counter = 0

try:
    for pwd in password_generator():
        if pwd in tested:
            continue

        counter += 1
        if counter % 100 == 0:
            print(f"🔄 Testat {counter} lösenord – senaste: {pwd}", end="\r", flush=True)

        try:
            sheet.unprotect(pwd)
            if not sheet.IsProtected:
                print(f"\n✅ Rätt lösenord för '{selected_sheet}': {pwd}")
                with open(found_log, "w", encoding="utf-8") as f:
                    f.write(pwd + "\n")
                break
        except:
            pass

        tested.add(pwd)
        tested_buffer.append(pwd)

        if len(tested_buffer) >= batch_write_interval:
            with open(tested_log, "a", encoding="utf-8") as f:
                for entry in tested_buffer:
                    f.write(entry + "\n")
            tested_buffer = []

except KeyboardInterrupt:
    print("\n⛔ Avbrutet av användaren – sparar osparade lösenord...")
    if tested_buffer:
        with open(tested_log, "a", encoding="utf-8") as f:
            for entry in tested_buffer:
                f.write(entry + "\n")
    print("✅ Alla testade lösenord har sparats. Avslutar.")

# === Avslutande skrivning om scriptet nådde slutet utan avbrott ===
if tested_buffer:
    with open(tested_log, "a", encoding="utf-8") as f:
        for entry in tested_buffer:
            f.write(entry + "\n")
