from lxml import etree as ET
import numpy as np
import pandas as pd

data= ET.parse(r'isotopes_work.xml')

root = ET.XML(ET.tostring(data.getroot()))
elements=[]
dataframes=[]
decays={'bo:alphaDecay': [],
        'bo:alphaDecayLikeliness': [],
        'bo:protonDecay': [],
        'bo:protonDecayLikeliness': [],
        'bo:2protonDecay': [],
        'bo:2protonDecayLikeliness': [],
        'bo:neutronDecay': [],
        'bo:neutronDecayLikeliness': [],
        'bo:2neutronDecay': [],
        'bo:2neutronDecayLikeliness': [],
        'bo:ecDecay': [],
        'bo:ecDecayLikeliness': [],
        'bo:2ecDecay': [],
        'bo:2ecDecay': [],
        'bo:betaminusDecay': [],
        'bo:betaminusDecayLikeliness': [],
        'bo:2betaminusDecay': [],
        'bo:2betaminusDecayLikeliness': [],
        'bo:betaplusDecay': [],
        'bo:betaplusDecayLikeliness': [],
        'bo:2betaplusDecay': [],
        'bo:2betaplusDecayLikeliness': [],
        'bo:betaminusneutronDecay': [],
        'bo:betaminusneutronDecayLikeliness': [],
        'bo:betaminus2neutronDecay': [],
        'bo:betaminus2neutronDecayLikeliness': [],
        'bo:betaminus3neutronDecay': [],
        'bo:betaminus3neutronDecayLikeliness': [],
        'bo:betaminus4neutronDecay': [],
        'bo:betaminus4neutronDecayLikeliness': [],
        'bo:betaminusalphaneutronDecay': [],
        'bo:betaminusalphaneutronDecayLikeliness': [],
        'bo:betaminusalphaDecay': [],
        'bo:betaminusalphaDecayLikeliness': [],
        'bo:betaminus2alphaDecay': [],
        'bo:betaminus2alphaDecayLikeliness': [],
        'bo:betaminus3alphaDecay': [],
        'bo:betaminus3alphaDecayLikeliness': [],
        'bo:betaplusprotonDecay': [],
        'bo:betaplusprotonDecayLikeliness': [],
        'bo:betaplus2protonDecay': [],
        'bo:betaplus2protonDecayLikeliness': [],
        'bo:betaplusalphaDecay': [],
        'bo:betaplusalphaDecayLikeliness': [],
        'bo:betaplus2alphaDecay': [],
        'bo:betaplus2alphaDecayLikeliness': [],
        'bo:betaplus3alphaDecay': [],
        'bo:betaplus3alphaDecayLikeliness': [],
        'bo:alphabetaminusDecay': [],
        'bo:alphabetaminusDecayLikeliness': [],
        'bo:protonalphaDecay': [],
        'bo:protonalphaDecayLikeliness': [],
        'bo:ecprotonDecay': [],
        'bo:ecprotonDecayLikeliness': [],
        'bo:ec2protonDecay': [],
        'bo:ec2protonDecayLikeliness': [],
        'bo:ec3protonDecay': [],
        'bo:ec3protonDecayLikeliness': [],
        'bo:ecalphaDecay': [],
        'bo:ecalphaDecayLikeliness': [],
        'bo:ecalphaprotonDecay': [],
        'bo:ecalphaprotonDecayLikeliness': []
        }
decay={'bo:alphaDecay': "",
        'bo:alphaDecayLikeliness': "",
        'bo:protonDecay': "",
        'bo:protonDecayLikeliness': "",
        'bo:2protonDecay': "",
        'bo:2protonDecayLikeliness': "",
        'bo:neutronDecay': "",
        'bo:neutronDecayLikeliness': "",
        'bo:2neutronDecay': "",
        'bo:2neutronDecayLikeliness': "",
        'bo:ecDecay': "",
        'bo:ecDecayLikeliness': "",
        'bo:2ecDecay': "",
        'bo:2ecDecay': "",
        'bo:betaminusDecay': "",
        'bo:betaminusDecayLikeliness': "",
        'bo:2betaminusDecay': "",
        'bo:2betaminusDecayLikeliness': "",
        'bo:betaplusDecay': "",
        'bo:betaplusDecayLikeliness': "",
        'bo:2betaplusDecay': "",
        'bo:2betaplusDecayLikeliness': "",
        'bo:betaminusneutronDecay': "",
        'bo:betaminusneutronDecayLikeliness': "",
        'bo:betaminus2neutronDecay': "",
        'bo:betaminus2neutronDecayLikeliness': "",
        'bo:betaminus3neutronDecay': "",
        'bo:betaminus3neutronDecayLikeliness': "",
        'bo:betaminus4neutronDecay': "",
        'bo:betaminus4neutronDecayLikeliness': "",
        'bo:betaminusalphaneutronDecay': "",
        'bo:betaminusalphaneutronDecayLikeliness': "",
        'bo:betaminusalphaDecay': "",
        'bo:betaminusalphaDecayLikeliness': "",
        'bo:betaminus2alphaDecay': "",
        'bo:betaminus2alphaDecayLikeliness': "",
        'bo:betaminus3alphaDecay': "",
        'bo:betaminus3alphaDecayLikeliness': "",
        'bo:betaplusprotonDecay': "",
        'bo:betaplusprotonDecayLikeliness': "",
        'bo:betaplus2protonDecay': "",
        'bo:betaplus2protonDecayLikeliness': "",
        'bo:betaplusalphaDecay': "",
        'bo:betaplusalphaDecayLikeliness': "",
        'bo:betaplus2alphaDecay': "",
        'bo:betaplus2alphaDecayLikeliness': "",
        'bo:betaplus3alphaDecay': "",
        'bo:betaplus3alphaDecayLikeliness': "",
        'bo:alphabetaminusDecay': "",
        'bo:alphabetaminusDecayLikeliness': "",
        'bo:protonalphaDecay': "",
        'bo:protonalphaDecayLikeliness': "",
        'bo:ecprotonDecay': "",
        'bo:ecprotonDecayLikeliness': "",
        'bo:ec2protonDecay': "",
        'bo:ec2protonDecayLikeliness': "",
        'bo:ec3protonDecay': "",
        'bo:ec3protonDecayLikeliness': "",
        'bo:ecalphaDecay': "",
        'bo:ecalphaDecayLikeliness': "",
        'bo:ecalphaprotonDecay': "",
        'bo:ecalphaprotonDecayLikeliness': ""
        }
