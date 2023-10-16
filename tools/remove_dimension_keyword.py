from pathlib import Path
from ogs6py.ogs import OGS


def main(filename):
    try:
        f = OGS(INPUT_FILE=filename, PROJECT_FILE=filename)
        if f.tree.find("./processes/process/dimension") is not None:
            print(f"Remove dimension keyword in: {filename}")
            f.remove_element("./processes/process/dimension")
            f.write_input()
    except:
        print(f"Could not read project file: {filename}")

if __name__ == '__main__':
    for path in Path('.').rglob('*.prj'):
        main(path)

