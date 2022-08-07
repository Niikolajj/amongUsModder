import os
from urllib.request import urlopen
import re
from zipfile import ZipFile
from win32com.client import Dispatch
import warnings
with warnings.catch_warnings():
  warnings.filterwarnings("ignore",category=DeprecationWarning)
  from distutils.dir_util import (copy_tree, remove_tree)
    
def installMod():
  directories = [os.getcwd() + "/../", os.getcwd() + "/"]
  drives = ["C:/", "D:/", "G:/"]
  locations = ["Program Files (x86)/", ""]

  for drive in drives:
    for location in locations:
      directories.append(drive + location + "Steam/steamapps/common/")

  for baseDirectory in directories:
    if os.path.isdir(baseDirectory + "Among Us") & os.path.isfile(baseDirectory + "Among Us/Among Us.exe"):
      print("Among Us gefunden: " + baseDirectory + "Among Us/")
      modName = "mod"

      with urlopen("https://mod.undefine.dev") as f:
        print("Modpack herunterladen...")
        content = f.read()

        m = re.search(".*=(.*?)\..*",f.headers.get("Content-Disposition"))
        if(m.group(1)):
          modName = m.group(1)
        print("Unbenanntes Modpack gefunden" if modName == "mod" else "Modpack " + modName + " gefunden")
        
        with open(modName+".zip", "wb") as download:
          download.write(content)
        
        print("Ordner neuerstellen: " + baseDirectory + "Among Us - "+ modName)
        if(os.path.isdir(baseDirectory + "Among Us - "+ modName)):
          remove_tree(baseDirectory + "Among Us - "+ modName)
        copy_tree(baseDirectory + "Among Us", baseDirectory + "Among Us - "+ modName)

        print("Modpack entpacken")
        with ZipFile(modName + ".zip", 'r') as zip_ref:
          zip_ref.extractall("mod")
        os.remove(modName+".zip")

        files = os.listdir("mod")
        files.append(".")
        for file in files:
          if(os.path.isdir("mod/" + file + "/BepInEx")):
            copy_tree("mod/" + file, baseDirectory + "Among Us - "+ modName)
        remove_tree("mod")

        print("Verknüpfung erstellen")
        print(baseDirectory + "Among Us - "+ modName + '/Among Us.exe')
        target = os.path.join(baseDirectory + "Among Us - "+ modName + '/Among Us.exe')
        pathLink = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'), "Among Us - "+ modName + '.lnk')
        shortcut = Dispatch('WScript.Shell').CreateShortCut(pathLink)
        shortcut.Targetpath = target
        shortcut.IconLocation = target
        shortcut.save()
        input("Fertig, drück Enter")
        break
  else:
    print("Kein Among Us gefunden, bitte in den Among Us Ordner verschieben und nochmal probieren")

installMod()