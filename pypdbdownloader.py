
import os
import argparse
import struct
from pdb import set_trace

import shutil
import tempfile
import urllib.request

#For each file
#Get guid 
#download blob
#send get request with id and file name
#save pdb and id

#get folder and list of files
#recursive or by filetype

#GET /download/symbols/CameraCaptureUI.pdb/66AC6BF1DC04BB7464C9BC300FA9CDDA1/CameraCaptureUI.pdb HTTP/1.1
#User-Agent: Microsoft-Symbol-Server/
#Host: msdl.microsoft.com



def handle_file(filepath, out_folder="C:\\symbols\\"):
    filename = filepath.split('\\')[-1].split('.')[0] + ".pdb"
    if 'other' in filepath:
        return
    bin_file = open(filepath, "rb").read()
    
    rsrc_location = bin_file.find(b'rsrc$02')
    guid = bin_file[rsrc_location+15:rsrc_location+15+16]
  
    unpacked = struct.unpack('<IHHBBBBBBBB', guid[:16])
    #set_trace()
 
    full_id = ''
    for part in unpacked:
        full_id += '%02x' %(part, )
 
    print(full_id)
    get_path = "http://msdl.microsoft.com/download/symbols/" + filename + "/" + full_id+"1"+ "/"  +filename 
    print(get_path)
    folder_path = out_folder + filename.replace(".pdb", "")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    try:
        with urllib.request.urlopen(get_path) as response:
            output_file = open(folder_path+ "\\" + filename, 'wb')
            #with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            #shutil.copyfileobj(response, tmp_file)
            shutil.copyfileobj(response, output_file)
                
    except Exception:
        pass
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-if','--input_folder',default="C:\\Windows\\System32\\", required=False)
    parser.add_argument('-of','--out_folder',default="C:\\symbols\\", required=False)
    #parser.add_argument('--is_dll', type=bool,default=False, required=False)
    #parser.add_argument('--is_sys', type=bool,default=False, required=False)
    #parser.add_argument('--is_exe', type=bool,default=False, required=False)
    parser.add_argument('--is_folder', type=bool,default=False, required=False)
    parser.add_argument('-f','--file_path',default="C:\\Windows\\System32\\termsrv.dll", required=False)
    
    args = parser.parse_args()

    #for filepath in ["CameraCaptureUI.dll", ]:
    #    handle_file(args.input_folder+filepath)

    if args.is_folder:
        infiles = os.listdir(args.input_folder)
        for infile in infiles:
            if ".dll" not in infile:
                continue
            handle_file(args.input_folder+"//" +infile, args.out_folder)

    # else:
    #     handle_file(args.file_path)




