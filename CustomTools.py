import nuke
import platform
import os

#Create a function that will create a write node ready to render 
def writeOutToCompSaves():

    if nuke.root().name() != "Root":
        nuke.message('Save the nuke script before writing a file!')
    else:
        #Finds the Comp's filepath and creates a write node
        writeNode = nuke.createNode("Write", inpanel = False)
        writeNode["create_directories"].setValue(True)
        rootName = nuke.root().name()

        def generateFilePath(renderType):

            lastSlash = rootName.rfind('/')
            folderOfComp = rootName.replace(rootName[(lastSlash+1):len(rootName)], "")
            compName_nk = rootName[(lastSlash+1):len(rootName)]
            compName = compName_nk.replace(compName_nk[compName_nk.rfind("."):], "")

            #Checks the Systems and corrects the filepath formatting 
            finalOutputFilePath = os.path.join(folderOfComp + "renders", renderType, compName, compName + ".####." + renderType)
            if platform.system != "Darwin":
                return finalOutputFilePath.replace("\\", "/")
            else:
                return finalOutputFilePath

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


def updateShuffleNode(shuffleNodes = nuke.selectedNodes()):

    for node in shuffleNodes:
        node['label'].setValue("[value in1]")
    

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


def buildCustomMenu():

    #Creates the Custom Meun inside of Nuke's UI
    menuBar = nuke.menu("Nuke")
    customMenu = menuBar.addMenu("CustomTools")
    customMenu.addCommand("RotoBlur", "CustomTools.rotoBlur()", "o")
    customMenu.addCommand("Convert Tracker to Transform", "CustomTools.ConvertTrackerToTransform(trackerNode = nuke.selectedNode())", "shift+t")
    customMenu.addCommand("Render Near Comp", "CustomTools.writeOutToCompSaves()", "shift+w")
    customMenu.addCommand("Show Output AOV on Shuffle Nodes", "CustomTools.updateShuffleNode()")