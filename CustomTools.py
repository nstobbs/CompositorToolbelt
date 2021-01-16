import nuke

def ConvertTrackerToTransform(trackerNode):

    #Checks that the node is a Tracker Node
    nodeName = trackerNode.name()
    
    try:
        nodeName.index('Tracker')
    except ValueError:
        nuke.message("selected node can't be used")
    else:

        #Checks all the nodes in the Nuke Scripts. Used to find the newly created node
        setAllNodesInNukeScriptBefore = {}
        setAllNodesInNukeScriptAfter = {}
        setAllNodesInNukeScriptBefore = set(nuke.allNodes())

        #Create a panel that allows users to pick match-move or stabilize transform
        transformOptionPanel = nuke.Panel('transformOptionPanel')
        buttonMatch = transformOptionPanel.addButton('Match-move')    
        buttonStab = transformOptionPanel.addButton('Stabilize')
        transformOptionPanel.show()

        if buttonMatch == True:

            #Change the settings of the Tracker to export a Transform Node ()
            trackerNode.knob("cornerPinOptions").setValue('Transform (match-move, baked)')
            trackerNode.knob('createCornerPin').execute()

            #Finds the newly created transform node, Change this to a inner function
            setAllNodesInNukeScriptAfter = set(nuke.allNodes())
            transformNode = (setAllNodesInNukeScriptAfter - setAllNodesInNukeScriptBefore) 
            
            #Turns on motion blur on the Transform node
            for nodes in transformNode:
                nodes.knob('shutteroffset').setValue('centred')
                nodes.knob('motionblur').setValue(0)

        elif buttonStab == True:

            #Change the settings of the Tracker to export a Transform Node ()
            trackerNode.knob("cornerPinOptions").setValue('Transform (stabilize, baked)')
            trackerNode.knob('createCornerPin').execute()
        
            #Finds the newly created transform node, Change this to a inner function
            setAllNodesInNukeScriptAfter = set(nuke.allNodes())
            transformNode = (setAllNodesInNukeScriptAfter - setAllNodesInNukeScriptBefore) 
            
            #Turns on motion blur on the Transform node
            for nodes in transformNode:
                nodes.knob('shutteroffset').setValue('centred')
                nodes.knob('motionblur').setValue(1)

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