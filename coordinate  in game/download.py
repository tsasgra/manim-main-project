import urllib.request
import os

save_dir = r"C:\Users\ASUS\manimations\coordinate  in game\picture"

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Đổi nguồn tải sang GitHub của Lichess để không bị chặn IP
pieces_urls = {
    "white_K.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wK.svg",
    "white_Q.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wQ.svg",
    "white_R.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wR.svg",
    "white_B.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wB.svg",
    "white_N.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wN.svg",
    "white_P.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wP.svg",
    "black_K.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/bK.svg",
    "black_Q.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/bQ.svg",
    "black_R.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/bR.svg",
    "black_B.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/bB.svg",
    "black_N.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/bN.svg",
    "black_P.svg": "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/bP.svg"
}

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
urllib.request.install_opener(opener)

for filename, url in pieces_urls.items():
    save_path = os.path.join(save_dir, filename)
    
    # Kiểm tra nếu file đã tải về nhưng bị lỗi (dung lượng quá nhỏ) thì xóa đi tải lại
    if os.path.exists(save_path):
        if os.path.getsize(save_path) > 1000: 
            print(f"[{filename}] đã tải thành công, bỏ qua...")
            continue
        else:
            os.remove(save_path)
            
    print(f"Đang tải {filename} từ Lichess...")
    try:
        urllib.request.urlretrieve(url, save_path)
    except Exception as e:
        print(f"Lỗi khi tải {filename}: {e}")

print("Đã hoàn tất tải toàn bộ quân cờ!")