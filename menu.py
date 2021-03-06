# CompositorToolbelt.py and menu.py - Created on 15/1/2021 - Nuke 12.2v5 Release Build
#--------------------------------------------------
import nuke
import nukescripts
import CompositorToolbelt

# Msg
#--------------------------------------------------
print('#' * 79)
print("Compositor's Toolbelt by github.com/nstobbs")


#Projects Settings
#--------------------------------------------------
nuke.knobDefault("Root.format", "HD_1080")
nuke.knobDefault("Root.fps", "23.98")


#Default Node Values
#--------------------------------------------------
nuke.addOnUserCreate(lambda:nuke.thisNode()['first_frame'].setValue(nuke.frame()),
                    nodeClass='FrameHold')
nuke.addOnUserCreate(lambda:nuke.thisNode()['size'].setValue(2),
                    nodeClass='Blur')                    


#Run
#--------------------------------------------------
CompositorToolbelt.buildCompositorToolbeltMenu()
# nukescripts.update_plugin_menu("All plugins")
