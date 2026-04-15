# ============================================================
# linked_list.py
# Hari 2 – Anggota 3
# Tugas: Sorted Linked List lengkap + Binary & Linear Search
# ============================================================

from __future__ import annotations
from contact import Contact


class LinkedList:
    """
    Sorted Linked List untuk menyimpan kontak secara alfabetis (A-Z).

    Invariant: Setiap kali insert, kontak disisipkan di posisi yang
    tepat sehingga urutan A-Z selalu terjaga tanpa perlu sort manual.

    Kompleksitas:
        insert_sorted  → O(n)
        delete         → O(n)
        search_by_name → O(log n)  [Binary Search via array]
        search_by_phone→ O(n)      [Linear Search]
        get_all        → O(n)
    """

    def __init__(self):
        self.head: Contact | None = None
        self._size: int           = 0

    # ── Properti ────────────────────────────────────────────
    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.head is None

    # ── INSERT ───────────────────────────────────────────────
    def insert_sorted(self, contact: Contact) -> bool:
        """
        Sisipkan kontak di posisi urut A-Z berdasarkan nama.
        Return False jika nama sudah ada (duplikat).
        """
        contact.next = None   # Pastikan pointer bersih

        # List kosong
        if self.head is None:
            self.head = contact
            self._size += 1
            return True

        # Sisip di depan (lebih kecil dari head)
        if contact.name.lower() < self.head.name.lower():
            contact.next = self.head
            self.head    = contact
            self._size  += 1
            return True

        # Duplikat di head
        if contact.name.lower() == self.head.name.lower():
            return False

        # Cari posisi sisip di tengah/akhir
        cur = self.head
        while cur.next:
            if cur.next.name.lower() == contact.name.lower():
                return False                          # Duplikat
            if cur.next.name.lower() > contact.name.lower():
                break
            cur = cur.next

        contact.next = cur.next
        cur.next     = contact
        self._size  += 1
        return True

    # ── DELETE ───────────────────────────────────────────────
    def delete(self, name: str) -> Contact | None:
        """
        Hapus kontak berdasarkan nama (case-insensitive).
        Kembalikan node yang dihapus, atau None jika tidak ada.
        """
        if self.head is None:
            return None

        name_lower = name.strip().lower()

        # Hapus head
        if self.head.name.lower() == name_lower:
            deleted      = self.head
            self.head    = self.head.next
            deleted.next = None
            self._size  -= 1
            return deleted

        cur = self.head
        while cur.next:
            if cur.next.name.lower() == name_lower:
                deleted      = cur.next
                cur.next     = deleted.next
                deleted.next = None
                self._size  -= 1
                return deleted
            cur = cur.next

        return None

    # ── SEARCH: Binary Search (nama eksak) ──────────────────
    def search_by_name(self, name: str) -> Contact | None:
        """
        Binary Search untuk nama eksak (case-insensitive).
        Data sudah sorted → konversi ke array, lalu binary search.
        Kompleksitas: O(n) konversi + O(log n) search = O(n).
        """
        arr        = self.get_all()
        name_lower = name.strip().lower()
        left, right = 0, len(arr) - 1

        while left <= right:
            mid      = (left + right) // 2
            mid_name = arr[mid].name.lower()
            if mid_name == name_lower:
                return arr[mid]
            elif mid_name < name_lower:
                left = mid + 1
            else:
                right = mid - 1

        return None

    # ── SEARCH: Partial (Linear, untuk saran) ───────────────
    def search_by_name_partial(self, keyword: str) -> list[Contact]:
        """
        Linear Search pencarian sebagian nama (case-insensitive).
        Berguna untuk fitur 'did you mean?' / saran kontak.
        """
        results    = []
        kw         = keyword.strip().lower()
        cur        = self.head
        while cur:
            if kw in cur.name.lower():
                results.append(cur)
            cur = cur.next
        return results

    # ── SEARCH: Linear Search (nomor telepon) ───────────────
    def search_by_phone(self, phone: str) -> Contact | None:
        """
        Linear Search berdasarkan nomor telepon (exact match).
        Kompleksitas: O(n).
        """
        phone = phone.strip()
        cur   = self.head
        while cur:
            if cur.phone == phone:
                return cur
            cur = cur.next
        return None

    # ── UPDATE ───────────────────────────────────────────────
    def update(
        self,
        name:      str,
        new_name:  str | None = None,
        new_phone: str | None = None,
        
        new_note:  str | None = None,
    ) -> tuple[bool, str]:
        """
        Update satu atau beberapa field kontak.
        Jika nama berubah → hapus & sisip ulang untuk jaga urutan.
        Return (True, pesan_sukses) atau (False, pesan_error).
        """
        contact = self.search_by_name(name)
        if contact is None:
            return False, f"Kontak '{name}' tidak ditemukan."

        name_changed = new_name and new_name.strip().lower() != name.strip().lower()

        if name_changed:
            # Periksa apakah nama baru sudah ada
            if self.search_by_name(new_name):
                return False, f"Nama '{new_name}' sudah digunakan oleh kontak lain."
            self.delete(name)
            contact.name = new_name.strip()

        if new_phone is not None:
            contact.phone = new_phone.strip()
        if new_note is not None:
            contact.note  = new_note.strip()

        if name_changed:
            self.insert_sorted(contact)

        return True, "Kontak berhasil diperbarui."

    # ── GET DATA ─────────────────────────────────────────────
    def get_all(self) -> list[Contact]:
        """Kembalikan semua kontak sebagai list (urutan A-Z)."""
        result = []
        cur    = self.head
        while cur:
            result.append(cur)
            cur = cur.next
        return result

    def get_sorted(self, reverse: bool = False, by: str = "name") -> list[Contact]:
        """
        Kembalikan list kontak yang sudah diurutkan.
        by     : 'name' | 'phone'
        reverse: False = ascending, True = descending
        """
        arr = self.get_all()
        if by == "phone":
            arr.sort(key=lambda c: c.phone, reverse=reverse)
        else:
            arr.sort(key=lambda c: c.name.lower(), reverse=reverse)
        return arr

    # ── DISPLAY ─────────────────────────────────────────────
    def display_all(self) -> None:
        """Cetak semua kontak dalam format tabel."""
        self._print_table(self.get_all())

    def _print_table(self, contacts: list[Contact]) -> None:
        """Cetak list kontak sebagai tabel rata kiri."""
        if not contacts:
            print("  [Tidak ada kontak]")
            return

        W_NO    = 4
        W_NAME  = 25
        W_PHONE = 17
        
        W_NOTE  = 20
        total   = W_NO + W_NAME + W_PHONE + W_NOTE + 6

        header  = (
            f"  {'No':<{W_NO}} {'Nama':<{W_NAME}} "
            f"{'Telepon':<{W_PHONE}} {'Catatan':<{W_NOTE}}"
        )
        print(header)
        print("  " + "─" * total)

        for i, c in enumerate(contacts, 1):
            name  = (c.name[:W_NAME-1]  + "…") if len(c.name)  > W_NAME  else c.name
            phone = (c.phone[:W_PHONE-1] + "…") if len(c.phone) > W_PHONE else c.phone
            
            note  = (c.note[:W_NOTE-1]  + "…") if len(c.note)  > W_NOTE  else c.note
            print(
                f"  {i:<{W_NO}} {name:<{W_NAME}} "
                f"{phone:<{W_PHONE}} {note:<{W_NOTE}}"
            )


# ── Unit-test sederhana ─────────────────────────────────────
if __name__ == "__main__":
    ll = LinkedList()
    for name, phone in [("Citra", "081"), ("Ani", "082"), ("Budi", "083"), ("Ani", "999")]:
        ok = ll.insert_sorted(Contact(name, phone))
        print(f"  insert '{name}': {'OK' if ok else 'DUPLIKAT'}")

    print("\n  Semua kontak (harus A-Z):")
    ll.display_all()

    print("\n  Binary Search 'Budi':", ll.search_by_name("Budi"))
    print("  Linear Search nomor '082':", ll.search_by_phone("082"))
    print("  Partial 'it':", [c.name for c in ll.search_by_name_partial("it")])

    ll.update("Budi", new_name="Dedi", new_phone="099")
    print("\n  Setelah update 'Budi' → 'Dedi':")
    ll.display_all()

    ll.delete("Ani")
    print("\n  Setelah delete 'Ani':")
    ll.display_all()

    print("\n✅ linked_list.py OK")
