descriptorsPath = "Container/Library/Application Support/PRBPosterExtensionDataStore/61/Extensions/com.apple.WallpaperKit.CollectionsPoster"
tmpPath = "./tmp/"
# import zip
import zipfile
import shutil
import os
import sys

zipPath = sys.argv[1]
outputName = "ConvertedToTendies"

if len(sys.argv) < 2:
    print("Usage: python imazingToTendies.py <path to .imazingapp file> <optional: output name>")
    sys.exit(1)

if len(sys.argv) > 2:
    outputName = sys.argv[2]

correctedName = zipPath.replace(":", "").replace("\\", "").replace("/", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace("|", "")
if not zipfile.is_zipfile(zipPath):
    print("Incorrect file format. Is it a zip archive/.imazingapp file?")
    sys.exit(1)

if not os.path.exists(tmpPath):
    os.makedirs(tmpPath)

if os.path.exists(tmpPath + correctedName):
    shutil.rmtree(tmpPath + correctedName)

with zipfile.ZipFile(zipPath, 'r') as zip_ref:
    zip_ref.extractall(tmpPath + correctedName)

def dirTree(path, level=0, walk=True):
    tree=[]
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            tree.append(item)
            if walk:
              tree.extend(dirTree(os.path.join(path, item), level+1))
    return tree

if not os.path.exists(tmpPath + descriptorsPath):
    print("No PosterBoards found.")
    sys.exit(0)
foundDescriptors = []

realPath = tmpPath + descriptorsPath
tree = dirTree(tmpPath + descriptorsPath + "/configurations", walk=False)
for item in tree:
  print("Found descriptor: " + item +" in " + tmpPath + descriptorsPath + "/configurations/" + item)
  foundDescriptors.append(tmpPath + descriptorsPath + "/configurations/" + item)
    
print()
print("The file with the name " + outputName + ".tendies will be created in the current directory.")
print("IF A FILE WITH THE SAME NAME ALREADY EXISTS, IT WILL BE OVERWRITTEN.")
print("Are you sure you want to convert these posters to Tendies (Nugget 5.0+) format? (y/n)")
yesno = input()
if yesno.lower() != "y":
    print("Exiting.")
    sys.exit(0)

if os.path.exists("./tendies"):
    shutil.rmtree("./tendies")

if not os.path.exists("./tendies"):
    os.makedirs("./tendies")

if not os.path.exists("./tendies/descriptors"):
    os.makedirs("./tendies/descriptors")

for descriptor in foundDescriptors:
    shutil.copytree(descriptor, "./tendies/descriptors/" + descriptor.split("/")[-1])

if os.path.exists(outputName + ".tendies"):
    os.remove(outputName + ".tendies")

shutil.make_archive(outputName, 'zip', "./tendies")
os.rename(outputName + ".zip", outputName + ".tendies")

print("Conversion complete. Output file: " + outputName + ".tendies")
shutil.rmtree(tmpPath + correctedName)
shutil.rmtree("./tendies")