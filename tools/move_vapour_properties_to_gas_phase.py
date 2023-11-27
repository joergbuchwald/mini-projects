import sys
from ogs6py.ogs import OGS

"""
Old:
                <phase>
                     <type>AqueousLiquid</type>
                     <properties>
                         <property>
                             <name>vapour_density</name>
                             <type>WaterVapourDensity</type>
                         </property>
                         <property>
                             <name>vapour_diffusion</name>
                             <type>VapourDiffusionFEBEX</type>
                             <tortuosity>0.8</tortuosity>
                         </property>
                         <property>
                             <name>latent_heat</name>
                             <type>LinearWaterVapourLatentHeat</type>
                         </property>
                         <property>
                             <name>thermal_diffusion_enhancement_factor
                             </name>
                             <type>Constant</type>
                             <value>1.0</value>
                         </property>
                     </properties>
                 </phase>

New:
                 <phase>
                     <type>Gas</type>
                     <properties>
                         <property>
                             <name>specific_heat_capacity</name>
                             <type>Constant</type>
                             <value>0</value>
                         </property>
                         <property>
                             <name>density</name>
                             <type>WaterVapourDensity</type>
                         </property>
                         <property>
                             <name>diffusion</name>
                             <type>VapourDiffusionFEBEX</type>
                             <tortuosity>0.8</tortuosity>
                         </property>
                         <property>
                             <name>latent_heat</name>
                             <type>LinearWaterVapourLatentHeat</type>
                         </property>
                         <property>
                             <name>thermal_diffusion_enhancement_factor</name>
                             <type>Constant</type>
                             <value>1.0</value>
                        </property>
"""

def main(filename1, filename2):
    f = OGS(INPUT_FILE=filename1, PROJECT_FILE=filename2)
    f.write_input()
    f = OGS(INPUT_FILE=filename2, PROJECT_FILE=filename2)
    # add new phase
    media = f.tree.findall("./media/medium")
    if len(media) > 1:
        media_ids = [medium.attrib["id"] for medium in media]
    else:
        media_ids ["0"]
    for medium_id in media_ids:
        if len(media) > 1:
            phases_xpath = f"./media/medium[@id='{medium_id}']/phases"
        else:
            phases_xpath = f"./media/medium/phases"
        gas_phase = f.tree.find(phases_xpath+"/phase[type='Gas']")
        if gas_phase is None:
            f.add_block("phase", parent_xpath=phases_xpath, taglist=["type", "properties"],
                            textlist=["Gas", None])
            f.add_block("property", parent_xpath=phases_xpath+"/phase[type='Gas']/properties",
                        taglist=["name", "type", "value"], textlist=["specific_heat_capacity", "Constant", "0"])
        properties = {"vapour_density": "density",
                          "vapour_diffusion": "diffusion",
                          "latent_heat": "latent_heat",
                          "thermal_diffusion_enhancement_factor": "thermal_diffusion_enhancement_factor"}
        elems_tobedeleted = []
        for old_prop, new_prop in properties.items():
            print(old_prop)
            xpath = f"{phases_xpath}/phase[type='AqueousLiquid']/properties/property"
            tmp1 = f.tree.findall(xpath)
            for t1 in tmp1:
                tmp = t1.getchildren()
                for t in tmp:
                    if t.tag == "name":
                        print(t.text)
                        if old_prop in t.text:
                            print(old_prop)
                            found_elems = tmp
                            elems_tobedeleted.append(tmp[0].getparent())
            #found_elems = f.tree.find(xpath)
            if found_elems is None:
                print(f"{old_prop} not found in {xpath}")
            taglist = ["name"]
            textlist = [new_prop]
            for elem in found_elems:
                if not elem.tag == "name":
                    taglist.append(elem.tag)
                    textlist.append(elem.text)
            f.add_block("property", parent_xpath=phases_xpath+"/phase[type='Gas']/properties",
                        taglist=taglist, textlist=textlist)
        for elem in elems_tobedeleted:
            elem.getparent().remove(elem)


    f.write_input()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
