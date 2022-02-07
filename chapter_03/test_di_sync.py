from di_sync import di_sync


class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(('COPY', src, dest))
    
    def move(self, src, dest):
        self.append(('MOVE', src, dest))

    def delete(self, src, dest):
        self.append(('DELETE', src, dest))

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    # reader와 filesystem라는 의존성을 주입하여 가짜 상수들을 만들어서 테스트
    source = {"sha1" : "my-file"}
    dest = {}
    filesystem = FakeFileSystem()

    reader = {"/source" : source, "/dest": dest}
    di_sync(reader=reader, filesystem=filesystem, source_root=source, dest_root=dest)
    
    assert filesystem == [("COPY", "/source/my-file", "/dest/my-file")]