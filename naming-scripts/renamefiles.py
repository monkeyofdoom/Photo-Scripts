# Created by: James Glennie
# Date: 2012-05-08
# Some code copied and modified from various web pages
# Requires the free 'exiftool' utility: http://owl.phy.queensu.ca/~phil/exiftool/
# Last updated: 2012-09-03

import os, time, sys, string
# from stat import * # ST_SIZE etc

extlist = [".JPG",".CR2",".DNG",".MOV",".AVI",".3GP",".MP4"]
movietypes = [".MOV",".AVI"]     

path = sys.argv[1]
if os.path.exists(path):
	listing = os.listdir(path)
	for infile in listing:
		createdate = ""
		oldfile = "";
		ext = os.path.splitext(infile)
		if ext[1].upper() in extlist:
			# check to see if the file has an associated THM file
			if ext[1].upper() in movietypes:
				if os.path.isfile(path+ext[0]+".THM"):
					oldfile = infile
					infile = ext[0]+".THM"

			fi,fo,fe = os.popen3("exiftool -S -s -SubSecCreateDate '" + path+infile + "'")
			for createdate in fo.readlines():
				createdate = createdate.strip()
				createdate = string.replace(createdate,":","-")
				createdate = string.replace(createdate," ","_")
				createdate = string.replace(createdate,".","-")

			# If subsec wasn't found, use general createdate 
			if createdate == "":
				fi,fo,fe = os.popen3("exiftool -S -s -CreateDate '" + path+infile + "'")
				for createdate in fo.readlines():	
					createdate = createdate.strip()
					createdate = string.replace(createdate,":","-")
					createdate = string.replace(createdate," ","_")
					createdate = string.replace(createdate,".","-")

			#TODO : add support for fallback on file creation date
			
			if createdate != "":
				# set the base file back to the original
				if oldfile != "":
					infile = oldfile

				basefilename = createdate
				newfilename = basefilename + ext[1]
				
				renamefrom = path+infile
				renameto = path+newfilename

				#TODO : add support for creating/moving to subfolders based on year/month
				if renamefrom != renameto:
					if not os.path.isfile(renameto):
						print('renaming file ' + infile + ' to ' + newfilename)
						os.rename(path+infile, path+newfilename)

				if oldfile != "":
					renamefrom = path + ext[0] + ".THM";
					renameto = path + basefilename + ".THM"
					if renamefrom != renameto:
						if not os.path.isfile(renameto):
							print('renaming file ' + ext[0] + '.THM' + ' to ' + basefilename + '.THM')
							os.rename(path + ext[0] + ".THM", path + basefilename + ".THM")