for child in root.getchildren(): #elemente
    elements.append(child.attrib.values()[0])
    isotopes=[]
    numbers=[]
    masses=[]
    errors=[]
    halflifes=[]
    atomicnumbers=[]
    relativeabundances=[]
    spins=[]
    magneticmoments=[]
    for i in decays:
        decays[i]=[]
    for grandchild in child.getchildren(): #isotope
        isotopes.append(grandchild.attrib.values()[0])
        numbers.append(grandchild.attrib.values()[1])
        mass=""
        error=""
        halflife=""
        atomicnumber=""
        relativeabundance=""
        spin=""
        magneticmoment=""
        for i in decay:
            decay[i]=""
        for grandgrandchild in grandchild.getchildren():# scalars
            if grandgrandchild.attrib.values()[0]=="bo:exactMass":
                error=grandgrandchild.attrib.values()[1]
                mass=grandgrandchild.text
            elif grandgrandchild.attrib.values()[0]=="bo:halfLife":
                halflife=grandgrandchild.text
            elif grandgrandchild.attrib.values()[0]=="bo:atomicNumber":
                atomicnumber=grandgrandchild.text
            elif grandgrandchild.attrib.values()[0]=="bo:relativeAbundance":
                relativeabundance=grandgrandchild.text
            elif grandgrandchild.attrib.values()[0]=="bo:spin":
                spin=grandgrandchild.text
            elif grandgrandchild.attrib.values()[0]=="bo:magneticMoment":
                magneticmoment=grandgrandchild.text
            for i in decay:
                if grandgrandchild.attrib.values()[0]==i:
                    decay[i]=grandgrandchild.text
        for i in decays:
            decays[i].append(decay[i])
        masses.append(mass)
        errors.append(error)
        halflifes.append(halflife)
        atomicnumbers.append(atomicnumber)
        relativeabundances.append(relativeabundance)
        spins.append(spin)
        magneticmoments.append(magneticmoment)
#    print(decays)
    d={'isotop': isotopes, 'number': numbers, 'mass': masses, 'error': errors, 'spin': spins, 'magnetic_moment': magneticmoments, 'relative_abundance': relativeabundances, 'halflife': halflifes, 'atomicnumber': atomicnumbers}
    for i in decays:
        d[i]=decays[i]
#        print(len(d[i]),len(isotopes))
    dataframes.append(pd.DataFrame(data=d).set_index('number'))
data= ET.parse(r'isotopes_wikipedia.xml')
root = ET.XML(ET.tostring(data.getroot()))
elements=[]

