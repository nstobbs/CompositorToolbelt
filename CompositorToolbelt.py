import nuke
import platform
import os

#Create a function that will create a write node ready to render 
def writeOutToCompSaves():

        rootName = nuke.root()["name"].value()

        #Checks if the script has been saved or not 
        if not rootName:
            nuke.message("Save the script before rendering!")
        else:
            def generateFilePath(renderType):
                
                writeNode = nuke.createNode("Write", inpanel = False)
                writeNode["create_directories"].setValue(True)

                lastSlash = rootName.rfind('/')
                folderOfComp = rootName.replace(rootName[(lastSlash+1):len(rootName)], "")
                compName_nk = rootName[(lastSlash+1):len(rootName)]
                compName = compName_nk.replace(compName_nk[compName_nk.rfind("."):], "")

                #Checks the Systems and corrects the filepath formatting 
                finalOutputFilePath = os.path.join(folderOfComp + "renders", renderType, compName, compName + ".####." + renderType)
                if platform.system != "Darwin" or "Linux":
                    return finalOutputFilePath.replace("\\", "/")

            def jpegExportSettings(renderType='jpeg'):
                
                #Changes settings for exporting out jpegs
                writeNode.knob('file').setValue(generateFilePath(renderType))
                writeNode.knob('file_type').setValue("jpeg")
                writeNode.knob('_jpeg_sub_sampling').setValue("4:4:4")
                writeNode.knob('_jpeg_quality').setValue(1.0)
                writeNode.knob('Render').execute()

            def dpxExportSettings(renderType='dpx'):

                #Changes settings for exporting out DPX
                writeNode.knob('file').setValue(generateFilePath(renderType))
                writeNode.knob('file_type').setValue("dpx")
                writeNode.knob('Render').execute()

            def buildCustomPanel():

                writeOutToCompSaveFolderPanel= nuke.Panel('Render Out')
                writeOutToCompSaveFolderPanel.setTitle("Select file type")
                writeOutToCompSaveFolderPanel.addButton('JPEG')
                writeOutToCompSaveFolderPanel.addButton('DPX')
                return writeOutToCompSaveFolderPanel, writeOutToCompSaveFolderPanel.show()

            (p,panelResultsWrite) = buildCustomPanel()

            if panelResultsWrite == 0:
                jpegExportSettings()
            elif panelResultsWrite == 1:
                dpxExportSettings()


def ConvertTrackerToTransform(trackerNode):

    #Checks that the node is a Tracker Node
    nodeName = trackerNode.name()
    
    try:
        nodeName.index('Tracker')
    except ValueError:
        nuke.message("selected node can't be used")
    else:

        #Checks all the nodes in the Nuke Scripts. Used to find the newly created node
        setAllNodesInCompBefore = set(nuke.allNodes())

        def ExportNode(TransformType, motionBlurAmount):

            #Change the settings of the Tracker to export a Transform Node ()
            trackerNode.knob("cornerPinOptions").setValue(TransformType)
            trackerNode.knob('createCornerPin').execute()

            #Finds the newly created transform node, Change this to a inner function
            setAllNodesInCompAfter = set(nuke.allNodes())
            transformNode = (setAllNodesInCompAfter - setAllNodesInCompBefore) 
            
            #Turns on motion blur on the Transform node
            for nodes in transformNode:
                nodes.knob('shutteroffset').setValue('centred')
                nodes.knob('motionblur').setValue(motionBlurAmount)

        def buildTransformOptionPanel():

            #Create a panel that allows users to pick match-move or stabilize transform
            transformOptionPanel = nuke.Panel('Export Node')
            transformOptionPanel.setTitle("Select Transform")
            transformOptionPanel.addButton('Match-move')
            transformOptionPanel.addButton('Stabilize')
            return transformOptionPanel, transformOptionPanel.show()

        (p,panelResults) = buildTransformOptionPanel()
        
        if panelResults == 0:
            ExportNode('Transform (match-move, baked)', 1)
        elif panelResults == 1:
            ExportNode('Transform (stabilize, baked)', 0)


def updateShuffleNode():

    shuffleNodes = nuke.selectedNodes()
    for node in shuffleNodes:
        if "Shuffle" in node['name'].value():
            node['label'].setValue("[value in1]")
            node['postage_stamp'].setValue(True)
    

def rotoBlur():

    #Creates Roto Node
    rotoNode = nuke.createNode("Roto")
    rotoNode.knob("cliptype").setValue("none")
    rotoNode.knob("replace").setValue(True)

    #Creates Blur Node
    blurNode = nuke.createNode("Blur", inpanel= False)
    blurNode.knob("size").setValue(2)
    blurNode.knob('channels').setValue('alpha')
    blurNode.setYpos(blurNode.ypos() + 5)


def buildCompositorToolbeltMenu():

    #Creates the Custom Meun inside of Nuke's UI
    menuBar = nuke.menu("Nuke")
    customMenu = menuBar.addMenu("CompositorToolbelt")
    customMenu.addCommand("RotoBlur", "CompositorToolbelt.rotoBlur()", "o")
    customMenu.addCommand("Convert Tracker to Transform", "CompositorToolbelt.ConvertTrackerToTransform(trackerNode = nuke.selectedNode())", "shift+t")
    customMenu.addCommand("Render Near Comp", "CompositorToolbelt.writeOutToCompSaves()", "shift+w")
    customMenu.addCommand("Show Output AOV on Selected Shuffle Nodes", "CompositorToolbelt.updateShuffleNode()")
