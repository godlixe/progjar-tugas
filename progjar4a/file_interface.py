import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}", 'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def upload(self, params=[]):
        try:
            file_path = params[0]
            if (file_path == ''):
                return None
            file_name = params[1]
            file_contents = None
            with open(file_path, 'rb') as f:
                file_contents = base64.b64decode(base64.b64encode(f.read()))
            dest_f = open(file_name, 'wb')
            dest_f.write(file_contents)
            return dict(status='OK', data_file=file_name, message="file berhasil diupload")
        except Exception as e:
            print(e)
            return dict(status='ERROR', data=str(e))

    def delete(self, params=[]):
        try:
            file_path = params[0]
            if (file_path == ''):
                return None
            if os.path.exists(file_path):
                os.remove(file_path)
                return dict(status='OK', data_file=file_path, message="file berhasil dihapus")
            else:
                return dict(status='OK', data_file=file_path, message="file tidak ada")
        except Exception as e:
            print(e)
            return dict(status='ERROR', data=str(e))


if __name__ == '__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['pokijan.jpg']))
