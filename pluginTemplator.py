#! /usr/bin/python
def write_plugin_import():
    import_str = ('import sys\n'
                  'import maya.OpenMaya as OpenMaya\n'
                  'import maya.OpenMayaMPx as OpenMayaMPx\n\n')

    return import_str

def write_plugin_init():
    plugin_init_str = ('def initializePlugin( mobject ):\n'
                       '\tmplugin = OpenMayaMPx.MFnPlugin( mobject )\n'
                       '\ttry:\n'
                       '\t\tmplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator,\n'
                       '\t\tnodeInitializer, OpenMayaMPx.MPxNode.kDependNode, kPluginNodeClassify )\n'
                       '\texcept:\n'
                       '\t\tsys.stderr.write( "Failed to register node: " + kPluginNodeName )\n'
                       '\t\traise\n\n'
                       'def uninitializePlugin( mobject ):\n'
                       '\tmplugin = OpenMayaMPx.MFnPlugin( mobject )\n'
                       '\ttry:\n'
                       '\t\tmplugin.deregisterNode( kPluginNodeId )\n'
                       '\texcept:\n'
                       '\t\tsys.stderr.write( "Failed to deregister node: " + kPluginNodeName )\n'
                       '\t\traise\n\n')
    return plugin_init_str

def write_plugin_class(name, pluginType):
    parentClass = 'OpenMayaMPx.MPxNode'
	
    plugin_class_str = 'class ' + name +'(' + parentClass + '):\n\n'

    if pluginType == 'texture/2d':
        plugin_class_str += ('\taOutColor = OpenMaya.MObject()\n'
                             '\taUCoord = OpenMaya.MObject()\n'
                             '\taVCoord = OpenMaya.MObject()\n'
                             '\taUVCoord = OpenMaya.MObject()\n'
                             '\taFilterSizeX = OpenMaya.MObject()\n'
                             '\taFilterSizeY = OpenMaya.MObject()\n'
                             '\taFilterSize = OpenMaya.MObject()\n\n')

    plugin_class_str += ('\tdef __init__(self):\n'
			'\t\t' + parentClass + '.__init__(self)\n\n')

    if pluginType == 'texture/2d':
        plugin_class_str += ('\tdef compute(self, plug, block):\n'
                             '\t\tif (plug == ' + name + '.aOutColor):\n'
                             '\t\t\tresultColor = OpenMaya.MFloatVector()\n'
                             '\t\t\tu = block.inputValue(' + name + '.aUCoord).asFloat()\n'
                             '\t\t\tv = block.inputValue(' + name + '.aVCoord).asFloat()\n\n'
                             '\t\t\t# write compute function here\n\n'
                             '\t\t\t#set output color attribute\n'
                             '\t\t\toutColorHandle = block.outputValue(' + name + '.aOutColor)\n'
                             '\t\t\toutColorHandle.setMFloatVector(resultColor)\n'
                             '\t\t\toutColorHandle.setClean()\n'
                             '\t\telse:\n'
                             '\t\t\treturn OpenMaya.kUnknownParameter\n\n')

    return plugin_class_str

