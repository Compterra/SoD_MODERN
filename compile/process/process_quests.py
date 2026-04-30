import string
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPILE_DIR = ROOT / "compile"
HEADERS_DIR = ROOT / "compile" / "headers"
for path in (ROOT, COMPILE_DIR, HEADERS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from module_info import *

if str(HEADERS_DIR) not in sys.path:
    sys.path.insert(0, str(HEADERS_DIR))

from module_quests import *
from header_common import opmask_quest_index

from process_common import *

def save_quests():
  ofile = open(export_dir + "quests.txt","w")
  ofile.write("questsfile version 1\n")
  ofile.write("%d\n"%(len(quests)))
  for i_quest in range(len(quests)):
    quest = quests[i_quest]
    ofile.write("qst_%s %s %d "%(quest[0],(str.replace(quest[1]," ","_")),quest[2]))
    ofile.write("%s "%(str.replace(quest[3]," ","_")))
    ofile.write("\n")
  ofile.close()

def save_python_header():
  ofile = open("./ID_quests.py","w")
  for i_quest in range(len(quests)):
    ofile.write("qst_%s = %d\n"%(quests[i_quest][0],i_quest))
  for i_quest in range(len(quests)):
    ofile.write("qsttag_%s = %d\n"%(quests[i_quest][0],opmask_quest_index|i_quest))
  ofile.write("\n\n")
  ofile.close()


print("Exporting quest data...")
save_quests()
save_python_header()
  
