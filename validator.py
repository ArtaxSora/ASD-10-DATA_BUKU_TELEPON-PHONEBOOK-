# ============================================================
# validator.py
# Hari 1 – Anggota 2
# Tugas: Validasi & sanitasi semua input pengguna
# ============================================================

from __future__ import annotations
import re


class Validator:
    """
    Kumpulan metode statis untuk validasi input pengguna.

    Setiap metode validate_*() mengembalikan tuple (bool, str):
        - bool : True  = valid
        - str  : pesan error jika tidak valid, "" jika valid
    """

    # ── Nama ────────────────────────────────────────────────
    @staticmethod
    def validate_name(name: str) -> tuple[bool, str]:
        name = name.strip()
        if not name:
            return False, "Nama tidak boleh kosong."
        if len(name) < 2:
            return False, "Nama minimal 2 karakter."
        if len(name) > 60:
            return False, "Nama maksimal 60 karakter."
        if not re.match(r"^[a-zA-Z0-9\s\-'\.]+$", name):
            return False, "Nama hanya boleh berisi huruf, angka, spasi, tanda hubung, apostrof, dan titik."
        return True, ""

    # ── Nomor Telepon ────────────────────────────────────────
    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, str]:
        """
        Mengembalikan (True, nomor_bersih) jika valid.
        nomor_bersih = hanya digit (+ boleh di awal).
        """
        phone = phone.strip()
        if not phone:
            return False, "Nomor telepon tidak boleh kosong."
        # Normalisasi: hapus spasi, tanda hubung, tanda kurung
        cleaned = re.sub(r"[\s\-\(\)]", "", phone)
        # Boleh diawali '+'
        digits_only = cleaned.lstrip("+")
        if not digits_only.isdigit():
            return False, "Nomor telepon hanya boleh berisi angka (dan '+' di awal)."
        if len(digits_only) < 8 or len(digits_only) > 15:
            return False, "Nomor telepon harus 8–15 digit."
        return True, cleaned


    # ── Pilihan menu ─────────────────────────────────────────
    @staticmethod
    def validate_menu(choice: str, valid_options: list | tuple | set) -> tuple[bool, str]:
        if choice not in valid_options:
            opts = ", ".join(str(o) for o in valid_options)
            return False, f"Pilihan tidak valid. Pilih salah satu dari: [{opts}]"
        return True, ""

    # ── Sanitasi teks bebas ──────────────────────────────────
    @staticmethod
    def sanitize(text: str) -> str:
        """
        Bersihkan karakter berbahaya dari teks bebas (catatan, dsb).
        - Trim whitespace
        - Ganti kutip ganda → kutip tunggal (aman untuk CSV)
        - Hapus karakter kontrol
        """
        if not text:
            return ""
        text = text.strip()
        text = text.replace('"', "'")
        text = re.sub(r"[\x00-\x1f\x7f]", "", text)   # hapus kontrol ASCII
        return text

    # ── Helper: input berulang sampai valid ──────────────────
    @staticmethod
    def prompt_until_valid(
        prompt_text: str,
        validate_fn,          # callable → (bool, str)
        allow_empty: bool = False,
    ) -> str:
        """
        Tampilkan prompt terus-menerus sampai input valid.

        Args:
            prompt_text  : Teks yang ditampilkan sebelum input
            validate_fn  : Fungsi validasi (mengembalikan (bool, str))
            allow_empty  : Jika True dan input kosong, langsung kembalikan ""

        Returns:
            Nilai yang sudah divalidasi (sudah di-'cleaned' oleh validate_fn)
        """
        while True:
            raw = input(prompt_text).strip()
            if allow_empty and raw == "":
                return ""
            ok, result = validate_fn(raw)
            if ok:
                # Beberapa validator mengembalikan nilai yang sudah dibersihkan
                return result if result else raw
            print(f"  ❌ {result}")


# ── Unit-test sederhana ─────────────────────────────────────
# if __name__ == "__main__":
#     tests = [
#         ("validate_name",  Validator.validate_name,  [("", False), ("A", False), ("Budi Santoso", True), ("123!@#", False)]),
#         ("validate_phone", Validator.validate_phone, [("", False), ("123", False), ("08123456789", True), ("+628123456789", True)]),
#     ]
#     all_ok = True
#     for fn_name, fn, cases in tests:
#         for val, expected_ok in cases:
#             ok, msg = fn(val)
#             status = "✅" if ok == expected_ok else "❌"
#             if ok != expected_ok:
#                 all_ok = False
#             print(f"  {status} {fn_name}({val!r}) → ok={ok}  msg={msg!r}")
#     print("\n✅ validator.py OK" if all_ok else "\n❌ Ada test yang gagal!")
