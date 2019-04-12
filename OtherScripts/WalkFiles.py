
import os
import uuid

config = {"Integration":"OI.FFM.InboundServices","Dispatcher":"OI.FFM.Notifications","MUA":"OI.FFM.Web"}

for context in ["Integration", "Dispatcher", "MUA"]:

    path_to_components = 'C:/Users/pedro.arguelles/Desktop/components_'+context
    path_to_refs = 'C:/Users/pedro.arguelles/Desktop/refs_'+context
    path_to_mua = 'C:/Users/pedro.arguelles/Desktop/'+context+'/'


    path_to_repository = 'C:/Users/pedro.arguelles/Desktop/Repos/oi-mua/src/'+config[context]

    refs = open(path_to_refs, 'w')
    components = open(path_to_components,'w')

    # Get each component to include in the installer
    for subdir, dirs, files in os.walk(path_to_mua):
        for file in files:

            # Find the path in the repository
            path = ""
            for subdir2, dirs2, files2 in os.walk(path_to_repository):
                for file2 in files2:
                    if str(file) == str(file2) and config[context] in subdir2:
                        path = '/'.join(str(subdir2).split('/')[7:])
                        path = str(path).replace('/','\\')
                        path = path+"\\"+str(file2)
                        break

            # Write the component and reference files
            if path != "":
                refs.write("<Component Id=\""+file+"\" Guid=\""+str(uuid.uuid4())+"\">\n")
                refs.write("    <File Id=\""+file+"\" Name=\""+file+"\"  KeyPath=\"yes\" DiskId=\"1\" Source=\"$(var.SolutionDir)"+str(path)+"\"/>\n")
                refs.write("</Component>\n")

                components.write("<ComponentRef Id=\""+file+"\"/>\n")

    refs.close()
    components.close()