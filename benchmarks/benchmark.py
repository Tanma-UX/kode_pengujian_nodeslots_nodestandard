import sys
import os
import gc
import time
import tracemalloc

# 1. PENGATURAN IMPORT MODUL
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.insert(0, SRC_DIR)
from sll_standard import SinglyLinkedListStandard
from sll_slots import SinglyLinkedListSlots

# 2. KONFIGURASI BENCHMARK
DATA_SIZES = [100_000, 200_000, 400_000, 800_000, 1_600_000, 3_200_000, 6_400_000, 12_800_000]

# 3. PENGUJIAN KONSUMSI MEMORI
def measure_memory(SLLClass, n):
    """Mengukur Peak Memory Allocation menggunakan tracemalloc. Return:Peak memory dalam Kilobytes (KB)."""
    gc.collect()
    tracemalloc.start()
    try:
        linked_list = SLLClass()

        for i in range(n):
            linked_list.append(i)

        current_memory, peak_memory = (tracemalloc.get_traced_memory())

        # Konversi bytes menjadi KB
        peak_memory_kb = peak_memory / 1024

    finally:
        # Hentikan profiling dan lepaskan objek
        tracemalloc.stop()

        if "linked_list" in locals():
            del linked_list

        gc.collect()

    return peak_memory_kb

# 4. PENGUJIAN WAKTU APPEND
def measure_append_time(SLLClass, n):
    """Mengukur waktu penambahan N node menggunakan append()."""
    linked_list = SLLClass()
    gc.collect()
    gc.disable()
    try:
        start_time = time.perf_counter()

        for i in range(n):
            linked_list.append(i)

        end_time = time.perf_counter()

    finally:
        gc.enable()
        del linked_list

    return end_time - start_time

# 5. PENGUJIAN WAKTU PREPEND
def measure_prepend_time(SLLClass, n):
    """Mengukur waktu penambahan N node menggunakan prepend()."""
    linked_list = SLLClass()

    gc.collect()
    gc.disable()

    try:
        start_time = time.perf_counter()

        for i in range(n):
            linked_list.prepend(i)

        end_time = time.perf_counter()

    finally:
        gc.enable()
        del linked_list

    return end_time - start_time

# 6. PENGUJIAN WAKTU DELETE_HEAD
def measure_delete_head_time(SLLClass, n):
    """
    Mengukur waktu penghapusan node pertama.
    """

    linked_list = SLLClass()

    # Persiapan data sebelum timer dimulai
    for i in range(n):
        linked_list.append(i)

    gc.collect()
    gc.disable()

    try:
        start_time = time.perf_counter()

        linked_list.delete_head()

        end_time = time.perf_counter()

    finally:
        gc.enable()
        del linked_list

    return end_time - start_time

# 7. PENGUJIAN WAKTU DELETE_AT
def measure_delete_at_time(SLLClass, n):
    """
    Mengukur waktu penghapusan node pada posisi tengah.

    Posisi penghapusan:
        index = N // 2
    """

    linked_list = SLLClass()

    # Persiapan data dilakukan sebelum timer dimulai
    for i in range(n):
        linked_list.append(i)

    middle_index = n // 2

    gc.collect()
    gc.disable()

    try:
        start_time = time.perf_counter()

        linked_list.delete_at(middle_index)

        end_time = time.perf_counter()

    finally:
        gc.enable()
        del linked_list

    return end_time - start_time

# 8. PENGUJIAN WAKTU DELETE_TAIL
def measure_delete_tail_time(SLLClass, n):
    """
    Mengukur waktu penghapusan node terakhir.
    """

    linked_list = SLLClass()

    # Persiapan data sebelum timer dimulai
    for i in range(n):
        linked_list.append(i)

    gc.collect()
    gc.disable()

    try:
        start_time = time.perf_counter()

        linked_list.delete_tail()

        end_time = time.perf_counter()

    finally:
        gc.enable()
        del linked_list

    return end_time - start_time

