import sys, math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# Plug-in information:
kPluginNodeName = "TaegukTexture"
kPluginNodeClassify = "texture/2d"
kPluginNodeId = OpenMaya.MTypeId(0x0000D) # change this to be unique

class TaegukTexture(OpenMayaMPx.MPxNode):
    aOutColor = OpenMaya.MObject()
    aUCoord = OpenMaya.MObject()
    aVCoord = OpenMaya.MObject()
    aUVCoord = OpenMaya.MObject()
    aFilterSizeX = OpenMaya.MObject()
    aFilterSizeY = OpenMaya.MObject()
    aFilterSize = OpenMaya.MObject()
    aRadius = OpenMaya.MObject()
    aColor1 = OpenMaya.MObject()
    aColor2 = OpenMaya.MObject()
    aColor3 = OpenMaya.MObject()
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, block):
        if (plug == TaegukTexture.aOutColor):
            resultColor = OpenMaya.MFloatVector()
            resultColor2 = OpenMaya.MFloatVector()
            
            u = block.inputValue(TaegukTexture.aUCoord).asFloat()
            v = block.inputValue(TaegukTexture.aVCoord).asFloat()
  
            radius = block.inputValue(TaegukTexture.aRadius).asFloat()
  
            surfaceColor1 = block.inputValue(TaegukTexture.aColor1).asFloatVector()
            surfaceColor2 = block.inputValue(TaegukTexture.aColor2).asFloatVector()
            surfaceColor3 = block.inputValue(TaegukTexture.aColor3).asFloatVector()
  
            uu = u - math.floor(u)
            vv = v - math.floor(v)
  
            s = (uu - 0.5) * (3.0 / math.sqrt(13.0)) - (vv - 0.5) * (2.0 / math.sqrt(13.0))
            t = (uu - 0.5) * (2.0 / math.sqrt(13.0)) + (vv - 0.5) * (3.0 / math.sqrt(13.0))

            def inCircle(cx, cy, r, x, y):
                if ((x - cx) * (x - cx) + (y - cy) * (y - cy) - r * r) <= 0:
                    return 1.0
                else:
                    return 0.0
 
            in_out = inCircle(0, 0, radius, s, t)
            in_red = 0.0
  
            if in_out > 0: 
                if t >= 0:
                    in_red = math.fabs(1 - inCircle(radius/2.0, 0.0, radius/2.0, s, t))
                else:
                    in_red = inCircle(- radius/2.0, 0.0, radius/2.0, s, t)
  
            resultColor2 = surfaceColor1 * in_red + surfaceColor2 * (1.0 - in_red)
            resultColor = resultColor2 * in_out + surfaceColor3 * (1.0 - in_out)

            #set output color attribute
            outColorHandle = block.outputValue(TaegukTexture.aOutColor)
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()            
        else:
            return OpenMaya.kUnknownParameter

def nodeCreator():
    return OpenMayaMPx.asMPxPtr(TaegukTexture())

def nodeInitializer():
    # create attributes here
    nAttr = OpenMaya.MFnNumericAttribute()

    TaegukTexture.aRadius = nAttr.create( "radius", "r", OpenMaya.MFnNumericData.kFloat, 0.25)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(0.5)

    TaegukTexture.aColor1 = nAttr.createColor( "color1", "c1")
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setDefault(1.0, 0.0, 0.0)

    TaegukTexture.aColor2 = nAttr.createColor( "color2", "c2")
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setDefault(0.0, 0.0, 1.0)

    TaegukTexture.aColor3 = nAttr.createColor( "color3", "c3")
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setDefault(1.0, 1.0, 1.0)

    TaegukTexture.aUCoord = nAttr.create( "uCoord", "u", OpenMaya.MFnNumericData.kFloat, 0.5)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)

    TaegukTexture.aVCoord = nAttr.create( "vCoord", "v", OpenMaya.MFnNumericData.kFloat, 0.5)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)

    TaegukTexture.aUVCoord = nAttr.create( "uvCoord","uv", TaegukTexture.aUCoord, TaegukTexture.aVCoord)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setHidden(True)

    TaegukTexture.aFilterSizeX = nAttr.create( "uvFilterSizeX", "fsx", OpenMaya.MFnNumericData.kFloat)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setWritable(True)
    nAttr.setHidden(True)

    TaegukTexture.aFilterSizeY = nAttr.create( "uvFilterSizeY", "fsy", OpenMaya.MFnNumericData.kFloat)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setWritable(True)
    nAttr.setHidden(True)

    TaegukTexture.aFilterSize = nAttr.create("uvFilterSize","fs", TaegukTexture.aFilterSizeX, TaegukTexture.aFilterSizeY)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setWritable(True)
    nAttr.setHidden(True)

    TaegukTexture.aOutColor = nAttr.createColor( "outColor", "oc")
    nAttr.setStorable(False)
    nAttr.setHidden(True)

    TaegukTexture.addAttribute(TaegukTexture.aColor1)
    TaegukTexture.addAttribute(TaegukTexture.aColor2)
    TaegukTexture.addAttribute(TaegukTexture.aColor3)
    TaegukTexture.addAttribute(TaegukTexture.aRadius)    
    TaegukTexture.addAttribute(TaegukTexture.aUVCoord)
    TaegukTexture.addAttribute(TaegukTexture.aFilterSize)
    TaegukTexture.addAttribute(TaegukTexture.aOutColor)

    TaegukTexture.attributeAffects(TaegukTexture.aRadius, TaegukTexture.aOutColor)
    TaegukTexture.attributeAffects(TaegukTexture.aColor1, TaegukTexture.aOutColor)
    TaegukTexture.attributeAffects(TaegukTexture.aColor2, TaegukTexture.aOutColor)
    TaegukTexture.attributeAffects(TaegukTexture.aColor3, TaegukTexture.aOutColor)    
    TaegukTexture.attributeAffects(TaegukTexture.aUCoord, TaegukTexture.aOutColor)
    TaegukTexture.attributeAffects(TaegukTexture.aVCoord, TaegukTexture.aOutColor)
    TaegukTexture.attributeAffects(TaegukTexture.aUVCoord, TaegukTexture.aOutColor)
    TaegukTexture.attributeAffects(TaegukTexture.aFilterSizeX, TaegukTexture.aOutColor)
    TaegukTexture.attributeAffects(TaegukTexture.aFilterSizeY, TaegukTexture.aOutColor)
    TaegukTexture.attributeAffects(TaegukTexture.aFilterSize, TaegukTexture.aOutColor)

def initializePlugin( mobject ):
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator,
        nodeInitializer, OpenMayaMPx.MPxNode.kDependNode, kPluginNodeClassify )
    except:
        sys.stderr.write( "Failed to register node: " + kPluginNodeName )
        raise

def uninitializePlugin( mobject ):
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.deregisterNode( kPluginNodeId )
    except:
        sys.stderr.write( "Failed to deregister node: " + kPluginNodeName )
        raise

