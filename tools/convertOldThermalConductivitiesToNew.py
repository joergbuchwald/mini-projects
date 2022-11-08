import sys
from ogs6py.ogs import OGS

"""
Old:

                <property>
                    <name>thermal_conductivity</name>
                    <type>SoilThermalConductivitySomerton</type>
                    <dry_thermal_conductivity>k_T_dry</dry_thermal_conductivity>
                    <wet_thermal_conductivity>k_T_wet</wet_thermal_conductivity>
                </property>

OR:
                <property>
                    <name>thermal_conductivity</name>
                    <type>SaturationDependentThermalConductivity</type>
                    <wet>0.6</wet>
                    <dry>0.2</dry>
                </property>
New:
                <property>
                    <name>thermal_conductivity</name>
                    <type>SaturationWeightedThermalConductivity</type>
                    <mean_type>arithmetic_squareroot</mean_type>
                    <dry_thermal_conductivity>k_T_dry</dry_thermal_conductivity>
                    <wet_thermal_conductivity>k_T_wet</wet_thermal_conductivity>
                </property>
"""

def main(filename):
    f = OGS(INPUT_FILE=filename, PROJECT_FILE=filename)
    # convert SoilThermalConductivitySomerton
    f.add_element(parent_xpath="./media/medium/properties/property[type='SoilThermalConductivitySomerton']",
                  tag="mean_type", text="arithmetic_squareroot")
    f.replace_text("SaturationWeightedThermalConductivity",
                   xpath="./media/medium/properties/property[type='SoilThermalConductivitySomerton']/type")
    # convert SaturationDependentThermalConductivity
    f.add_element(parent_xpath="./media/medium/properties/property[type='SaturationDependentThermalConductivity']",
                  tag="mean_type", text="arithmetic_linear")
    items = f.tree.findall("./media/medium/properties/property[type='SaturationDependentThermalConductivity']")
    for i, item in enumerate(items):
        children = item.getchildren()
        for child in children:
            if child.tag == "wet":
                wet_value = child.text
                f.add_block("parameter", parent_xpath="./parameters",
                        taglist=["name","type", "value"],
                        textlist=[f"lambda_wet{i}","Constant", wet_value])
                child.tag = "wet_thermal_conductivity"
                child.text = f"lambda_wet{i}"
            elif child.tag == "dry":
                dry_value = child.text
                f.add_block("parameter", parent_xpath="./parameters", taglist=["name","type", "value"],
                        textlist=[f"lambda_dry{i}","Constant", dry_value])
                child.tag = "dry_thermal_conductivity"
                child.text = f"lambda_dry{i}"
    f.replace_text("SaturationWeightedThermalConductivity",
                   xpath="./media/medium/properties/property[type='SaturationDependentThermalConductivity']/type")
    f.write_input()

if __name__ == '__main__':
    main(sys.argv[1])
