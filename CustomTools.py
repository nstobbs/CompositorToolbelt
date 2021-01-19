import nuke

#Create a function that will create a write node ready to render 
def writeOutToCompSaves(rootName, renderType):

    #Finds the Comp's filepath and creates a write node
    writeNode = nuke.createNode('Write')

    def generateFilePath(rootName, renderType):


        lastSlash = rootName.rfind('/')
        folderOfComp = rootName.replace(rootName[(lastSlash+1):len(rootName)], "")
        compName_nknc = rootName[(lastSlash+1):len(rootName)]
        compName = compName_nknc.replace(compName_nknc[compName_nknc.rfind("."):], "")

        finalOutputFilePath = folderOfComp + "renders" + "/" + renderType + "/" + compName + "/" + compName + ".####." + renderType

        print(rootName, "_rootName")
        print(folderOfComp, "_folderOfComp")
        print(compName_nknc, "_compName_nknc")
        print(compName, "_compName")
        print(renderType, "_renderType")
        print(finalOutputFilePath, "_finalOutputFilePath")
        return finalOutputFilePath


    def jpegExportSettings(rootName, renderType):
        
        #Changes settings for exporting out jpegs
        writeNode.knob('file').setValue(generateFilePath(rootName, renderType))
        writeNode.knob('file_type').setValue("JPEG")
        writeNode.knob('_jpeg_sub_sampling').setValue("4:4:4")
        writeNode.knob('_jpeg_quality').setValue(1.0)
    
    def dpxExportSettings(rootName, renderType):

        #Changes settings for exporting out DPX
        writeNode.knob('file').setValue(generateFilePath(rootName, renderType))
        writeNode.knob('file_type').setValue("DPX")

    def buildCustomPanel():

        writeOutToCompSaveFolderPanel= nuke.Panel('Render Out')
        writeOutToCompSaveFolderPanel.addButton('JPEG')
        writeOutToCompSaveFolderPanel.addButton('DPX')
        return writeOutToCompSaveFolderPanel, writeOutToCompSaveFolderPanel.show()

    (p,panelResultsWrite) = buildCustomPanel()

    if panelResultsWrite == 0:
        jpegExportSettings(nuke.root().name(), "jpeg")
    elif panelResultsWrite == 1:
        dpxExportSettings(nuke.root().name(), "dpx")


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
            transformOptionPanel.addButton('Match-move')
            transformOptionPanel.addButton('Stabilize')
            return transformOptionPanel, transformOptionPanel.show()

        (p,panelResults) = buildTransformOptionPanel()
        
        if panelResults == 0:
            ExportNode('Transform (match-move, baked)', 1)
        elif panelResults == 1:
            ExportNode('Transform (stabilize, baked)', 0)
            

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