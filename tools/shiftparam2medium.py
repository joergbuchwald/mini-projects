import sys
from lxml import etree as ET

class moveparametersXML(object):
    def __init__(self, **args):
        self.tree = None
        self.mediapath = "./media/medium"
        self.param_names = ["permeability", "porosity", "storage", "biot_coefficient"] # solid phase only
        if "ifile" in args:
            self.inputfile = args['ifile']
        else:
            self.inputfile = "default.prj"
        if "ofile" in args:
            self.outputfile = args["ofile"]
        else:
            self.outputfile = "default.prj"
        self.tempmem = {}

    def subsParam(self):
        if not self.tree:
            #parser = ET.XMLParser(remove_blank_text=True)
            #self.tree = ET.parse(self.inputfile, parser)
            self.tree = ET.parse(self.inputfile)
        root = self.tree.getroot()
        for medium in root.findall(self.mediapath):
            self.tempmem[medium.attrib["id"]] = {}
            for phases in medium:
                for phase in phases:
                    for propties in phase:
                        for propty in propties:
                            for param_name in self.param_names:
                                if propty.find("name").text == param_name:
                                    self.saveEntry(param_name, medium, propty)
                                    print("Medium:", medium.attrib["id"], "delete property: ", param_name)
                                    self.deleteEntry(propty)
            self.addEntries(medium)

    def saveEntry(self, name, medium, propty):
        self.tempmem[medium.attrib["id"]][name] = { "tag": [], "text": [] }
        for subtag in propty:
            self.tempmem[medium.attrib["id"]][name]["tag"].append(subtag.tag)
            self.tempmem[medium.attrib["id"]][name]["text"].append(subtag.text)
        #print(self.tempmem)

    def deleteEntry(self, propty):
        propty.getparent().remove(propty)

    def addEntries(self, mediumref):
        properties = None
        for entry in mediumref:
            if entry.tag == "properties":
                properties = entry
        if properties is None:
            properties = ET.SubElement(mediumref, "properties")
        for name in self.tempmem[mediumref.attrib["id"]]:
            print("Medium:", mediumref.attrib["id"], "add property: ", name)
            p = ET.SubElement(properties, "property")
            for i, subitem in enumerate(self.tempmem[mediumref.attrib["id"]][name]["tag"]):
                subelement = ET.SubElement(p, subitem)
                subelement.text = self.tempmem[mediumref.attrib["id"]][name]["text"][i]


    def writeOutput(self):
        if self.tree:
            self.tree.write(self.outputfile,
                            encoding="ISO-8859-1",
                            xml_declaration=True,
                            pretty_print=True)
            return True

if __name__ == "__main__":
    if len(sys.argv) > 2:
        replace = moveparametersXML(ifile=sys.argv[1], ofile=sys.argv[2])
    else:
        replace = moveparametersXML(ifile=sys.argv[1], ofile=sys.argv[1])
    replace.subsParam()
    replace.writeOutput()

