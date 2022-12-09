import os

fin = open("build.ninja", "rt")
fout = open("build.ninja.new", "wt")
gomp = None
gompi = None
iomp5 = None
iomp5i = None

fixit = True # True: iomp5 get linked before gomp, false: the other way round
ignore = True
once = False
for line in fin:
    if "Link the executable bin/ogs" in line:
        ignore = False
    if ignore is False:
        linesplit = line.split(" ")
        for i, entry in enumerate(linesplit):
            if ("-lgomp" in entry) or ("libgomp.so" in entry):
                if gomp is None:
                    gomp = entry
                    gompi = i
            elif ("-liomp5" in entry) or ("libiomp5.so" in entry):
                if iomp5 is None:
                    iomp5 = entry
                    iomp5i = i
    if (gomp is not None) and (iomp5 is not None) and (once is False):
        if fixit is True:
            a = gompi
            b = iomp5i
        else:
            a = iomp5i
            b = gompi
        if a < b:
            newline = line.replace(gomp,"XXX42randomXXX")
            newline = newline.replace(iomp5,gomp)
            newline = newline.replace("XXX42randomXXX",iomp5)
            fout.write(newline)
        else:
            fout.write(line)
        once = True
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