def write_plugin_node_init(name, pluginType):
    plugin_node_init_str = ('def nodeCreator():\n'
                            '\treturn OpenMayaMPx.asMPxPtr(' + name + '())\n\n'
                            'def nodeInitializer():\n'
                            '\t# create attributes here\n'
                            )

    if pluginType == 'texture/2d':
        plugin_node_init_str += ('\tnAttr = OpenMaya.MFnNumericAttribute()\n\n'
                                 '\t' + name + '.aUCoord = nAttr.create( "uCoord", "u", OpenMaya.MFnNumericData.kFloat, 0.5)\n'
				 '\tnAttr.setKeyable(True)\n'
                                 '\tnAttr.setStorable(True)\n\n'
				 '\t' + name + '.aVCoord = nAttr.create( "vCoord", "v", OpenMaya.MFnNumericData.kFloat, 0.5)\n'
				 '\tnAttr.setKeyable(True)\n'
				 '\tnAttr.setStorable(True)\n\n'
                                 '\t' + name + '.aUVCoord = nAttr.create( "uvCoord","uv", ' + name + '.aUCoord, ' + name + '.aVCoord)\n'
				 '\tnAttr.setKeyable(True)\n'
				 '\tnAttr.setStorable(True)\n'
				 '\tnAttr.setHidden(True)\n\n'
				 '\t' + name + '.aFilterSizeX = nAttr.create( "uvFilterSizeX", "fsx", OpenMaya.MFnNumericData.kFloat)\n'
				 '\tnAttr.setStorable(False)\n'
				 '\tnAttr.setReadable(True)\n'
				 '\tnAttr.setWritable(True)\n'
				 '\tnAttr.setHidden(True)\n\n'
				 '\t' + name + '.aFilterSizeY = nAttr.create( "uvFilterSizeY", "fsy", OpenMaya.MFnNumericData.kFloat)\n'
				 '\tnAttr.setStorable(False)\n'
				 '\tnAttr.setReadable(True)\n'
				 '\tnAttr.setWritable(True)\n'
				 '\tnAttr.setHidden(True)\n\n'
				 '\t' + name + '.aFilterSize = nAttr.create("uvFilterSize","fs", ' + name + '.aFilterSizeX, ' + name + '.aFilterSizeY)\n'
				 '\tnAttr.setStorable(False)\n'
				 '\tnAttr.setReadable(True)\n'
				 '\tnAttr.setWritable(True)\n'
                                 '\tnAttr.setHidden(True)\n\n'
                                 '\t' + name + '.aOutColor = nAttr.createColor( "outColor", "oc")\n'
				 '\tnAttr.setStorable(False)\n'
				 '\tnAttr.setHidden(True)\n\n'
				 '\t' + name + '.addAttribute(' + name + '.aUVCoord)\n'
				 '\t' + name + '.addAttribute(' + name + '.aFilterSize)\n'
				 '\t' + name + '.addAttribute(' + name + '.aOutColor)\n\n'
				 '\t' + name + '.attributeAffects(' + name + '.aUCoord, ' + name + '.aOutColor)\n'
				 '\t' + name + '.attributeAffects(' + name + '.aVCoord, ' + name + '.aOutColor)\n'
				 '\t' + name + '.attributeAffects(' + name + '.aUVCoord, ' + name + '.aOutColor)\n'
				 '\t' + name + '.attributeAffects(' + name + '.aFilterSizeX, ' + name + '.aOutColor)\n'
				 '\t' + name + '.attributeAffects(' + name + '.aFilterSizeY, ' + name + '.aOutColor)\n'
				 '\t' + name + '.attributeAffects(' + name + '.aFilterSize, ' + name + '.aOutColor)\n\n')
    else:
        plugin_node_init_str += '\tpass\n\n'
        
    return plugin_node_init_str

def write_template(name, pluginType):
    f = open(name + '.py', 'w')
    f.write(write_plugin_import().replace('\t', ' '*4))
    f.write('# Plug-in information:\n')
    f.write('kPluginNodeName = "' + name + '"\n')
    f.write('kPluginNodeClassify = "' + pluginType + '"\n')
    f.write('kPluginNodeId = OpenMaya.MTypeId(0x00000) # change this to be unique\n\n')
    f.write(write_plugin_class(name, pluginType).replace('\t', ' '*4))
    f.write(write_plugin_node_init(name, pluginType).replace('\t', ' '*4))
    f.write(write_plugin_init().replace('\t', ' '*4))
    f.close()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 3:
        write_template(argv[1], argv[2])
    else:
        print 'Usage:\n\tpluginTemplator.py <plugin name> <plugin type>\nExample:\n\tpluginTemplator.py MyTexture texture/2d'
    
    
    
    
