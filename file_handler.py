# ============================================================
# file_handler.py
# Kerjaan arya
# Tugas: Membaca & menyimpan data kontak ke/dari file CSV
# ============================================================

from __future__ import annotations
import csv
import os
import shutil
from datetime import datetime
from contact import Contact


class FileHandler:

    FIELDS = ("name", "phone", "note")

    def __init__(self, filename: str = "phonebook.csv"):
        self.filename = filename

    # ── Inisialisasi file ────────────────────────────────────
    def _init_file(self) -> None:
        """Buat file CSV baru dengan header jika belum ada."""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDS)
                writer.writeheader()

    # ── LOAD ────────────────────────────────────────────────
    def load(self) -> list[Contact]:
        """
        Baca file CSV dan kembalikan list Contact.
        Baris yang tidak lengkap (tanpa name/phone) diabaikan.
        """
        self._init_file()
        contacts: list[Contact] = []

        try:
            with open(self.filename, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader, start=2):
                    name  = row.get("name", "").strip()
                    phone = row.get("phone", "").strip()
                    if not name or not phone:
                        print(f"  [SKIP] Baris {i}: name/phone kosong → dilewati")
                        continue
                    contacts.append(Contact(
                        name  = name,
                        phone = phone,
                        note  = row.get("note",  "").strip(),
                    ))
        except FileNotFoundError:
            pass   # File belum ada; kembalikan list kosong
        except Exception as exc:
            print(f"  [WARNING] Gagal membaca '{self.filename}': {exc}")

        return contacts

    # ── SAVE ─────────────────────────────────────────────────
    def save(self, contacts: list[Contact]) -> bool:
        """
        Simpan list Contact ke file CSV.
        Tulis ke file sementara dulu, lalu rename (atomic write).
        """
        tmp_path = self.filename + ".tmp"
        try:
            with open(tmp_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDS)
                writer.writeheader()
                for c in contacts:
                    writer.writerow(c.to_dict())
            # Ganti file asli dengan file sementara (atomic)
            shutil.move(tmp_path, self.filename)
            return True
        except Exception as exc:
            print(f"  [ERROR] Gagal menyimpan '{self.filename}': {exc}")
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return False

    # ── EXPORT ──────────────────────────────────────────────
    def export(self, export_path: str) -> bool:
        """
        Ekspor data ke file CSV lain (backup / berbagi).
        Return True jika berhasil.
        """
        contacts = self.load()
        orig     = self.filename
        self.filename = export_path
        ok = self.save(contacts)
        self.filename = orig
        if ok:
            print(f"  ✅ Data berhasil diekspor ke '{export_path}'")
        return ok


# ── Unit-test sederhana ─────────────────────────────────────
# if __name__ == "__main__":
#     import tempfile, os

#     with tempfile.TemporaryDirectory() as tmp:
#         downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
#         export_path = os.path.join(downloads_folder, "export_kontak_arya.csv")
#         fh   = FileHandler(filename="test_phonebook.csv")

#         contacts = [
#             Contact("Ani",  "082",  "teman"),
#             Contact("Budi", "081", "kolega"),
#         ]
#         assert fh.save(contacts), "save gagal"
#         loaded = fh.load()
#         assert len(loaded) == 2, f"load: dapat {len(loaded)}, harap 2"
#         assert loaded[0].name == "Ani"
#         print("  ✅ save/load OK")

#         export_path = os.path.join(tmp, "export.csv")
#         fh.export(export_path)
#         assert os.path.exists(export_path), "export gagal"
#         print("  ✅ export OK")

#     print("✅ file_handler.py OK")
