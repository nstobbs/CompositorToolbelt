import nuke
import CompositorToolbelt
import os
# CompositorToolbelt.py - Created on 15/1/2021 - Nuke 12.2v4 Release Build


#Function Creates the Custom Python Menu inside Nuke's UI
CompositorToolbelt.buildCompositorToolbeltMenu()
print('-' * 79)
print("Compositor's Toolbelt by github.com/nstobbs")

nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./plugins')

def showLoadedItems(path):
    itemList = os.listdir(path)
    print("Found Items in {}").format(path)
    for item in itemList:
        print(item)

showLoadedItems("/Users/nathanstobbs/.nuke/gizmos")