# 9. FORMAT TABEL PENGAMATAN MEMORI
def print_memory_table(results):
    """Menampilkan hasil pengujian konsumsi memori."""
    print("\n")
    print("=" * 92)
    print("TABEL 1. HASIL PENGUJIAN KONSUMSI MEMORI")
    print("=" * 92)

    header = (
        f"{'Jumlah Node':>15}"
        f"{'Standard (KB)':>20}"
        f"{'Slots (KB)':>20}"
        f"{'Penghematan (%)':>22}"
    )

    print(header)
    print("-" * 92)

    for result in results:

        n = result["n"]
        standard = result["memory_standard"]
        slots = result["memory_slots"]
        saving = result["memory_saving"]

        print(
            f"{n:>15,}"
            f"{standard:>20,.2f}"
            f"{slots:>20,.2f}"
            f"{saving:>22.2f}"
        )

    print("=" * 92)

# 8. FORMAT TABEL PENGAMATAN WAKTU
def print_time_table_append(results):
    """Menampilkan hasil pengujian waktu eksekusi."""

    print("\n")
    print("=" * 75)
    print("TABEL 2. HASIL PENGUJIAN WAKTU EKSEKUSI APPEND")
    print("=" * 75)

    header = (
        f"{'Jumlah Node':>15}"
        f"{'Append Std (sec)':>20}"
        f"{'Append Slots (sec)':>22}"
    )

    print(header)
    print("-" * 75)

    for result in results:

        print(
            f"{result['n']:>15,}"
            f"{result['append_standard']:>20,.6f}"
            f"{result['append_slots']:>22,.6f}"
        )

    print("=" * 75)


def print_time_table_prepend(results):
    """Menampilkan hasil pengujian waktu eksekusi."""

    print("\n")
    print("=" * 75)
    print("TABEL 2. HASIL PENGUJIAN WAKTU EKSEKUSI PREPEND")
    print("=" * 75)

    header = (
        f"{'Jumlah Node':>15}"
        f"{'Prepend Std (sec)':>21}"
        f"{'Prepend Slots (sec)':>23}"
    )

    print(header)
    print("-" * 75)

    for result in results:

        print(
            f"{result['n']:>15,}"
            f"{result['prepend_standard']:>21,.6f}"
            f"{result['prepend_slots']:>23,.6f}"
        )

    print("=" * 75)

def print_time_table_delete_head(results):
    """Menampilkan hasil pengujian waktu delete_head()."""

    print("\n")
    print("=" * 75)
    print("TABEL 3. HASIL PENGUJIAN WAKTU EKSEKUSI DELETE_HEAD")
    print("=" * 75)

    header = (
        f"{'Jumlah Node':>15}"
        f"{'Delete Head Std (sec)':>28}"
        f"{'Delete Head Slots (sec)':>28}"
    )

    print(header)
    print("-" * 75)

    for result in results:
        print(
            f"{result['n']:>15,}"
            f"{result['delete_head_standard']:>28,.6f}"
            f"{result['delete_head_slots']:>28,.6f}"
        )

    print("=" * 75)

def print_time_table_delete(results):
    """Menampilkan hasil pengujian waktu eksekusi."""

    print("\n")
    print("=" * 75)
    print("TABEL 2. HASIL PENGUJIAN WAKTU EKSEKUSI DELETE_AT_MIDDLE")
    print("=" * 75)

    header = (
        f"{'Jumlah Node':>15}"
        f"{'Delete Std (sec)':>19}"
        f"{'Delete Slots (sec)':>21}"
    )

    print(header)
    print("-" * 75)

    for result in results:

        print(
            f"{result['n']:>15,}"
            f"{result['delete_standard']:>19,.6f}"
            f"{result['delete_slots']:>21,.6f}"
        )

    print("=" * 75)

