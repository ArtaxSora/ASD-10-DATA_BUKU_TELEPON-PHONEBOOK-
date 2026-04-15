# ============================================================
# linked_list.py
# Kerjaan nabil & nazmi
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
