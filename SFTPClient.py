import paramiko
from pathlib import Path

host = ''
port = ''
user = ''
password = ''


class SFTPClientAdvance(paramiko.SFTPClient):

    def listdir_attr(self, path='.', sorted_date=True):
        file_list = super().listdir_attr(path)
        if sorted_date:
            return sorted(file_list, key=lambda x: x.st_mtime, reverse=True)
        else:
            return file_list

    def get_last_file(self, path="."):
        return self.listdir_attr(path, sorted_date=True)[0].filename

    def _adjust_cwd(self, path):
        # sftp может потребоваться не только на linux но и на windows, и ваш код не будет корректно работать
        # можно сделать более универсально и просто) не завязываясь на тип ОС
        if not isinstance(path, str):
            return super()._adjust_cwd(path.as_posix())
        else:
            return super()._adjust_cwd(path)



p = Path('dive_prod2')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password)
ftp = SFTPClientAdvance.from_transport(client.get_transport())
a = ftp.listdir(p)
print(a)


