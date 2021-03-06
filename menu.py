import nuke
import nukescripts
import CompositorToolbelt
import os
# CompositorToolbelt.py - Created on 15/1/2021 - Nuke 12.2v4 Release Build


#Function Creates the Custom Python Menu inside Nuke's UI

print('#' * 79)
print("Compositor's Toolbelt by github.com/nstobbs")

#Folders for Gizmos and Plugins
nuke.pluginAddPath('./Gizmos')

#Root node changes at start-up
nuke.knobDefault("Root.format", "HD_1080")
nuke.knobDefault("Root.fps", "23.98")

#FrameHold on Current Frame
nuke.addOnUserCreate(lambda:nuke.thisNode()['first_frame'].setValue(nuke.frame()),
                    nodeClass='FrameHold')

#Blur default value at 2
nuke.addOnUserCreate(lambda:nuke.thisNode()['size'].setValue(2),
                    nodeClass='Blur')                    

CompositorToolbelt.buildCompositorToolbeltMenu()

#Updates plugins in nuke
nukescripts.update_plugin_menu("All plugins")
