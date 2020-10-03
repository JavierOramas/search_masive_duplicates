from typer import Typer, Argument
from files_to_db import walk_dir
from generate_checksums import generate_checksums
from generate_checksums_multitheard import generate_multithreaded
from smb.SMBConnection import SMBConnection
app = Typer()

@app.command(name='generate', help='generate sha256 checksum of all the files on a dyrectory')
def generate(path=Argument('.')):
    
    user = input('login username ')
    password = input('login password ')
    spl_path = repr(path).split("/")
    host = spl_path[0].replace("'", '')
    path = path[len(host):]
    folder = walk_dir(path,user,password,host)
    generate_multithreaded(folder)

@app.command(name='smb')
def generate_smb(path=Argument('.')):

    smb = smbclient.SambaClient(server=host, share=path, 
                                username=user, password=password, domain='baz')
    user = input('login username ')
    password = input('login password ')
    spl_path = repr(path).split("/")
    host = spl_path[0].replace("'", '')
    path = path[len(host):]
    
    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True, is_direct_tcp=True)
    conn.connect('127.0.0.1', 445)
    

   
if __name__ == '__main__':
    app()