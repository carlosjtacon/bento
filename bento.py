import sys
import pathlib
import shutil
import unicodedata
import re
<<<<<<< HEAD
=======

>>>>>>> main

def exit():
	print('Usage: bento.py [preview|rename|gitarchive] [/path/to/folder] [options: ascii]')
	sys.exit(0)

def unidecode(s):
	n= unicodedata.normalize('NFKD', s)  
	res = ''.join([c for c in n if not unicodedata.combining(c)]) 
	return res

def clean_name(path):
	new_name = path.stem.rstrip() + path.suffix
	new_name = re.sub(' +', ' ', new_name)
	
	if 'ascii' in sys.argv:
		new_name = unidecode(new_name)
	
	return new_name

arguments = sys.argv

if len(arguments) < 3:
	exit()

mode = 0
mode = 1 if arguments[1] == 'preview' else mode
mode = 2 if arguments[1] == 'rename' else mode
mode = 3 if arguments[1] == 'gitarchive' else mode

path = pathlib.Path(arguments[2])

if not mode or not path.exists():
	exit()

print('Previewing' if mode == 1 else 'Renaming' if mode == 2 else 'Archiving Repos' if mode == 3 else None, path.absolute(), '\n')

gitrepos = []

for root, dirs, files in path.walk(on_error=print):
	if '.git' in dirs:
		dirs.remove('.git')
		print(root, 'is a Git repository.')
		
		if mode == 3:
			print('Zipping', root)
			zipdir = root.absolute().as_posix()
			shutil.make_archive(zipdir, 'zip', zipdir)
			gitrepos.append(zipdir)
	
	numfiles = len(files) + len(dirs)
	if numfiles > 3000:
		print('Warning: Folder', root, 'has too many files ({})'.format(numfiles))
	
	for i, dir in enumerate(dirs):
		dirpath = root / dir
		dir_clean = clean_name(dirpath)
		if dirpath.name != dir_clean:
			print('Folder', dirpath, 'is not good / Should be', dir_clean)
			newpath = dirpath.parent / dir_clean
			if newpath.exists():
				print('Error', newpath, 'already exists')
			if mode == 2:
				print('Renaming', dirpath, 'to', newpath)
				dirpath.rename(newpath)
				dirpath = newpath
		dirs[i] = dirpath.name
		
	for file in files:
		filepath = root / file
		gb = filepath.stat().st_size / 2 ** 30
		name_clean = clean_name(filepath)
		if filepath.name != name_clean:
			print('File', filepath, 'is not good / Should be', name_clean)
			if mode == 2:
				newpath = filepath.parent / name_clean
				print('Renaming', filepath, 'to', newpath)
				filepath.rename(newpath)
		if gb > 49:
			print('File', filepath, 'is too large ({} GB)'.format(gb))
		

if mode == 3 and gitrepos:			
	print('To remove zipped git repos run:')
	print('rm -r \'' + '\' \''.join(gitrepos) + '\'')
