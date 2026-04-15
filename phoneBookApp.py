import os
from datetime import datetime

from linked_list  import LinkedList
from stack        import Stack
from file_handler import FileHandler

def _banner() -> None:
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║        📒 PHONEBOOK CLI ─ Kelompok 10       ║")
    print("  ║     Sistem Manajemen Buku Telepon Terminal   ║")
    print("  ╚══════════════════════════════════════════════╝")


def _menu() -> None:
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║            📋  MENU UTAMA                   ║")
    print("  ╠══════════════════════════════════════════════╣")
    print("  ║  1. 📝  Tambah Kontak Baru                  ║")
    print("  ║  2. 📋  Tampilkan Semua Kontak              ║")
    print("  ║  3. 🔍  Cari Kontak                         ║")
    print("  ║  4. ✏️   Edit Kontak                         ║")
    print("  ║  5. 🗑️   Hapus Kontak                        ║")
    print("  ║  6. 📊  Urutkan & Tampilkan                 ║")
    print("  ║  7. 📜  Riwayat Operasi (History)           ║")
    print("  ║  8. 💾  Backup / Ekspor Data                ║")
    print("  ║  9. 🚪  Keluar                               ║")
    print("  ╚══════════════════════════════════════════════╝")

def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _divider(char: str = "─", width: int = 48) -> str:
    return "  " + char * width

def _pause() -> None:
    input("\n  ↵  Tekan Enter untuk kembali ke menu...")


def _section(title: str) -> None:
    print()
    print(_divider("═"))
    print(f"  {title}")
    print(_divider("─"))

# ══════════════════════════════════════════════════════════════
#  Kelas utama aplikasi
# ══════════════════════════════════════════════════════════════

class PhoneBookApp:
    """
    Kelas orkestrasi utama: menghubungkan LinkedList, Stack,
    FileHandler, dan Validator menjadi satu aplikasi CLI.
    """

    def __init__(self, csv_file: str = "phonebook.csv"):
        self.phonebook    = LinkedList()
        self.history      = Stack(max_size=10)
        self.file_handler = FileHandler(filename=csv_file)
        self._load_on_startup()

    # ── Startup & shutdown ───────────────────────────────────
    def _load_on_startup(self) -> None:
        contacts = self.file_handler.load()
        for c in contacts:
            self.phonebook.insert_sorted(c)
        total = len(self.phonebook)
        if total:
            print(f"  ✅ {total} kontak dimuat dari '{self.file_handler.filename}'.")
        else:
            print(f"  ℹ️  Tidak ada kontak sebelumnya. Mulai dengan kontak baru!")

    def _save(self) -> None:
        self.file_handler.save(self.phonebook.get_all())

    def _log(self, action: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self.history.push(f"[{ts}] {action}")

    # ── Loop utama ───────────────────────────────────────────
    def run(self) -> None:
        _clear()
        _banner()
        self._load_on_startup()   # Tampilkan info di bawah banner

        HANDLERS = {
            "1": self.handle_add,
            "2": self.handle_view,
            "3": self.handle_search,
            "4": self.handle_edit,
            "5": self.handle_delete,
            "6": self.handle_sort,
            "7": self.handle_history,
            "8": self.handle_backup,
            "9": self._exit,
        }

        while True:
            _menu()
            try:
                choice = input("\n  Pilih menu [1-9]: ").strip()
            except (KeyboardInterrupt, EOFError):
                self._exit()
                return

            if choice in HANDLERS:
                HANDLERS[choice]()
                if choice == "9":
                    return
            else:
                print("  ❌ Pilihan tidak valid. Masukkan angka 1–9.")