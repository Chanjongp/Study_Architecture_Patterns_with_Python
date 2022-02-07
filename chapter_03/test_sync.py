import tempfile
from pathlib import Path
import shutil
from sync import sync, determine_actions


class TestE2E:
    @staticmethod
    def test_when_a_file_exists_in_the_source_but_not_the_destination():
        try:    
            # 임시 디렉터리 생성
            source = tempfile.mkdtemp()
            dest = tempfile.mkdtemp()

            content = "I am a very useful file"
            # my-file이라는 이름의 원본 파일에 content 작성
            (Path(source) / "my-file").write_text(content)

            sync(source, dest)

            # sync을 맞추고, 원본에 있는 파일이 사본에 복사되었는지 체크
            expected_path = Path(dest) / "my-file"
            assert expected_path.exists()
            assert expected_path.read_text() == content

        finally:
            # 디렉터리 삭제 -> 하위 폴더들 전체 삭제
            shutil.rmtree(source)
            shutil.rmtree(dest)

    @staticmethod
    def test_when_a_file_has_been_renamed_in_the_source():
        try:
            # 임시 디렉터리 생성
            source = tempfile.mkdtemp()
            dest = tempfile.mkdtemp()

            content = "I am a file that was renamed"
            # 원본에 source-filename이라는 path
            source_path = Path(source) / "source-filename"
            # 사본에 dest-filename이라는 path 
            old_dest_path = Path(dest) / "dest-filename"

            # 예상되는(sync 후 바뀐) 사본의 경로 source-filename 
            expected_dest_path = Path(dest) / "source-filename"
            
            # 원본, 사본에 다른 파일이름으로 동일한 내용 작성
            source_path.write_text(content)
            old_dest_path.write_text(content)

            sync(source, dest)

            # sync 후 기존 path에 있는 파일명(dest-filename)이 존재하는지 체크
            # 바뀐 파일의 내용이 content와 같은지 체크
            assert old_dest_path.exists() is False
            assert expected_dest_path.read_text() == content

        finally:
            # 임시 디렉터리 삭제
            shutil.rmtree(source)
            shutil.rmtree(dest)


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {}
    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("COPY", Path("/src/fn1"), Path("/dst/fn1"))]


def test_when_a_file_has_been_renamed_in_the_source():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {"hash1": "fn2"}
    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("MOVE", Path("/dst/fn2"), Path("/dst/fn1"))]