for child in root.getchildren(): #elemente
    elements.append(child.attrib.values()[0])
    isotopes=[]
    numbers=[]
    masses=[]
    halflifes=[]
    atomicnumbers=[]
    relativeabundances=[]
    spins=[]
    magneticmoments=[]
    for i in decays:
        decays[i]=[]
    for grandchild in child.getchildren(): #isotope
        isotopes.append(grandchild.attrib.values()[0])
        numbers.append(grandchild.attrib.values()[1])
        mass=""
        halflife=""
        atomicnumber=""
        relativeabundance=""
        spin=""
        magneticmoment=""
        for i in decay:
            decay[i]=""
        for grandgrandchild in grandchild.getchildren():# scalars
            if grandgrandchild.attrib.values()[0]=="bo:exactMass":
                mass=grandgrandchild.text
            elif grandgrandchild.attrib.values()[0]=="bo:halfLife":
                try:
                    if dataframes[len(elements)-1].loc[numbers[-1],'halflife']=="":
                        if grandgrandchild.text != "":
                            dataframes[len(elements)-1].loc[numbers[-1],'halflife']=grandgrandchild.text
                except KeyError:
                    continue
            elif grandgrandchild.attrib.values()[0]=="bo:atomicNumber":
                atomicnumber=grandgrandchild.text
            elif grandgrandchild.attrib.values()[0]=="bo:relativeAbundance":
                relativeabundance=grandgrandchild.text
            elif grandgrandchild.attrib.values()[0]=="bo:spin":
                spin=grandgrandchild.text
                try:
                    dataframes[len(elements)-1].loc[numbers[-1],'spin']=spin
                except KeyError:
                    continue
            elif grandgrandchild.attrib.values()[0]=="bo:magneticMoment":
                magneticmoment=grandgrandchild.text
            for i in decay:
                if grandgrandchild.attrib.values()[0]==i:
                    try:
                        dataframes[len(elements)-1].loc[numbers[-1],i]=grandgrandchild.text
                    except KeyError:
                        continue


isotopelist=[]
isotope=[]
scalar=[]
root=ET.Element("cml")
for i,element in enumerate(elements):
    isotopelist.append(ET.SubElement(root,"isotopeList"))
    isotopelist[i].set("id",element)
#    print(i,  dataframes[i])
    isotope.append([])
    scalar.append([])
    for j in np.arange(0,len(dataframes[i])):
        #        print(dataframes[i]['mass'].iloc[j])
        try:
            isotope[i].append(ET.SubElement(isotopelist[i],"isotope"))
            scalar[i].append([])
            isotope[i][j].set("id",dataframes[i]['isotop'].iloc[j])
            isotope[i][j].set("number",dataframes[i].index.values[j])
            isotope[i][j].set("elementType",element)
        except:
            continue
        for k,column in enumerate(dataframes[i].columns):
            if column == "mass":
                if dataframes[i][column].iloc[j] != "":
                    scalar[i][j].append(ET.SubElement(isotope[i][j],"scalar"))
                    scalar[i][j][-1].set("dictRef","bo:exactMass")
                    scalar[i][j][-1].set("errorValue",dataframes[i]["error"].iloc[j])
                    scalar[i][j][-1].text = dataframes[i][column].iloc[j]
            if column == "spin":
                if dataframes[i][column].iloc[j] != "":
                    scalar[i][j].append(ET.SubElement(isotope[i][j],"scalar"))
                    scalar[i][j][-1].set("dictRef","bo:spin")
                    scalar[i][j][-1].text = dataframes[i][column].iloc[j]
            if column == "magnetic_moment":
                if dataframes[i][column].iloc[j] != "":
                    scalar[i][j].append(ET.SubElement(isotope[i][j],"scalar"))
                    scalar[i][j][-1].set("dictRef","bo:magneticMoment")
                    scalar[i][j][-1].text = dataframes[i][column].iloc[j]
            if column == "relative_abundance":
                if dataframes[i][column].iloc[j] != "":
                    scalar[i][j].append(ET.SubElement(isotope[i][j],"scalar"))
                    scalar[i][j][-1].set("dictRef","bo:relativeAbundance")
                    scalar[i][j][-1].text = dataframes[i][column].iloc[j]
            if column == "atomicnumber":
                if dataframes[i][column].iloc[j] != "":
                    scalar[i][j].append(ET.SubElement(isotope[i][j],"scalar"))
                    scalar[i][j][-1].set("dictRef","bo:atomicNumber")
                    scalar[i][j][-1].text = dataframes[i][column].iloc[j]
            if column == "halflife":
                if dataframes[i][column].iloc[j] != "":
                    scalar[i][j].append(ET.SubElement(isotope[i][j],"scalar"))
                    scalar[i][j][-1].set("dictRef","bo:halfLife")
                    scalar[i][j][-1].set("units","si:Units:s")
                    scalar[i][j][-1].text = dataframes[i][column].iloc[j]
            if "DecayLikeliness" in column:
                if dataframes[i][column].iloc[j] != "":
                    scalar[i][j].append(ET.SubElement(isotope[i][j],"scalar"))
                    scalar[i][j][-1].set("dictRef",dataframes[i].columns.tolist()[k-1])
                    scalar[i][j][-1].text = dataframes[i][dataframes[i].columns.tolist()[k-1]].iloc[j]
                    scalar[i][j].append(ET.SubElement(isotope[i][j],"scalar"))
                    scalar[i][j][-1].set("dictRef",column)
                    scalar[i][j][-1].set("units","bo:percentage")
                    scalar[i][j][-1].text = dataframes[i][column].iloc[j]
tree=ET.ElementTree(root)
tree.write("bla.xml",
    encoding="ISO-8859-1",
    xml_declaration=True,
    pretty_print=True)

#    if i==109:
#        print(dataframes[i]['bo:alphaDecay'])
