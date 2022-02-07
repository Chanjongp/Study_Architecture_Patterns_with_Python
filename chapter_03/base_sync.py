import hashlib
import os
import shutil
from pathlib import Path

BLOCKSIZE = 65536


def sync(source, dest):
    # 원본 폴더의 자식들을 순회하면서 파일 이름과 해시의 사전을 만든다.
    source_hashes = {}
    for folder, _, files in os.walk(source):
        # folder : folder가 있는 path
        # /chapter_02/__pycache__
        
        # files: folder 안에 있는 file 이름을 배열로 반환
        # ['sync.py', 'test_sync.py', 'Makefile', 'mypy.ini', '.gitignore', 'before_sync.py', 'license.txt']

        for fn in files:
            # ex. sync.py의 folder를 Path로 지정하고, 파일 이름을 추가함 (폴더이름을 / 해줘야 함)
            # Path(folder) == chapter_03
            # Path(folder) / fn) == chapter_03/before_sync.py
            source_hashes[hash_file(Path(folder) / fn)] = fn

    seen = set()  # 사본 폴더에서 찾은 파일을 추적한다.

    # 사본 폴더 자식들을 순회하면서 파일 이름과 해시를 얻는다.
    for folder, _, files in os.walk(dest):
        for fn in files:
            # folder 안에 있는 각 file 순회 및 해시
            dest_path = Path(folder) / fn 
            dest_hash = hash_file(dest_path)
            # 해시된 사본 파일 추가
            seen.add(dest_hash)

            # 사본에는 있지만 원본에 없는 파일을 찾으면서 삭제한다.
            if dest_hash not in source_hashes:
                os.remove(dest_path)

            # 사본에 있는 파일이 원본과 다른 이름이면 원본 이름으로 바꾼다.
            elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])

    # 원본에는 있지만 사본에는 없는 모든 파일들을 사본으로 복사한다.
    for src_hash, fn in source_hashes.items():
        if src_hash not in seen:
            shutil.copy(Path(source) / fn, Path(dest) / fn)

BLOCKSIZE = 65536


def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()