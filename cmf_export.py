import bpy
import bmesh
import struct

def writeFile(filepath="", select_only=False):
    file = open(filepath, "wb")
    file.write(b"COLUMBUS MODEL FILE")

    count = 0
    for ob in bpy.context.scene.objects:
        try:
            ob.data.polygons
        except AttributeError:
            continue

        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.object.mode_set(mode='OBJECT')

        count+=len(ob.data.polygons)

    file.write(struct.pack("I", count))
    bpy.ops.object.mode_set(mode='OBJECT')

    verts = []
    uvs = []
    norms = []

    for ob in bpy.context.scene.objects:
        try:
            ob.data.polygons
        except AttributeError:
            continue

        for face in ob.data.polygons:
            for vert, loop in zip(face.vertices, face.loop_indices):
                for item in ob.data.vertices[vert].co: #Vertex
                    verts.append(item)
                for item in (ob.data.uv_layers.active.data[loop].uv if ob.data.uv_layers.active != None else (0, 0)): #UV
                    uvs.append(item)
                for item in ob.data.vertices[vert].normal: #Normal
                    norms.append(item)

        for elem in verts:
            file.write(struct.pack('f', elem))

        for elem in uvs:
            file.write(struct.pack('f', elem))

        for elem in norms:
            file.write(struct.pack('f', elem))


