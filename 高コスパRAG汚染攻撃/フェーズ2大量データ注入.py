import spotipy
from spotipy.api.exc import SpotifyException
import os

# Spotify認証
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID")))

def upload_song_to_spotify(metadata: dict, file_path: str) -> str | None:
    """
    単一の楽曲ファイルをSpotifyにアップロードし、track_uriを返す。
    """
    try:
        # SpotipyのUploadItemオブジェクトを作成
        upload_item = spotipy.util.UploadItem(
            path=file_path,
            mimetype='audio/mpeg',
            **metadata
        )

        # API呼び出し (アップロード実行)
        response = sp.audio_tracks(upload_item)
        if response and response['id']:
            print(f"✅ Upload Success: {metadata['title']} (ID: {response['id']})")
            return response['uri']
        return None
    except SpotifyException as e:
        print(f"❌ Upload Failed for {metadata['title']}: {e}")
        return None
    except Exception as e:
        print(f"💥 General Error during upload: {e}")
        return None

def batch_upload_poisoned_songs(songs_list: list[dict], base_dir: str = "poison_songs") -> list[str]:
    """
    楽曲リスト全体をバッチ処理でアップロードする。
    """
    uploaded_uris = []
    print("\n--- PHASE 2: Starting Batch Upload to Spotify ---")

    for i, song_meta in enumerate(songs_list):
        # ファイルパスの構築 (例: poison_songs/Tokyo Neon Drift 1.mp3)
        file_name = f"{song_meta['title']}.mp3"
        file_path = os.path.join(base_dir, file_name)

        # 楽曲ファイルが存在しない場合はスキップ (実戦では必ずファイルを用意する)
        if not os.path.exists(file_path):
            print(f"⚠️ File not found for {song_meta['title']}. Skipping.")
            # --- 💡 ここにダミーファイルを生成するコードを挿入 ---
            # (実戦では、このメタデータに対応するMP3ファイルを生成して配置する)
            # 例: generate_dummy_mp3(file_path)
            continue

        uri = upload_song_to_spotify(song_meta, file_path)
        if uri:
            uploaded_uris.append(uri)

        # APIレートリミット対策のため、一定間隔で待機
        if i % 100 == 0 and i > 0:
            time.sleep(1)

    print("\n--- PHASE 2 Complete: Injection Finished ---")
    return uploaded_uris