def print_time_table_delete_tail(results):
    """Menampilkan hasil pengujian waktu delete_tail()."""

    print("\n")
    print("=" * 75)
    print("TABEL 4. HASIL PENGUJIAN WAKTU EKSEKUSI DELETE_TAIL")
    print("=" * 75)

    header = (
        f"{'Jumlah Node':>15}"
        f"{'Delete Tail Std (sec)':>28}"
        f"{'Delete Tail Slots (sec)':>28}"
    )

    print(header)
    print("-" * 75)

    for result in results:
        print(
            f"{result['n']:>15,}"
            f"{result['delete_tail_standard']:>28,.6f}"
            f"{result['delete_tail_slots']:>28,.6f}"
        )

    print("=" * 75)

# 9. PROGRAM UTAMA BENCHMARK
def main():
    memory_results = []
    time_results = []

    print("\n")
    print("=" * 70)
    print("BENCHMARK SINGLY LINKED LIST")
    print("NODE STANDARD VS NODE SLOTS")
    print("=" * 70)

    print("\nJumlah data pengujian:")

    for n in DATA_SIZES:
        print(f"- {n:,} Node")

    print("\nMemulai proses benchmark...\n")

    # Pengujian setiap variasi jumlah node
    for n in DATA_SIZES:

        print(f"\nMengukur {n:,} Node...")

        # A. PENGUJIAN MEMORI
        memory_standard = measure_memory(SinglyLinkedListStandard, n)

        memory_slots = measure_memory(SinglyLinkedListSlots, n)

        if memory_standard > 0:
            memory_saving = ((memory_standard - memory_slots) / memory_standard) * 100
        else:
            memory_saving = 0.0

        memory_results.append({
            "n": n,
            "memory_standard": memory_standard,
            "memory_slots": memory_slots,
            "memory_saving": memory_saving
        })

        # B. PENGUJIAN WAKTU APPEND
        append_standard = measure_append_time(SinglyLinkedListStandard, n)
        append_slots = measure_append_time(SinglyLinkedListSlots, n)

        # C. PENGUJIAN WAKTU PREPEND
        prepend_standard = measure_prepend_time(SinglyLinkedListStandard, n)
        prepend_slots = measure_prepend_time(SinglyLinkedListSlots, n)

        # D. PENGUJIAN WAKTU DELETE_AT
        delete_standard = measure_delete_at_time(SinglyLinkedListStandard, n)
        delete_slots = measure_delete_at_time(SinglyLinkedListSlots, n)

        # E. PENGUJIAN WAKTU DELETE_HEAD
        delete_head_standard = measure_delete_head_time(
            SinglyLinkedListStandard, n
        )

        delete_head_slots = measure_delete_head_time(
            SinglyLinkedListSlots, n
        )

        # F. PENGUJIAN WAKTU DELETE_TAIL
        delete_tail_standard = measure_delete_tail_time(
            SinglyLinkedListStandard, n
        )

        delete_tail_slots = measure_delete_tail_time(
            SinglyLinkedListSlots, n
        )
        
        # Simpan hasil pengukuran yang sudah diolah
        time_results.append({
            "n": n,

            "append_standard": append_standard,
            "append_slots": append_slots,

            "prepend_standard": prepend_standard,
            "prepend_slots": prepend_slots,

            "delete_standard": delete_standard,
            "delete_slots": delete_slots,

            "delete_head_standard": delete_head_standard,
            "delete_head_slots": delete_head_slots,

            "delete_tail_standard": delete_tail_standard,
            "delete_tail_slots": delete_tail_slots
        })

        print(f"Pengujian {n:,} Node selesai.")

    # MENAMPILKAN TABEL HASIL
    print_memory_table(memory_results)

    print_time_table_append(time_results)
    print_time_table_prepend(time_results)

    print_time_table_delete(time_results)
    print_time_table_delete_head(time_results)
    print_time_table_delete_tail(time_results)
    print("\nBenchmark selesai.")
    print("Seluruh hasil pengukuran berhasil ditampilkan.")

# 10. EKSEKUSI PROGRAM
if __name__ == "__main__":
    main()
