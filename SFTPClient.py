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
        return file_list

    def listdir(self, path=".", sorted_date=True):
        return [f.filename for f in self.listdir_attr(path, sorted_date)]

    def get_last_file(self, path="."):
        return self.listdir_attr(path, sorted_date=True)[0].filename

    def _adjust_cwd(self, path):
        return super()._adjust_cwd(str(path))



p = Path('dive_prod2/email_admin')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, look_for_keys=False, allow_agent=False)
ftp = SFTPClientAdvance.from_transport(client.get_transport())
a = ftp.listdir(p)
print(a)
