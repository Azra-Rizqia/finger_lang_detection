import os
import pickle
import mediapipe as mp
import cv2
import matplotlib.pyplot as plt

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

data = []
labels = []

# Periksa apakah folder data ada
if not os.path.exists(DATA_DIR):
    print(f"Folder {DATA_DIR} tidak ditemukan.")
    exit(1)

# Iterasi melalui folder dan file dalam dataset
for dir_ in os.listdir(DATA_DIR):
    folder_path = os.path.join(DATA_DIR, dir_)
    if not os.path.isdir(folder_path):
        print(f"{folder_path} bukan folder, dilewati.")
        continue

    for img_path in os.listdir(folder_path):
        img_file = os.path.join(folder_path, img_path)

        # Baca gambar
        img = cv2.imread(img_file)
        if img is None:
            print(f"Gagal membaca gambar: {img_file}")
            continue  # Lewati jika gambar tidak valid

        # Konversi ke RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Proses gambar dengan MediaPipe
        results = hands.process(img_rgb)
        if not results.multi_hand_landmarks:
            print(f"Tidak ada tangan terdeteksi di {img_file}")
            continue  # Lewati jika tidak ada tangan terdeteksi

        data_aux = []
        x_, y_ = [], []

        # Ambil landmark dari tangan
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            # Normalisasi koordinat
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))  # Normalisasi X
                data_aux.append(y - min(y_))  # Normalisasi Y

        data.append(data_aux)
        labels.append(dir_)

# Simpan data ke file pickle
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print("Data berhasil disimpan ke 'data.pickle'")