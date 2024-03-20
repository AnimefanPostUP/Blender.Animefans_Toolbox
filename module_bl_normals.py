

def smoothObjects (self, context):
    #Shade Smooth all selected Objects
    wasInObjectmode=False
    
    if bpy.context.mode != 'EDIT_MESH':
        wasInObjectmode=True
        bpy.ops.object.mode_set(mode='EDIT')
    
    selected_Objects=bpy.context.selected_objects
    for obj in selected_Objects:
        if not obj.type == 'MESH':
                continue
                
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        for f in bm.faces:
            f.smooth = True
            
    if wasInObjectmode:
        bpy.ops.object.mode_set(mode='OBJECT')        
    bpy.context.view_layer.update()
    
def splitNormals(self, context):
    settingsdata = bpy.context.scene.ttb_settings_data

    autosmooth= settingsdata.autosmooth
    clear= settingsdata.cleanSplitNormals
    activeMode=False
    
    #check if self has angle attribute
    if not hasattr(self, "angle"):
        angle = settingsdata.splitangle
        activeMode = True
    else:
        angle=self.angle
        
    
        
    edgecount=0      
    selected_Objects=bpy.context.selected_objects         
    if activeMode:
        #count selected edges using bmesh
        for obj in selected_Objects:
            if not obj.type == 'MESH':
                continue
                
            #get selected edges
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            for edge in bm.edges:
                if edge.select:
                    edgecount+=1    

    #Deselect objects that arent meshes
    for obj in selected_Objects:
        if not obj.type == 'MESH':
            obj.select_set(False)
           

      #go to edit mode if not already 
    if bpy.context.mode != 'EDIT_MESH':
        wasInObjectmode=True
        bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.context.tool_settings.mesh_select_mode = (False, True, False)    
        
        
    
    if(autosmooth):
        smoothObjects(self, context)
        
    if clear: # Clear if needed
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_sharp(clear=True)
        
        bpy.ops.mesh.customdata_custom_splitnormals_clear()    
           
    wasInObjectmode=False
    
    
    

        
    #Deselect all Edges first 
    bpy.ops.mesh.select_all(action='DESELECT')
    
    #Select all edges with a sharp edge angle
    bpy.ops.mesh.edges_select_sharp(sharpness=math.radians(angle))
    
    secondedgecount=0
    
    if activeMode:
        for obj in selected_Objects:
            if not obj.type == 'MESH':
                continue
                
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            for edge in bm.edges:
                if edge.select:
                    secondedgecount+=1
            
    if activeMode:
        if edgecount>secondedgecount or edgecount<secondedgecount:
            bpy.ops.ed.undo_push(message = "Push Undo (Split Normals Operator): "+str(abs(edgecount-secondedgecount)) + " Edges Changed")
            #print(str(abs(edgecount-secondedgecount)))
    
    #Split Normals of the selected edges
    bpy.ops.mesh.split_normals()
    # if not activeMode:
    #     bpy.ops.view3d.update_edit_mesh()
            
    # if not wasInObjectmode:
    #     bpy.ops.object.mode_set(mode='OBJECT')
    # else:
    #     bpy.ops.object.mode_set(mode='EDIT')
