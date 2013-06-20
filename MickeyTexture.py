import sys, math

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# Plug-in information:
kPluginNodeName = 'MickeyTexture'
kPluginNodeClassify = 'texture/2d'
kPluginNodeId = OpenMaya.MTypeId(0x0000B) # this must be unique

class MickeyTexture(OpenMayaMPx.MPxNode):
    # draw mickey face procedurally

    aOutColor = OpenMaya.MObject()
    aColor1 = OpenMaya.MObject()
    aUCoord = OpenMaya.MObject()
    aVCoord = OpenMaya.MObject()
    aUVCoord = OpenMaya.MObject()
    aFilterSizeX = OpenMaya.MObject()
    aFilterSizeY = OpenMaya.MObject()
    aFilterSize = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, block):

        if (plug == MickeyTexture.aOutColor):
            bgColor = block.inputValue(MickeyTexture.aColor1).asFloatVector()
            blackColor = OpenMaya.MFloatVector()
            skinColor = OpenMaya.MFloatVector(255.0/255.0, 190.0/255.0, 132.0/255.0)
            tongueColor = OpenMaya.MFloatVector(216.0/255.0, 38.0/255.0, 31.0/255.0)
            eyeColor = OpenMaya.MFloatVector(1.0, 1.0, 1.0)
	
            resultColor = OpenMaya.MFloatVector()
            finalColor = OpenMaya.MFloatVector()

            finalBlender = 0.0;
            blender1 = 0.0;

            u = block.inputValue(MickeyTexture.aUCoord).asFloat()
            v = block.inputValue(MickeyTexture.aVCoord).asFloat()

            uu = u - math.floor(u)
            vv = v - math.floor(v)

            s = u - 0.5;
            t = v - 0.5;

            # head
            if (s * s + t * t - 0.2 * 0.2) < 0:
                finalBlender = 1.0

            #left ear
            if (s * s / (0.13 * 0.13) + (t - 0.3) * (t - 0.3) / (0.1 * 0.1)) < 1.0:
                finalBlender = 1.0 

            #right ear
            ss = s * math.cos(-math.pi/3.0) - t * math.sin(-math.pi/3.0)
            tt = s * math.sin(-math.pi/3.0) + t * math.cos(-math.pi/3.0)
            if (ss * ss / (0.13 * 0.13) + (tt - 0.3) * (tt - 0.3) / (0.1 * 0.1)) < 1.0:
                finalBlender = 1.0

            #right forehead
            s1 = (s - 0.053) * math.cos(0.7 * math.pi/2.0) - (t - 0.045) * math.sin(0.7 * math.pi/2.0)
            t1 = (s - 0.053) * math.sin(0.7 * math.pi/2.0) + (t - 0.045) * math.cos(0.7 * math.pi/2.0)
            if (s1 * s1 / (0.15 * 0.15) + t1 * t1 / (0.088 * 0.088)) < 1.0:
                blender1 = 1.0

            #cheek
            s2 = (s + 0.042) * math.cos(0.5 * math.pi/2.0) - (t + 0.116) * math.sin(0.5 * math.pi/2.0)
            t2 = (s + 0.042) * math.sin(0.5 * math.pi/2.0) + (t + 0.116) * math.cos(0.5 * math.pi/2.0)
            if (s2 * s2 / (0.105 * 0.105) + t2 * t2 / (0.07 * 0.07)) < 1.0:
                blender1 = 1.0

            #left forehead
            s3 = s * math.cos(0.85 * math.pi/2.0) - t * math.sin(0.85 * math.pi/2.0)
            t3 = s * math.sin(0.85 * math.pi/2.0) + t * math.cos(0.85 * math.pi/2.0)
            if ((s3 + 0.065) * (s3 + 0.065) / (0.12 * 0.12) + (t3 - 0.2) * (t3 - 0.2) / (0.077 * 0.077)) < 1.0:
                blender1 = 1.0

            #face
            if ((s - 0.2) * (s - 0.2) + (t + 0.15) * (t + 0.15) - (0.21 * 0.21)) < 0:
                blender1 = 1.0

            #upper mouth
            s4 = (s - 0.14) * math.cos(-0.35 * math.pi/2.0) - (t + 0.14) * math.sin(-0.35 * math.pi/2.0)
            t4 = (s - 0.14) * math.sin(-0.35 * math.pi/2.0) + (t + 0.14) * math.cos(-0.35 * math.pi/2.0)

            if (s4 * s4  / (0.09 * 0.09) + t4 * t4 / (0.06 * 0.06)) < 1.0:
                blender1 = 1.0
                finalBlender = 1.0

            #nose
            s5 = (s - 0.23) * math.cos(-0.35 * math.pi/2.0) - (t + 0.095) * math.sin(-0.35 * math.pi/2.0)
            t5 = (s - 0.23) * math.sin(-0.35 * math.pi/2.0) + (t + 0.095) * math.cos(-0.35 * math.pi/2.0)

            if (s5 * s5  / (0.05 * 0.05) + t5 * t5 / (0.035 * 0.035)) < 1.0:
		blender1 = 0
		finalBlender = 1

            #lower mouth
            s6 = (s + 0.014) * math.cos(0.9 * math.pi/2.0) - (t + 0.16) * math.sin(0.9 * math.pi/2.0)
            t6 = (s + 0.014) * math.sin(0.9 * math.pi/2.0) + (t + 0.16) * math.cos(0.9 * math.pi/2.0)

            if (s6 * s6  / (0.08 * 0.08) + t6 * t6 / (0.05 * 0.05)) < 1.0: 
                blender1 = 1
		finalBlender = 1

            #lower mouth extra
            if ((s - 0.07) * (s - 0.07) + (t + 0.15) * (t + 0.15) - (0.07 * 0.07)) < 0:
                blender1 = 1
		finalBlender = 1

            finalColor = skinColor * blender1 + blackColor * (1.0 - blender1)
            resultColor = finalColor * finalBlender + bgColor * (1.0 - finalBlender)
	
            #set output color attribute
            outColorHandle = block.outputValue(MickeyTexture.aOutColor)
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
            
        else:
            return OpenMaya.kUnknownParameter

