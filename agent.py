import time
import psutil
import socketio
import requests
import platform

# Konfigurasi
SERVER_URL = 'http://localhost:8000'
sio = socketio.Client()

def get_system_info():
    """Mengambil Data Statis (OS, Node Name, Processor)"""
    return {
        "os": platform.system(),
        "release": platform.release(),
        "node": platform.node(),
        "processor": platform.processor()
    }

def main():
    # 1. Kirim Data Statis via API (REST HTTP)
    print("[AGENT] Mendaftarkan diri ke Server via API...")
    try:
        info = get_system_info()
        response = requests.post(f"{SERVER_URL}/api/register", json=info)
        if response.status_code == 200:
            print("[AGENT] Registrasi Berhasil!")
        else:
            print("[AGENT] Registrasi Gagal via API.")
    except Exception as e:
        print(f"[ERROR] Server API belum nyala: {e}")
        return

    # 2. Koneksi WebSocket untuk Data Real-time
    try:
        print("[AGENT] Menghubungkan WebSocket...")
        sio.connect(SERVER_URL)
        print("[AGENT] Terhubung ke WebSocket!")
        
        while True:
            # Ambil data Real-time
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            
            payload = {
                "timestamp": time.strftime("%H:%M:%S"),
                "cpu": cpu_usage,
                "ram": ram_usage
            }
            
            # Kirim data via Socket
            sio.emit('telemetry_data', payload)
            print(f"[SENT] CPU: {cpu_usage}% | RAM: {ram_usage}%")
            
            # Tidak perlu sleep karena psutil.cpu_percent sudah blocking selama 1 detik

    except Exception as e:
        print(f"[ERROR] Koneksi WebSocket putus: {e}")
    finally:
        sio.disconnect()

if __name__ == "__main__":
    main()