### custom keys ###
s_mode = 0

def stablize_toggle():
	global s_mode
	if s_mode == 0:
		s_mode = 1
		fx.viewer.setStabilize(1)
	elif s_mode == 1:
			s_mode = 0
			fx.viewer.setStabilize(0)

fx.bind('Ctrl+Alt+r', stablize_toggle)

### toggle outline + reshape tool ###
q_mode = 0
def outline_cycler():
    '''Cycle shape overlay Views for Paint and Roto'''
    node = fx.activeNode()
    if node.type == 'RotoNode':
        global q_mode
        fx.viewer.stereoAlign = False
        if q_mode == 0:
            q_mode = 1
            fx.viewer.setOverlay(False)
            fx.status("Overlay Off")
        elif q_mode == 1:
            q_mode = 0
            fx.viewer.setOverlay(True)
            fx.status("Overlay On")
	#else:
            #q_mode = 0
            #fx.viewer.setOverlay(True)
            #fx.viewer.selectTool("Reshape")
            #fx.status("Reshape Tool")

fx.bind('q', outline_cycler)

#### remap common roto checker to 1 2 3 4 ####

#a_mode = 0

def alpha_mode():
    #global a_mode
    node = fx.activeNode()
    if node.type == 'RotoNode':
	fx.viewer.stereoAlign = False
	fx.viewer.channelMask = fx.Color(0,0,0,1)
	fx.viewer.setViewMode(0)
	fx.status("Alpha Channel")
	fx.unbind('Alt+a')

    elif node.type == 'PaintNode':
	fx.viewer.setViewMode(0)
	fx.status("")
        #fx.bind('Alt+a', callMethod(soloChannel, fx.Color(0, 0, 0, 1)))

fx.bind('1', alpha_mode)

def normal_mode():
    node = fx.activeNode()
    if node.type == 'RotoNode':
	fx.viewer.stereoAlign = False
	fx.viewer.channelMask = fx.Color(1,1,1,0)
	fx.viewer.setViewMode(1)
	fx.status("Normal View")

    elif node.type == 'PaintNode':
	fx.viewer.channelMask = fx.Color(1,1,1,0)
	fx.viewer.setViewMode(1)
	fx.status("")

fx.bind('2', normal_mode)

def overlay_mode():
    node = fx.activeNode()
    if node.type == 'RotoNode':
	fx.viewer.stereoAlign = False
	fx.viewer.channelMask = fx.Color(1,1,1,1)
	fx.viewer.setViewMode(0)
	fx.status("Overlay Mode")

    elif node.type == 'PaintNode':
	fx.viewer.channelMask = fx.Color(1,1,1,0)
	fx.viewer.setViewMode(2)
	fx.status("")

fx.bind('3', overlay_mode)

def composite_mode():
    node = fx.activeNode()
    if node.type == 'RotoNode':
	fx.viewer.stereoAlign = False
	fx.viewer.channelMask = fx.Color(1,1,1,0)
	fx.viewer.setViewMode(3)
	fx.status("Composite Mode")

    elif node.type == 'PaintNode':
	fx.viewer.channelMask = fx.Color(1,1,1,0)
	fx.viewer.setViewMode(3)
	fx.status("")

fx.bind('4', composite_mode)

def overlay_null():
    node = fx.activeNode()
    if node.type == 'RotoNode':
        fx.status("Null Function")

fx.bind('0', overlay_null)

#### end of remap common roto checker to 1 2 3 4 ####

### handle resizer ###

def handelSize_small():
    id = 'shape.handleSize'
    fx.prefs[id] -= 1
    fx.status('Shape Handle Size: %s ' %("{0:.0f}".format(fx.prefs[id])))
    if fx.prefs[id] < 2:
        fx.prefs[id] = 1
        fx.status("Shape Handle Size can't be less than 1")
    else:
        fx.prefs[id] -= 1
        fx.status('Shape Handle Size: %s ' %("{0:.0f}".format(fx.prefs[id])))
fx.bind('Alt+[', handelSize_small)
 
#Shape Handle increase by 1
def handelSize_big():
    id = 'shape.handleSize'
    fx.prefs[id] += 1
    fx.status('Shape Handle Size: %s ' %("{0:.0f}".format(fx.prefs[id])))
fx.bind('Alt+]', handelSize_big)

### end of handle resizer ###

