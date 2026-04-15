# ============================================================
# contact.py
# Kerjaan Nabil
# Tugas: Buat class Contact sebagai Node Linked List
# ============================================================

# TODO menambahkan

class Contact:
    def __init__(self, name: str, phone: str, email: str = "", note: str = ""):
        self.name  = name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self.note  = note.strip()
        self.next  = None  # pointer linked list

    def __str__(self):
        return f"{self.name} | {self.phone}"

    def to_dict(self):
        return {
            "name":  self.name,
            "phone": self.phone,
            "email": self.email,
            "note":  self.note,
        }
        
