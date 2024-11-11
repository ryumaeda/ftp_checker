from fastapi import FastAPI
from ftplib import FTP
import os

# FTP接続情報
FTP_HOST = "ftp.example.com"
FTP_USER = "username"
FTP_PASSWORD = "password"
FTP_DIRECTORY = "/test/test"

app = FastAPI()

@app.get("/{search_text}")
async def search_files(search_text: str):
    # FTP接続情報
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASSWORD)
    
    # 検索対象のディレクトリに移動
    ftp.cwd(FTP_DIRECTORY)
    
    matching_files = []
    
    # ファイル一覧を取得
    files = ftp.nlst()
    
    # 各ファイルの内容を確認
    for file in files:
        # 一時ファイルとしてダウンロード
        with open(f'temp_{file}', 'wb') as temp_file:
            ftp.retrbinary(f'RETR {file}', temp_file.write)
            
        # ファイルの内容を読み込んで検索
        with open(f'temp_{file}', 'r') as temp_file:
            content = temp_file.read()
            if search_text in content:
                matching_files.append(file)
                
        # 一時ファイルを削除
        os.remove(f'temp_{file}')
    
    ftp.quit()
    
    return {"matching_files": matching_files}