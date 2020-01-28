from os.path import join, dirname
from dotenv import load_dotenv
from os import environ, remove
from shutil import make_archive
from paramiko import SSHClient, AutoAddPolicy
import scp
from shutil import rmtree


def evacuate(target):
    """ コントローラに繋がれている外部ディスクに画像を保存する """

    # 環境変数
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    IP = environ.get("IP")
    name = environ.get("NAME")
    password = environ.get("PASSWORD")
    raspi_name = environ.get("RASPI_NAME")

    root_dir = "/home/pi/Desktop/4cam_img"
    remote_path = "/Volumes/Extreme SSD/scp"
    remote_path = join(remote_path, raspi_name)

    # zipを作る
    make_archive(join(root_dir, target), 'zip', root_dir=root_dir, base_dir=target)

    # サーバに繋ぐ
    with SSHClient() as sshc:
        sshc.set_missing_host_key_policy(AutoAddPolicy())
        sshc.connect(hostname=IP, port=22, username=name, password=password)
        # zipを送る
        with scp.SCPClient(sshc.get_transport()) as scpc:
            scpc.put(files=join(root_dir, target+".zip"), remote_path=remote_path)

    # ファイルとディレクトリを削除
    remove(join(root_dir, target+".zip"))
    rmtree(join(root_dir, target))
