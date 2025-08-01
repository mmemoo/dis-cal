import gdown
import zipfile
import shutil
import sys
import subprocess
import os
from scripts.json_utils import write_json,read_json


write_json("setup_state.json","ollama",shutil.which("ollama") == True)
write_json("setup_state.json","brew",shutil.which("brew") == True)


if read_json("setup_state.json","ollama"):
    print("Ollama is already installed.")
else:
    if sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):
        gdown.download("https://drive.google.com/uc?id=1er8wPF-LTETLzsp09KA51fl8V0RisdAD",
                            r"cli_tool\OllamaSetup.exe")
            
        print("Launched Ollama setup, check the background apps to find it.")
        subprocess.run(r"cli_tool\OllamaSetup.exe")

    elif sys.platform.startswith("linux"):
        os.system("curl -fsSL https://ollama.com/install.sh | sh")
        
    else:
            
        if read_json("setup_state.json","brew"):
            print("Brew is already installed.")
        else:
            os.system("/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")    
            subprocess.run(f"echo 'eval \"$(/opt/homebrew/bin/brew shellenv)\"' >> /Users/{os.getlogin()}/.zprofile",shell=True,executable="/bin/bash")
            subprocess.run("eval \"$(/opt/homebrew/bin/brew shellenv)\"",shell=True,executable="/bin/bash")
            
            write_json("setup_state.json","brew",True)

        os.system("brew install --cask ollama")
        
    print("Ollama is installed.")
    write_json("setup_state.json","ollama",True)


if read_json("setup_state.json","usda_data"):
    print("USDA data already downloaded.")
else:
    gdown.download("https://drive.google.com/uc?id=1Y8Adg5W_7NAUVLRYSLqGjqg2WtpcsngP","data/usda_data.zip")
    
    usda_data = zipfile.ZipFile("data/usda_data.zip")
    usda_data.extractall("data")
    
    os.remove("data/usda_data.zip")

    write_json("setup_state.json","usda_data",True)


if read_json("setup_state.json","chromadb"):
    print("chromadb persistent database already downloaded.")
else:
    gdown.download("https://drive.google.com/uc?id=1UHxM7G80Oa13FwnwroFWLmXmWxe69lwm","data/chromadb.zip")
    
    usda_data = zipfile.ZipFile("data/chromadb.zip")
    usda_data.extractall("data")
    
    os.remove("data/chromadb.zip")

    write_json("setup_state.json","chromadb",True)