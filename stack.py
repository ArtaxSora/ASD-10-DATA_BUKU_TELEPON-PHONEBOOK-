# ============================================================
# stack.py
# kerjaan nazmi
# Tugas: Buat class Stack (LIFO) untuk riwayat operasi
# ============================================================

from __future__ import annotations


class _Node:
    """Node internal untuk Stack berbasis Linked-list."""
    __slots__ = ("data", "next")

    def __init__(self, data: str):
        self.data: str            = data
        self.next: _Node | None   = None


class Stack:
    """
    Stack LIFO dengan batas maksimum ukuran.

    Jika stack sudah penuh saat push(), elemen paling BAWAH
    (paling lama) dibuang otomatis agar riwayat tetap segar.

    Atribut publik:
        max_size (int) – Jumlah item maksimum (default 10)
    """

    def __init__(self, max_size: int = 10):
        self._top:  _Node | None = None
        self._size: int          = 0
        self.max_size            = max_size

    # ── Properti ────────────────────────────────────────────
    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._top is None

    def is_full(self) -> bool:
        return self._size >= self.max_size

    # ── Operasi utama ───────────────────────────────────────
    def push(self, item: str) -> None:
        """Tambah item ke atas stack. Buang elemen terbawah jika penuh."""
        if self.is_full():
            self._drop_bottom()
        node      = _Node(item)
        node.next = self._top
        self._top = node
        self._size += 1

    def pop(self) -> str | None:
        """Ambil dan hapus item teratas. Kembalikan None jika kosong."""
        if self.is_empty():
            return None
        data      = self._top.data      # type: ignore[union-attr]
        self._top = self._top.next      # type: ignore[union-attr]
        self._size -= 1
        return data

    def peek(self) -> str | None:
        """Lihat item teratas tanpa menghapus."""
        return self._top.data if self._top else None

    def clear(self) -> None:
        """Kosongkan seluruh stack."""
        self._top  = None
        self._size = 0

    # ── Display ─────────────────────────────────────────────
    def to_list(self) -> list[str]:
        """Kembalikan isi stack sebagai list (atas → bawah)."""
        result: list[str] = []
        cur = self._top
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def display(self) -> None:
        """Cetak seluruh isi stack ke terminal."""
        items = self.to_list()
        if not items:
            print("  [Stack kosong]")
            return
        for i, item in enumerate(items, start=1):
            marker = " ← TOP" if i == 1 else ""
            print(f"  {i:2}. {item}{marker}")

    # ── Helper privat ───────────────────────────────────────
    def _drop_bottom(self) -> None:
        """Hapus node paling bawah (paling lama dimasukkan)."""
        if self._top is None:
            return
        if self._top.next is None:       # Hanya 1 elemen
            self._top  = None
            self._size -= 1
            return
        cur = self._top
        while cur.next and cur.next.next:
            cur = cur.next
        cur.next   = None
        self._size -= 1


# ── Unit-test sederhana ─────────────────────────────────────
if __name__ == "__main__":
    s = Stack(max_size=3)
    s.push("ADD: Budi")
    s.push("EDIT: Ani")
    s.push("DELETE: Citra")
    s.push("ADD: Deni")       # Ini akan membuang "ADD: Budi"
    print("Stack setelah 4 push (max=3):")
    s.display()
    print("peek :", s.peek())
    print("pop  :", s.pop())
    print("Setelah pop:")
    s.display()
    print("✅ stack.py OK")
