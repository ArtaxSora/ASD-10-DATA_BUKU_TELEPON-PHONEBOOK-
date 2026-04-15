# ============================================================
# contact.py
# Kerjaan Nabil
# Tugas: Buat class Contact sebagai Node Linked List
# ============================================================

# TODO menambahkan

class Contact:
    def __init__(self, name: str, phone: str, note: str = ""):
        self.name  = name.strip()
        self.phone = phone.strip()
        self.note  = note.strip()
        self.next: "Contact | None" = None   # Linked-list pointer

    # ── Representasi ────────────────────────────────────────
    def __str__(self) -> str:
        return (
            f"Contact(name='{self.name}', phone='{self.phone}', "
            f"note='{self.note}')"
        )

    def __repr__(self) -> str:
        return self.__str__()

    # ── Serialisasi ─────────────────────────────────────────
    def to_dict(self) -> dict:
        """Konversi ke dictionary untuk keperluan CSV / display."""
        return {
            "name":  self.name,
            "phone": self.phone,
            "note":  self.note,
        }

    # ── Perbandingan (berguna untuk sorting) ────────────────
    def __lt__(self, other: "Contact") -> bool:
        return self.name.lower() < other.name.lower()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Contact):
            return False
        return self.name.lower() == other.name.lower()


# ── Unit-test sederhana (jalankan: python contact.py) ──────
if __name__ == "__main__":
    c1 = Contact("Budi Santoso", "081234567890", "Teman kuliah")
    c2 = Contact("Ani Rahayu",   "087654321098")
    print(c1)
    print(c2)
    print("c2 < c1 ?", c2 < c1)           # True  (Ani < Budi)
    print("dict:", c1.to_dict())
    print("✅ contact.py OK")
