import os
import cv2

# Membuat folder data jika belum ada
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 3  # Jumlah kelas
dataset_size = 100     # Jumlah gambar per kelas

# Mencoba membuka kamera dengan beberapa indeks (0, 1, 2)
cap = None
for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Kamera berhasil dibuka dengan indeks {i}")
        break
else:
    print("Tidak ada kamera yang terdeteksi.")
    exit(1)  # Keluar jika kamera tidak ditemukan

# Mengumpulkan data untuk setiap kelas
for j in range(number_of_classes):
    class_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print(f'Collecting data for class {j}. Tekan "Z" untuk mulai.')

    # Tunggu konfirmasi pengguna sebelum mulai mengambil gambar
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame dari kamera.")
            continue  # Ulangi membaca frame jika gagal

        cv2.putText(frame, 'Ready? Press "Z"!', (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('z'):
            break  # Mulai mengambil gambar setelah 'Z' ditekan

    # Mulai mengambil gambar dan menyimpan ke folder
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame.")
            break  # Hentikan jika frame gagal dibaca

        # Menampilkan frame di jendela GUI
        cv2.imshow('frame', frame)
        
        # Simpan gambar ke folder sesuai kelas
        file_path = os.path.join(class_dir, f'{counter}.jpg')
        cv2.imwrite(file_path, frame)

        counter += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Tekan 'Q' untuk keluar lebih awal
            print("Pengumpulan data dihentikan.")
            break

# Lepaskan kamera dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()
