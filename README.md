# NetWatch: Real-Time Server Telemetry System

**NetWatch** adalah sistem monitoring server berbasis web yang dikembangkan untuk memenuhi Tugas Akhir mata kuliah **Pemrograman Jaringan**. 

Proyek ini mendemonstrasikan penerapan komunikasi jaringan hibrida menggunakan **REST API** (untuk metadata statis) dan **WebSocket** (untuk streaming data real-time).

## 📋 Fitur Utama

1.  **Real-time Monitoring:** Menampilkan penggunaan CPU dan RAM secara live tanpa refresh halaman.
2.  **Hybrid Communication Protocol:**
    * **HTTP REST API:** Digunakan untuk handshake awal dan pengiriman data spesifikasi server (OS, Processor).
    * **WebSocket (Socket.io):** Digunakan untuk streaming data telemetri (latency rendah & full-duplex).
3.  **Visualisasi Data:** Grafik dinamis menggunakan Chart.js.
4.  **Alert System:** Indikator status koneksi (Connected/Disconnected) secara real-time.

## 🛠️ Teknologi yang Digunakan

* **Backend Server:** Python (FastAPI, Uvicorn, Python-SocketIO)
* **Agent (Client):** Python (Psutil, Requests)
* **Frontend:** HTML5, CSS3, JavaScript
* **Library Frontend:** Chart.js (Grafik), Socket.io-client (Koneksi)

# Panduan Instalasi & Eksekusi NetWatch

Dokumen ini berisi langkah-langkah teknis untuk menginstal dependency dan menjalankan sistem NetWatch pada komputer lokal (Windows/Mac/Linux).

## 1. Persiapan Lingkungan (Prerequisites)

Pastikan komputer Anda sudah terinstall:
* **Python 3.8** atau versi lebih baru.
* Cek versi python dengan perintah:
    ```bash
    python --version
    ```

---

## 2. Instalasi Library

Agar lebih rapi, kita akan menginstall semua library sekaligus.

1.  Buka terminal/CMD di folder proyek, lalu jalankan perintah instalasi:
    ```bash
    pip install -r requirements.txt
    ```
    *(Tunggu hingga proses download selesai)*

2. Selesai
---

## 3. Menjalankan Sistem

Sistem ini terdiri dari dua bagian yang harus dijalankan secara bersamaan: **Server** dan **Agent**. Anda membutuhkan **2 Terminal** yang berbeda.

### Langkah A: Jalankan Server (Terminal 1)
Server bertugas melayani Web Dashboard.

1.  Buka terminal di folder proyek.
2.  Jalankan perintah:
    ```bash
    uvicorn server:app --reload --port 8000
    ```
3.  **Jangan tutup terminal ini.** Pastikan muncul pesan: `Uvicorn running on http://127.0.0.1:8000`.
4.  Buka browser dan akses: [http://localhost:8000](http://localhost:8000).
    *(Web akan terbuka, tapi grafik masih diam/kosong)*

### Langkah B: Jalankan Agent (Terminal 2)
Agent bertugas mengirim data CPU/RAM laptop Anda ke Server.

1.  Buka terminal **baru** (New Terminal/Tab).
2.  Pastikan berada di folder proyek yang sama.
3.  Jalankan perintah:
    ```bash
    python agent.py
    ```
4.  Jika berhasil, akan muncul log:
    ```text
    [AGENT] Registrasi Berhasil!
    [AGENT] Terhubung ke WebSocket!
    [SENT] CPU: 12% | RAM: 45%
    ...
    ```

---

## 4. Verifikasi

Kembali ke browser Anda di [http://localhost:8000](http://localhost:8000).
* **Status Koneksi:** Harus berwarna hijau ("Connected").
* **Info Server:** Harus menampilkan detail OS Anda (misal: Windows 11 / Linux).
* **Grafik:** Garis harus bergerak naik turun sesuai aktivitas komputer Anda.