def nodeCreator():
    return OpenMayaMPx.asMPxPtr(MickeyTexture())

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()

    #Create input attrubutes
    MickeyTexture.aColor1 = nAttr.createColor( "color1", "c1")
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setDefault(1.0, 1.0, 1.0)

    MickeyTexture.aUCoord = nAttr.create( "uCoord", "u", OpenMaya.MFnNumericData.kFloat, 0.5)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)

    MickeyTexture.aVCoord = nAttr.create( "vCoord", "v", OpenMaya.MFnNumericData.kFloat, 0.5)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)

    MickeyTexture.aUVCoord = nAttr.create( "uvCoord","uv", MickeyTexture.aUCoord, MickeyTexture.aVCoord)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)
    nAttr.setHidden(True)

    MickeyTexture.aFilterSizeX = nAttr.create( "uvFilterSizeX", "fsx", OpenMaya.MFnNumericData.kFloat)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setWritable(True)
    nAttr.setHidden(True)

    MickeyTexture.aFilterSizeY = nAttr.create( "uvFilterSizeY", "fsy", OpenMaya.MFnNumericData.kFloat)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setWritable(True)
    nAttr.setHidden(True)

    MickeyTexture.aFilterSize = nAttr.create("uvFilterSize","fs",MickeyTexture.aFilterSizeX,MickeyTexture.aFilterSizeY)
    nAttr.setStorable(False)
    nAttr.setReadable(True)
    nAttr.setWritable(True)
    nAttr.setHidden(True)

    #create output attributes here
    MickeyTexture.aOutColor = nAttr.createColor( "outColor", "oc")
    nAttr.setStorable(False)
    nAttr.setHidden(True)

    MickeyTexture.addAttribute(MickeyTexture.aColor1)
    MickeyTexture.addAttribute(MickeyTexture.aUVCoord)
    MickeyTexture.addAttribute(MickeyTexture.aOutColor)
    MickeyTexture.addAttribute(MickeyTexture.aFilterSize)
    
    MickeyTexture.attributeAffects(MickeyTexture.aColor1, MickeyTexture.aOutColor)
    MickeyTexture.attributeAffects(MickeyTexture.aUCoord, MickeyTexture.aOutColor)
    MickeyTexture.attributeAffects(MickeyTexture.aVCoord, MickeyTexture.aOutColor)
    MickeyTexture.attributeAffects(MickeyTexture.aUVCoord, MickeyTexture.aOutColor)
    MickeyTexture.attributeAffects(MickeyTexture.aFilterSizeX, MickeyTexture.aOutColor)
    MickeyTexture.attributeAffects(MickeyTexture.aFilterSizeY, MickeyTexture.aOutColor)
    MickeyTexture.attributeAffects(MickeyTexture.aFilterSize, MickeyTexture.aOutColor)
            
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
