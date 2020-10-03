import os
import sqlite3
import fs


def sqlite_insert(conn, table, row):
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    conn.cursor().execute(sql, row)
    conn.commit()


# list = os.listdir("/run/user/1000/gvfs/smb-share:server=codex2,share=archivosdigitales")
def walk_dir(file_path:str, username:str, password:str, host:str):
    bd = sqlite3.connect('dropbox.db')
    bd.execute(""" CREATE TABLE IF NOT EXISTS archivos (
                                            id integer PRIMARY KEY,
                                            archivo text NOT NULL,
                                            checksum text
                                        ); """)


    try:
        folder = fs.open_fs(f'smb://{username}:{password}@{host}:445{file_path}')
    except:
        folder = fs.open_fs(f'smb://{username}:{password}@{host}:139{file_path}')
        
    try:
        for path in folder.walk.files():
            sqlite_insert(bd, 'archivos', {
                'archivo': path})
    except:
        pass

    bd.close()

    print("Registro de archivos exitoso")
    return folder