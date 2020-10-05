#!/usr/bin/env python

import sys
from lxml import etree as ET


def transform(tree, xslt):
    transform = ET.XSLT(xslt)
    return transform(tree)


def xsltMoveSolidPropertyToMedium(property_name):
    return ET.XML('''\
    <xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:strip-space elements="*"/>

        <xsl:template match="node()|@*">
            <xsl:copy>
                <xsl:apply-templates select="node()|@*"/>
            </xsl:copy>
        </xsl:template>

        <!-- Remove this property. -->
        <xsl:template match="//phase[./type='Solid']/properties/property[./name='PROPERTY_NAME']"/>

        <!-- Copy it into /medium/properties if the latter exists. -->
        <xsl:template match="//medium/properties">
            <xsl:copy>
                <xsl:apply-templates select="@*" />
                <xsl:copy-of select="//phase[./type='Solid']/properties/property[./name='PROPERTY_NAME']"/>
                <xsl:apply-templates select="node()" />
            </xsl:copy>
        </xsl:template>

        <!-- Copy it into /medium/properties if the latter does _not_ exists. -->
        <xsl:template match="//medium[not(properties)]">
            <xsl:copy>
                <xsl:apply-templates select="@*" />
                <properties>
                    <xsl:copy-of select="//phase[./type='Solid']/properties/property[./name='PROPERTY_NAME']"/>
                </properties>
                <xsl:apply-templates select="node()" />
            </xsl:copy>
        </xsl:template>
    </xsl:stylesheet>'''.replace('PROPERTY_NAME', property_name))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Requires two arguments, input and output file names.")
        exit

    tree = ET.parse(sys.argv[1])
    encoding = tree.docinfo.encoding

    for property in [
            'permeability', 'porosity', 'storage', 'biot_coefficient'
    ]:
        tree = transform(tree, xsltMoveSolidPropertyToMedium(property))

    ET.indent(tree, space="    ")
    tree.write(sys.argv[2],
               encoding=encoding,
               xml_declaration=True,
               pretty_print=True)
