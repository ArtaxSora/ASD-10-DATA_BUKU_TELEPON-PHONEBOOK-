# ============================================================
# phonebook_app.py
# Hari 3–4 – Semua Anggota
#   Anggota 1: handle_add, handle_view, handle_sort
#   Anggota 2: handle_search, handle_edit
#   Anggota 3: handle_delete, handle_history, UI/UX polish
# ============================================================

from __future__ import annotations
import os
import sys
from datetime import datetime

from contact      import Contact
from linked_list  import LinkedList
from stack        import Stack
from file_handler import FileHandler
from validator    import Validator


# ══════════════════════════════════════════════════════════════
#  Utilitas tampilan
# ══════════════════════════════════════════════════════════════

def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _divider(char: str = "─", width: int = 48) -> str:
    return "  " + char * width


def _banner() -> None:
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║       📒  PHONEBOOK CLI  ─  Kelompok 10     ║")
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

    # ────────────────────────────────────────────────────────
    #  1. TAMBAH KONTAK
    #  Anggota 1
    # ────────────────────────────────────────────────────────
    def handle_add(self) -> None:
        _section("📝  TAMBAH KONTAK BARU")

        # Nama
        name = Validator.prompt_until_valid(
            "  Nama       : ", Validator.validate_name
        )
        if self.phonebook.search_by_name(name):
            print(f"  ❌ Kontak dengan nama '{name}' sudah ada.")
            _pause(); return

        # Telepon
        phone = Validator.prompt_until_valid(
            "  Telepon    : ", Validator.validate_phone
        )

        # Email (opsional)
        email = Validator.prompt_until_valid(
            "  Email      : ", Validator.validate_email, allow_empty=True
        )

        # Catatan (opsional, bebas)
        note = Validator.sanitize(input("  Catatan    : ").strip())

        contact = Contact(
            name  = Validator.sanitize(name),
            phone = phone,
            email = email,
            note  = note,
        )
        self.phonebook.insert_sorted(contact)
        self._save()
        self._log(f"ADD     → '{name}'")

        print(f"\n  ✅ Kontak '{name}' berhasil ditambahkan! "
              f"(Total: {len(self.phonebook)} kontak)")
        _pause()

    # ────────────────────────────────────────────────────────
    #  2. TAMPILKAN SEMUA KONTAK
    #  Anggota 1
    # ────────────────────────────────────────────────────────
    def handle_view(self) -> None:
        _section(f"📋  SEMUA KONTAK  ({len(self.phonebook)} total)")
        self.phonebook.display_all()
        _pause()

    # ────────────────────────────────────────────────────────
    #  3. CARI KONTAK
    #  Anggota 2
    # ────────────────────────────────────────────────────────
    def handle_search(self) -> None:
        _section("🔍  CARI KONTAK")
        print("  Metode pencarian:")
        print("  1. Nama  → Binary Search  O(log n)")
        print("  2. Nomor → Linear Search  O(n)")
        method = input("  Pilih [1/2]: ").strip()

        if method == "1":
            keyword = input("  Masukkan nama: ").strip()
            if not keyword:
                print("  ❌ Keyword tidak boleh kosong.")
                _pause(); return

            # Coba exact Binary Search lebih dulu
            found = self.phonebook.search_by_name(keyword)
            if found:
                print(f"\n  ✅ Ditemukan (Binary Search – exact match):")
                self.phonebook._print_table([found])
                self._log(f"SEARCH  → nama='{keyword}' (ditemukan)")
            else:
                # Fallback: partial linear search
                suggestions = self.phonebook.search_by_name_partial(keyword)
                if suggestions:
                    print(f"\n  ℹ️  Tidak ada nama persis. "
                          f"Ditemukan {len(suggestions)} kontak yang mirip:")
                    self.phonebook._print_table(suggestions)
                    self._log(f"SEARCH  → nama='{keyword}' ({len(suggestions)} mirip)")
                else:
                    print(f"  ❌ Tidak ada kontak dengan nama '{keyword}'.")
                    self._log(f"SEARCH  → nama='{keyword}' (tidak ditemukan)")

        elif method == "2":
            raw = input("  Masukkan nomor telepon: ").strip()
            ok, phone = Validator.validate_phone(raw)
            if not ok:
                print(f"  ❌ {phone}")
                _pause(); return

            found = self.phonebook.search_by_phone(phone)
            if found:
                print(f"\n  ✅ Ditemukan (Linear Search):")
                self.phonebook._print_table([found])
                self._log(f"SEARCH  → nomor='{phone}' (ditemukan)")
            else:
                print(f"  ❌ Nomor '{phone}' tidak ditemukan.")
                self._log(f"SEARCH  → nomor='{phone}' (tidak ditemukan)")
        else:
            print("  ❌ Pilihan tidak valid.")

        _pause()

    # ────────────────────────────────────────────────────────
    #  4. EDIT KONTAK
    #  Anggota 2
    # ────────────────────────────────────────────────────────
    def handle_edit(self) -> None:
        _section("✏️  EDIT KONTAK")

        name    = input("  Nama kontak yang akan diedit: ").strip()
        contact = self._resolve_contact(name)
        if contact is None:
            _pause(); return

        print(f"\n  Data saat ini:")
        self.phonebook._print_table([contact])
        print("\n  [Tekan Enter untuk melewati / tidak mengubah field]")

        # ── Nama baru ──
        new_name_raw = input(f"  Nama baru  [{contact.name}]: ").strip()
        new_name: str | None = None
        if new_name_raw:
            ok, msg = Validator.validate_name(new_name_raw)
            if not ok:
                print(f"  ❌ {msg}"); _pause(); return
            new_name = Validator.sanitize(new_name_raw)

        # ── Telepon baru ──
        new_phone_raw = input(f"  Telepon    [{contact.phone}]: ").strip()
        new_phone: str | None = None
        if new_phone_raw:
            ok, result = Validator.validate_phone(new_phone_raw)
            if not ok:
                print(f"  ❌ {result}"); _pause(); return
            new_phone = result

        # ── Email baru ──
        new_email_raw = input(f"  Email      [{contact.email}]: ").strip()
        new_email: str | None = None
        if new_email_raw:
            ok, result = Validator.validate_email(new_email_raw)
            if not ok:
                print(f"  ❌ {result}"); _pause(); return
            new_email = result

        # ── Catatan baru ──
        new_note_raw = input(f"  Catatan    [{contact.note}]: ").strip()
        new_note: str | None = Validator.sanitize(new_note_raw) if new_note_raw else None

        success, msg = self.phonebook.update(
            name,
            new_name  = new_name,
            new_phone = new_phone,
            new_email = new_email,
            new_note  = new_note,
        )

        if success:
            self._save()
            final = new_name if new_name else name
            self._log(f"EDIT    → '{name}' ⟶ '{final}'")
            print(f"\n  ✅ {msg}")
        else:
            print(f"\n  ❌ {msg}")

        _pause()

    # ────────────────────────────────────────────────────────
    #  5. HAPUS KONTAK
    #  Anggota 3
    # ────────────────────────────────────────────────────────
    def handle_delete(self) -> None:
        _section("🗑️  HAPUS KONTAK")

        name    = input("  Nama kontak yang akan dihapus: ").strip()
        contact = self._resolve_contact(name)
        if contact is None:
            _pause(); return

        print(f"\n  Kontak yang akan dihapus:")
        self.phonebook._print_table([contact])

        confirm = input("\n  ⚠️  Yakin ingin menghapus? [y/N]: ").strip().lower()
        if confirm == "y":
            deleted = self.phonebook.delete(contact.name)
            if deleted:
                self._save()
                self._log(f"DELETE  → '{contact.name}'")
                print(f"\n  ✅ Kontak '{contact.name}' berhasil dihapus.")
            else:
                print(f"\n  ❌ Gagal menghapus kontak.")
        else:
            print("  ℹ️  Penghapusan dibatalkan.")

        _pause()

    # ────────────────────────────────────────────────────────
    #  6. SORT & TAMPILKAN
    #  Anggota 1
    # ────────────────────────────────────────────────────────
    def handle_sort(self) -> None:
        _section("📊  URUTKAN & TAMPILKAN")
        print("  Pilih urutan tampilan:")
        print("  1. Nama A → Z  (default)")
        print("  2. Nama Z → A")
        print("  3. Nomor Telepon (ascending)")
        choice = input("  Pilih [1–3]: ").strip()

        if choice == "1":
            data  = self.phonebook.get_sorted(reverse=False, by="name")
            label = "Nama A → Z"
        elif choice == "2":
            data  = self.phonebook.get_sorted(reverse=True, by="name")
            label = "Nama Z → A"
        elif choice == "3":
            data  = self.phonebook.get_sorted(reverse=False, by="phone")
            label = "Nomor Telepon ↑"
        else:
            print("  ❌ Pilihan tidak valid.")
            _pause(); return

        print(f"\n  📊 Urutan: {label}  ({len(data)} kontak)\n")
        self.phonebook._print_table(data)
        _pause()

    # ────────────────────────────────────────────────────────
    #  7. RIWAYAT OPERASI
    #  Anggota 3
    # ────────────────────────────────────────────────────────
    def handle_history(self) -> None:
        _section(f"📜  RIWAYAT OPERASI  ({len(self.history)}/10 slot terisi)")
        items = self.history.to_list()
        if not items:
            print("  [Belum ada riwayat operasi]")
        else:
            for i, item in enumerate(items, 1):
                mark = " ← terbaru" if i == 1 else ""
                print(f"  {i:2}. {item}{mark}")
        _pause()

    # ────────────────────────────────────────────────────────
    #  8. BACKUP / EKSPOR
    #  Anggota 3
    # ────────────────────────────────────────────────────────
    def handle_backup(self) -> None:
        _section("💾  BACKUP / EKSPOR DATA")
        print("  1. Buat backup otomatis (timestamp)")
        print("  2. Ekspor ke nama file kustom")
        choice = input("  Pilih [1/2]: ").strip()

        if choice == "1":
            self.file_handler.backup()
            self._log("BACKUP  → backup otomatis")
        elif choice == "2":
            filename = input("  Nama file tujuan (contoh: backup.csv): ").strip()
            if not filename.endswith(".csv"):
                filename += ".csv"
            self.file_handler.export(filename)
            self._log(f"EXPORT  → '{filename}'")
        else:
            print("  ❌ Pilihan tidak valid.")

        _pause()

    # ────────────────────────────────────────────────────────
    #  9. KELUAR
    # ────────────────────────────────────────────────────────
    def _exit(self) -> None:
        print()
        print("  👋 Terima kasih telah menggunakan PhoneBook CLI!")
        info = self.file_handler.file_info()
        if info.get("exists"):
            print(f"  💾 Data tersimpan di: {info['path']}")
        print("  Sampai jumpa!\n")

    # ────────────────────────────────────────────────────────
    #  HELPER PRIVAT: resolve kontak dengan fallback partial
    # ────────────────────────────────────────────────────────
    def _resolve_contact(self, name: str) -> Contact | None:
        """
        Cari kontak dengan nama eksak.
        Jika tidak ada, tampilkan saran partial dan minta nama ulang.
        Return Contact atau None.
        """
        contact = self.phonebook.search_by_name(name)
        if contact:
            return contact

        suggestions = self.phonebook.search_by_name_partial(name)
        if suggestions:
            print(f"\n  ℹ️  '{name}' tidak ditemukan persis. "
                  f"Kontak yang mirip:")
            self.phonebook._print_table(suggestions)
            exact = input("\n  Masukkan nama lengkap (atau Enter untuk batal): ").strip()
            if not exact:
                return None
            contact = self.phonebook.search_by_name(exact)
            if contact:
                return contact

        print(f"  ❌ Kontak '{name}' tidak ditemukan.")
        return None


# ══════════════════════════════════════════════════════════════
#  Entry-point
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "phonebook.csv"
    app = PhoneBookApp(csv_file=csv_file)
    app.run()
