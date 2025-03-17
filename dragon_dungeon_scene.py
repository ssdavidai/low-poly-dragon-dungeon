import bpy
import math
import random

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a new collection for our scene
dungeon_collection = bpy.data.collections.new("DungeonScene")
bpy.context.scene.collection.children.link(dungeon_collection)

# Set active collection
layer_collection = bpy.context.view_layer.layer_collection.children[dungeon_collection.name]
bpy.context.view_layer.active_layer_collection = layer_collection

# Create materials
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    principled_bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if principled_bsdf:
        principled_bsdf.inputs[0].default_value = color
    return mat

# Create materials
floor_mat = create_material("FloorMaterial", (0.05, 0.05, 0.05, 1.0))  # Dark grey
wall_mat = create_material("WallMaterial", (0.1, 0.1, 0.12, 1.0))  # Dark grey-blue
dragon_mat = create_material("DragonMaterial", (0.7, 0.2, 0.1, 1.0))  # Red
gold_mat = create_material("GoldMaterial", (1.0, 0.8, 0.0, 1.0))  # Gold
pot_mat = create_material("PotMaterial", (0.1, 0.1, 0.1, 1.0))  # Dark grey

# Helper to assign material
def assign_material(obj, material):
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

# Create floor
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "DungeonFloor"
assign_material(floor, floor_mat)

# Create back wall
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 5, 5))
back_wall = bpy.context.active_object
back_wall.name = "BackWall"
back_wall.rotation_euler = (math.radians(90), 0, 0)
assign_material(back_wall, wall_mat)

# Create side walls
bpy.ops.mesh.primitive_plane_add(size=10, location=(-5, 0, 5))
left_wall = bpy.context.active_object
left_wall.name = "LeftWall"
left_wall.rotation_euler = (0, math.radians(90), 0)
assign_material(left_wall, wall_mat)

bpy.ops.mesh.primitive_plane_add(size=10, location=(5, 0, 5))
right_wall = bpy.context.active_object
right_wall.name = "RightWall"
right_wall.rotation_euler = (0, math.radians(90), 0)
assign_material(right_wall, wall_mat)

# Create a low-poly dragon
bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=1.5, radius2=0, depth=4, location=(0, 0, 2))
dragon_body = bpy.context.active_object
dragon_body.name = "DragonBody"
assign_material(dragon_body, dragon_mat)

# Dragon head
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.8, radius2=0, depth=2, location=(0, -2.5, 2.5))
dragon_head = bpy.context.active_object
dragon_head.name = "DragonHead"
dragon_head.rotation_euler = (math.radians(-30), 0, 0)
assign_material(dragon_head, dragon_mat)

# Dragon legs
for x, y in [(-0.8, 0.8), (0.8, 0.8), (-0.8, -0.8), (0.8, -0.8)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=5, radius=0.3, depth=1.5, location=(x, y, 0.75))
    leg = bpy.context.active_object
    leg.name = f"DragonLeg_{x}_{y}"
    assign_material(leg, dragon_mat)

# Dragon wings
for side in [-1, 1]:
    bpy.ops.mesh.primitive_plane_add(size=2, location=(side * 1.2, 0, 2.5))
    wing = bpy.context.active_object
    wing.name = f"DragonWing_{side}"
    wing.rotation_euler = (0, math.radians(60 * side), math.radians(30))
    
    # Triangulate the wing for low-poly look
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.triangulate(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    assign_material(wing, dragon_mat)

# Dragon tail
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.5, radius2=0.1, depth=3, location=(0, 2.5, 1.5))
tail = bpy.context.active_object
tail.name = "DragonTail"
tail.rotation_euler = (math.radians(30), 0, 0)
assign_material(tail, dragon_mat)

# Create a pot of gold
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1, depth=1.5, location=(2, -2, 0.75))
pot = bpy.context.active_object
pot.name = "Pot"
assign_material(pot, pot_mat)

# Gold coins (simplified as small cylinders)
for i in range(15):
    x = 2 + random.uniform(-0.5, 0.5)
    y = -2 + random.uniform(-0.5, 0.5)
    z = 1.5 + random.uniform(0, 0.4)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.2, depth=0.05, location=(x, y, z))
    coin = bpy.context.active_object
    coin.name = f"GoldCoin_{i}"
    coin.rotation_euler = (random.uniform(0, 0.5), random.uniform(0, 0.5), random.uniform(0, 3.14))
    assign_material(coin, gold_mat)

# Add a simple torch on the wall for lighting effect
bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.1, depth=1, location=(-4, 4, 4))
torch = bpy.context.active_object
torch.name = "Torch"
torch.rotation_euler = (math.radians(30), 0, 0)

# Add a point light for the torch
bpy.ops.object.light_add(type='POINT', radius=1, location=(-4, 4, 4))
light = bpy.context.active_object
light.name = "TorchLight"
light.data.energy = 50
light.data.color = (1.0, 0.7, 0.4)

# Add atmospheric light
bpy.ops.object.light_add(type='AREA', location=(0, 0, 8))
ambient_light = bpy.context.active_object
ambient_light.name = "AmbientLight"
ambient_light.data.energy = 30
ambient_light.scale = (10, 10, 10)
ambient_light.data.color = (0.2, 0.3, 0.5)  # Bluish atmospheric light

# Set up camera
bpy.ops.object.camera_add(location=(8, -8, 6))
camera = bpy.context.active_object
camera.name = "DungeonCamera"
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
bpy.context.scene.camera = camera

# Apply low-poly look to everything
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        # Add edge split modifier for sharp edges
        edge_split = obj.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
        edge_split.split_angle = math.radians(30)
        
        # Triangulate modifier for low-poly look
        triangulate = obj.modifiers.new(name="Triangulate", type='TRIANGULATE')
        
        bpy.ops.object.shade_smooth()
        obj.select_set(False)

# Set render settings for preview
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'

print("Low poly dungeon scene with dragon guarding gold created successfully!")