#===============================================================================
class keyframeVisibility(Action):
    """Creates keyframes without clicking on the visibility icon
"""

    def __init__(self):
        Action.__init__(self, "Keyframe Visibility")

    def available(self):
        shapes = getObjects(selection(), types=[Shape])
        assert len(shapes) > 0, "There must be one or more selected shapes"

    def execute(self, type="in"):
        shapes = getObjects(selection(), types=[Shape])


        beginUndo("Visibility ON/OFF") 
        print "test"
        node = activeNode()
        session = node.session
        startFrame = session.startFrame

        actualframe = player.frame
        wasConstant = False
        for shape in shapes:            
            opacity = shape.property("opacity")
            if opacity.constant:
                opacity.constant = False        
                wasConstant = True
                
            if type == "in":    
                if opacity.getValue(actualframe) > 0:
                    opacity.setValue(0, actualframe)
                    opacity.setValue(100, actualframe)
                    opacity.setValue(0, actualframe -1)
                else:
                    opacity.setValue(0, actualframe)
                    opacity.setValue(100, actualframe)
                    opacity.setValue(0, actualframe -1)


                if wasConstant and actualframe != 0:
                    editor = PropertyEditor(opacity)                
                    editor.deleteKey(0)
                    editor.execute()
                    
            if type == "out":   
                if opacity.getValue(actualframe) > 0:
                    opacity.setValue(0, actualframe)
                    opacity.setValue(100, actualframe)
                    opacity.setValue(0, actualframe +1)
                else:
                    opacity.setValue(0, actualframe)
                    opacity.setValue(100, actualframe)
    
                if type == "singleframe":
                if actualframe not in (0,session.duration):
                    if opacity.getValue(actualframe) > 0:
                        opacity.setValue(0, actualframe-1)
                        opacity.setValue(100, actualframe)
                        opacity.setValue(0, actualframe+1)
                        if actualframe != 1 and wasConstant:
                            editor = PropertyEditor(opacity)                
                            editor.deleteKey(0)
                            editor.execute()
                elif actualframe == 0:
                    if opacity.getValue(actualframe) > 0:
                        opacity.setValue(100, actualframe)
                        opacity.setValue(0, actualframe+1)
                elif actualframe == session.duration:
                    if opacity.getValue(actualframe) > 0:
                        opacity.setValue(0, actualframe-1)
                        opacity.setValue(100, actualframe)
                        editor = PropertyEditor(opacity)                
                        editor.deleteKey(0)
                        editor.execute()


        endUndo()
addAction(keyframeVisibility())

def keyframeVisibilitySingle():
    action = fx.actions["keyframeVisibility"]
    if action:
        action.execute("singleframe")

fx.bind('Shift+n', keyframeVisibilitySingle)

#default mode:
def keyframeVisibility():
    action = fx.actions["keyframeVisibility"]
    if action:
        action.execute()
#===============================================================================
fx.bind("Alt+,", keyframeVisibility)
#===============================================================================

#default mode:
def keyframeVisibilityo():
    action = fx.actions["keyframeVisibility"]
    if action:
        action.execute("out")

#===============================================================================
fx.bind("Alt+.", keyframeVisibilityo)
#===============================================================================

previous_gain = 0
def toggleviewerGain():
    global previous_gain
    if fx.viewer.exposure != 0:
        previous_gain = fx.viewer.exposure
        fx.viewer.exposure = 0
    else:
        fx.viewer.exposure = previous_gain
        
#===============================================================================
fx.bind("Ctrl+g", toggleviewerGain)
#===============================================================================

previous_gamma =1
def toggleviewerGamma():
    global previous_gamma
    if fx.viewer.gamma != 1:
        previous_gamma = fx.viewer.gamma
        fx.viewer.gamma = 1
    else:
        fx.viewer.gamma = previous_gamma
    
#===============================================================================
fx.bind("Ctrl+shift+g", toggleviewerGamma)
#===============================================================================

def DviewerGamma():
    if fx.viewer.gamma < 0:
		fx.viewer.gamma = 0
    else:
       fx.viewer.gamma -= .2
#===============================================================================
fx.bind("Shift+,", DviewerGamma)
#===============================================================================
def IviewerGamma():
    global previous_gamma
    previous_gamma = fx.viewer.gamma
    fx.viewer.gamma += .2
#===============================================================================
fx.bind("Shift+.", IviewerGamma)
#===============================================================================
def DviewerGain():
    if fx.viewer.exposure < -5:
		fx.viewer.exposure = -5
    else:
       fx.viewer.exposure -= .2
#===============================================================================
fx.bind("Ctrl+,", DviewerGain)
#===============================================================================
def IviewerGain():
    global previous_gain
    previous_exposure = fx.viewer.exposure
    fx.viewer.exposure += .2
#===============================================================================
fx.bind("Ctrl+.", IviewerGain)
#===============================================================================

class keyframeTools(Action):
    """Keyframe Actions
"""
 
    def __init__(self):
        Action.__init__(self, "Keyframe Tools")
 
    def available(self):
        shapes = getObjects(selection(), types=[Shape])
        assert len(shapes) > 0, "There must be one or more selected shapes"
         
    def execute(self, type="normal"):
        beginUndo("Keyframe Tools")
 
        node = activeNode()
        session = node.session
        shapelist = getObjects(selection(), types=[Shape])
        actualframe = player.frame
         
        for shape in shapelist:
            path = shape.property("path")
            if actualframe in path.keys:
                if type == "normal":
                    editor = PropertyEditor(path)
                    editor.deleteKey(path.keys.index(actualframe))
                    editor.execute()
 
        endUndo()
addAction(keyframeTools())

def keyframeTools():
    action = fx.actions["keyframeTools"]
    if action:
        action.execute()
 #===============================================================================
fx.bind('Alt+d', keyframeTools)
#===============================================================================
#===============================================================================
import Offsetmatrix

def OffsetmatrixHelperlayer():
    action = fx.actions["OffsetmatrixHelperlayer"]
    if action:
        action.execute()

fx.bind('F11', OffsetmatrixHelperlayer)

## paint opacity toggles

opacity = 0
def dtogglePaintOpacity():
	global opacity
	if fx.activeNode().type == "PaintNode":
		opacity = fx.paint.opacity/100
		fx.paint.opacity = (opacity - .01)
		opacity = fx.paint.opacity / 100
		print(opacity)
 
fx.bind("Shift+[", dtogglePaintOpacity)

def itogglePaintOpacity():
	global opacity
	if fx.activeNode().type == "PaintNode":
		opacity = fx.paint.opacity/100
		fx.paint.opacity = (opacity + .01)
		opacity = fx.paint.opacity / 100
		print(opacity)
 
fx.bind("Shift+]", itogglePaintOpacity)
