import os

fin = open("build.ninja", "rt")
fout = open("build.ninja.new", "wt")
gomp = None
iomp5 = None

ignore = True
for line in fin:
    if "Link the executable bin/ogs" in line:
        ignore = False
    if ignore is False:
        linesplit = line.split(" ")
        for entry in linesplit:
            if ("-lgomp" in entry) or ("libgomp.so" in entry):
                if gomp is None:
                    gomp = entry
            elif ("-liomp5" in entry) or ("libiomp5.so" in entry):
                if iomp5 is None:
                    iomp5 = entry
    if (gomp is not None) and (iomp5 is not None):
        newline = line.replace(gomp,"XXX42randomXXX")
        newline = newline.replace(iomp5,gomp)
        newline = newline.replace("XXX42randomXXX",iomp5)
        fout.write(newline)
    else:
        fout.write(line)

fin.close()
fout.close()

if gomp is None:
    raise RuntimeError("Could not find libgomp in build.ninja")
if iomp5 is None:
    raise RuntimeError("Could not find libiomp5 in build.ninja")

os.rename("build.ninja", "build.ninja.old")
os.rename("build.ninja.new", "build.ninja")
