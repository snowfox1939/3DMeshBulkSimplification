#!/usr/bin/python3
import os
import sys
import inspect
import meshlabxml as mlx
import platform
import glob
import shutil
import time
from threading import Thread

'''
Description: It takes via normal script "simplifybulk.py" 17 minutes to Decimate a 3M faces into 7 resolutions
			 [100K, 200K, 300K, 400K, 500K, 600K, 750K]. With this version of the program, I have included threading
			 so the time it takes now is only around 5 minutes (a considerable improvement).
Usage: python3 simplifybulkthreaded.py
You can of course include functionality to take arguments from command line/terminal like I did in simplify.py
DO NOT FORGET to change: Decimations_List, originalMesh (name of original mesh), SimplifiedMesh & Textures to what suits you.
Enjoy!
'''



def simplify(originalMeshName, SimplifiedMeshName, NumberOfFaces, WithTexture):
	# File names
	FilterScript = 'SimplificationFilter.mlx'  # script file
	original_mesh = originalMeshName # input file
	simplified_mesh = SimplifiedMeshName  # output file
	Num_Of_Faces = int(NumberOfFaces)  # Final Number of Faces


	#Check the input mesh number of faces (so that we do not decimate to a higher number of faces than original mesh)
	MetricsMeshDictionary = {}
	MetricsMeshDictionary = mlx.files.measure_topology(original_mesh)
	#print (MetricsMeshDictionary)
	print('\n Number of faces of original mesh is: ' + str(MetricsMeshDictionary['face_num'] )) 

	if(MetricsMeshDictionary['face_num'] <= Num_Of_Faces):
	    #exit the script and print a message about it
	    print("\n SORRY your decimated mesh can not have higher number of faces that the input mesh.....")
	    print("\n ......................................................................................")
	    sys.exit()

	#Creating a folder named as the Number of faces: named '150000'
	print('\n Creating a folder to store the decimated model ...........')
	if not os.path.exists(str(Num_Of_Faces)):
	    os.makedirs(str(Num_Of_Faces))


	simplified_meshScript = mlx.FilterScript(file_in=original_mesh, file_out=str(Num_Of_Faces) + '/' + simplified_mesh,
	                                         ml_version='2016.12')  # Create FilterScript object

	mlx.remesh.simplify(simplified_meshScript, texture=WithTexture, faces=Num_Of_Faces,
	                    target_perc=0.0, quality_thr=1.0, preserve_boundary=True,
	                    boundary_weight=1.0, preserve_normal=True,
	                    optimal_placement=True, planar_quadric=True,
	                    selected=False, extra_tex_coord_weight=1.0)
	print('\n Beginning the process of Decimation ...........')

	simplified_meshScript.run_script()  # Run the script
	os.chdir(str(Num_Of_Faces))
	print('\n Process of Decimation Finished ...')
	print('\n Copying textures (PNG and JPEG) into the folder of decimated model....')

	#go back to parent directory so we can copy the textures to the 3D Model folder
	os.chdir('..')

	#Now checking for textures in the folder of the input mesh.... (plz change if needed)
	allfilelist= os.listdir('.')

	for Afile in allfilelist[:]: 
	    if not(Afile.endswith(".png") or Afile.endswith(".PNG") or Afile.endswith(".jpg") or Afile.endswith(".JPG")):
	        allfilelist.remove(Afile)
	print('\n Found the LIST of images in PNG and JPEG (textures): ')
	print(allfilelist)

	for file in allfilelist:
	    shutil.copy(file, str(Num_Of_Faces))

	print('\n sleeping for 3 seconds.... ')
	time.sleep(3)


Decimations_List = [100000, 200000, 300000, 400000, 500000, 600000, 750000]
originalMesh = 'Lantern.1.obj'
SimplifiedMesh = 'Lantern_Simplified.obj'
Textures = True

print("...........Starting timer for the decimation process............")
initial_time = time.time()

threads_list = []

for decimationResolution in Decimations_List:
	threads_list.append(Thread(target=simplify, args=(originalMesh, SimplifiedMesh, decimationResolution, Textures)))

for thread in threads_list:
    try:
        thread.start()
    except KeyboardInterrupt: # std Python exception
        continue # moves to next thread iterable

#Waiting for all threads to finish
thread.join()


print("I Finished Decimating in tandem.....")

finish_time = time.time()
print("---Decimation Process took: %s seconds ---" % (finish_time - initial_time))
print("\n Done.... have a good day!")
