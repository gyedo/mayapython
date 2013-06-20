import sys, math

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# Plug-in information:
kPluginNodeName = 'StarTexture'
kPluginNodeClassify = 'texture/2d'
kPluginNodeId = OpenMaya.MTypeId(0x0000C) # this must be unique

class StarTexture(OpenMayaMPx.MPxNode):
    # draw star procedurally
    aOutColor = OpenMaya.MObject()
    aUCoord = OpenMaya.MObject()
    aVCoord = OpenMaya.MObject()
    aUVCoord = OpenMaya.MObject()
    aUctr = OpenMaya.MObject()
    aVctr = OpenMaya.MObject()
    aRmin = OpenMaya.MObject()
    aRmax = OpenMaya.MObject()
    aNpoints = OpenMaya.MObject()
    aColor1 = OpenMaya.MObject()
    aColor2 = OpenMaya.MObject()    
    aFilterSizeX = OpenMaya.MObject()
    aFilterSizeY = OpenMaya.MObject()
    aFilterSize = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, block):

        if (plug == StarTexture.aOutColor):
            resultColor = OpenMaya.MFloatVector()

            u = block.inputValue(StarTexture.aUCoord).asFloat()
            v = block.inputValue(StarTexture.aVCoord).asFloat()

            uctr = block.inputValue(StarTexture.aUctr).asFloat()
            vctr = block.inputValue(StarTexture.aVctr).asFloat()
      
            rmin = block.inputValue(StarTexture.aRmin).asDouble()
            rmax = block.inputValue(StarTexture.aRmax).asDouble()
  
            npoints = block.inputValue(StarTexture.aNpoints).asShort()

            surfaceColor1 = block.inputValue(StarTexture.aColor1).asFloatVector()
            surfaceColor2 = block.inputValue(StarTexture.aColor2).asFloatVector()

            starangle = 2 * math.pi / npoints; 

            p0 = OpenMaya.MVector(rmax * math.cos(0.0), rmax * math.sin(0.0), 0.0)
            p1 = OpenMaya.MVector(rmin * math.cos(starangle/2.0), rmin * math.sin(starangle/2.0), 0.0) 
            d0 = p1 - p0
  
            uu = u - uctr - math.floor(u)
            vv = v - vctr - math.floor(v)

            if uu >= 0:
                angle = math.atan(vv / uu) 
            else:
                angle = math.pi + math.atan(vv / uu) 

            r = math.sqrt(uu * uu + vv * vv); 
            a = (angle % starangle) / starangle
  
            if a >= 0.5:
                a = 1 - a
  
            d1 = OpenMaya.MVector(r * math.cos(a), r * math.sin(a), 0.0) 
            d1 = d1 - p0
            d2 = d0 ^ d1

            def step(t, c):
                if t < c:
                    return 0.0
                else:
                    return 1.0

            in_out = step(0, d2.z) 
  
            resultColor = surfaceColor1 * in_out + surfaceColor2 * (1.0 - in_out)
            
            #set output color attribute
            outColorHandle = block.outputValue(StarTexture.aOutColor)
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter

def nodeCreator():
    return OpenMayaMPx.asMPxPtr(StarTexture())

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()

    #Create input attrubutes
    StarTexture.aNpoints = nAttr.create("npoints", "np", OpenMaya.MFnNumericData.kShort, 5)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
      
    StarTexture.aUctr = nAttr.create("uctr", "uc", OpenMaya.MFnNumericData.kFloat, 0.5)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
  
    StarTexture.aVctr = nAttr.create("vctr", "vc", OpenMaya.MFnNumericData.kFloat, 0.5)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
      
    StarTexture.aRmin = nAttr.create("rmin", "rmn", OpenMaya.MFnNumericData.kDouble, 0.07) 
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
  
    StarTexture.aRmax = nAttr.create( "rmax", "rmx", OpenMaya.MFnNumericData.kDouble, 0.2)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)

    StarTexture.aColor1 = nAttr.createColor( "color1", "c1")
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setDefault(1.0, 0.5161, 0.0)

    StarTexture.aColor2 = nAttr.createColor( "color2", "c2")
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setDefault(1.0, 1.0, 1.0)

    StarTexture.aUCoord = nAttr.create( "uCoord", "u", OpenMaya.MFnNumericData.kFloat, 0.5)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)

    StarTexture.aVCoord = nAttr.create( "vCoord", "v", OpenMaya.MFnNumericData.kFloat, 0.5)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)

    StarTexture.aUVCoord = nAttr.create( "uvCoord","uv", StarTexture.aUCoord, StarTexture.aVCoord)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setHidden(True)

    StarTexture.aFilterSizeX = nAttr.create( "uvFilterSizeX", "fsx", OpenMaya.MFnNumericData.kFloat)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setWritable(True)
    nAttr.setHidden(True)

    StarTexture.aFilterSizeY = nAttr.create( "uvFilterSizeY", "fsy", OpenMaya.MFnNumericData.kFloat)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setWritable(True)
    nAttr.setHidden(True)

    StarTexture.aFilterSize = nAttr.create("uvFilterSize","fs", StarTexture.aFilterSizeX, StarTexture.aFilterSizeY)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setWritable(True)
    nAttr.setHidden(True)

    #create output attributes here
    StarTexture.aOutColor = nAttr.createColor( "outColor", "oc")
    nAttr.setStorable(False)
    nAttr.setHidden(True)

    StarTexture.addAttribute(StarTexture.aColor1)
    StarTexture.addAttribute(StarTexture.aColor2)
    StarTexture.addAttribute(StarTexture.aUctr)
    StarTexture.addAttribute(StarTexture.aVctr)
    StarTexture.addAttribute(StarTexture.aRmin)
    StarTexture.addAttribute(StarTexture.aRmax)
    StarTexture.addAttribute(StarTexture.aNpoints)
    StarTexture.addAttribute(StarTexture.aUVCoord)
    StarTexture.addAttribute(StarTexture.aOutColor)
    StarTexture.addAttribute(StarTexture.aFilterSize)
    
    StarTexture.attributeAffects(StarTexture.aUctr, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aVctr, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aRmin, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aRmax, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aNpoints, StarTexture.aOutColor)                             
    StarTexture.attributeAffects(StarTexture.aColor1, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aColor2, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aUCoord, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aVCoord, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aUVCoord, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aFilterSizeX, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aFilterSizeY, StarTexture.aOutColor)
    StarTexture.attributeAffects(StarTexture.aFilterSize, StarTexture.aOutColor)
            
def initializePlugin( mobject ):
    ''' Initializes the plug-in. '''
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator, 
                    nodeInitializer, OpenMayaMPx.MPxNode.kDependNode, kPluginNodeClassify )
    except:
        sys.stderr.write( "Failed to register node: " + kPluginNodeName )
        raise

def uninitializePlugin( mobject ):
    ''' Unitializes the plug-in. '''
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.deregisterNode( kPluginNodeId )
    except:
        sys.stderr.write( "Failed to deregister node: " + kPluginNodeName )
        raise
