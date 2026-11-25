
class NodeSlots:
    """
    Node menggunakan __slots__ untuk membatasi atribut.
    """

    __slots__ = ('data', 'next')

    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedListSlots:
    """
    Implementasi Singly Linked List menggunakan NodeSlots.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data):
        """Menambahkan node pada bagian akhir (O(1))."""

        new_node = NodeSlots(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def prepend(self, data):
        """Menambahkan node pada bagian awal (O(1))."""

        new_node = NodeSlots(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

        self._size += 1

    def delete_head(self):
        """Menghapus node pertama."""

        if self.head is None:
            raise IndexError("Linked List kosong.")

        deleted_node = self.head
        self.head = self.head.next

        self._size -= 1

        if self.head is None:
            self.tail = None

        deleted_node.next = None

        return deleted_node.data

    def delete_tail(self):
        """Menghapus node terakhir."""

        if self.head is None:
            raise IndexError("Linked List kosong.")

        if self.head is self.tail:
            return self.delete_head()

        current = self.head

        while current.next is not self.tail:
            current = current.next

        deleted_node = self.tail

        self.tail = current
        self.tail.next = None

        self._size -= 1

        deleted_node.next = None

        return deleted_node.data

    def delete_at(self, index):
        """Menghapus node berdasarkan indeks."""

        if index < 0 or index >= self._size:
            raise IndexError("Indeks berada di luar batas.")

        if index == 0:
            return self.delete_head()

        current = self.head

        for _ in range(index - 1):
            current = current.next

        deleted_node = current.next
        current.next = deleted_node.next

        if deleted_node is self.tail:
            self.tail = current

        deleted_node.next = None
        self._size -= 1

        return deleted_node.data

    def search(self, data):
        """Mencari data dalam Linked List."""

        current = self.head

        while current is not None:
            if current.data == data:
                return True

            current = current.next

        return False

    def __len__(self):
        """Mengembalikan jumlah node."""

        return self._size
