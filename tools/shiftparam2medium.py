#!/usr/bin/env python

import sys
from lxml import etree as ET


def transform(tree, xslt):
    write(ET.ElementTree(xslt), '/tmp/xslt.xml')
    transform = ET.XSLT(ET.ElementTree(xslt))
    return transform(tree)


xsltHeader = '''\
    <xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:strip-space elements="*"/>
    '''

xsltFooter = '</xsl:stylesheet>'

xsltCopyAll = '''\
        <xsl:template match="node()|@*">
            <xsl:copy>
                <xsl:apply-templates select="node()|@*"/>
            </xsl:copy>
        </xsl:template>
    '''


def xsltRemove(match):
    return '    <xsl:template match="' + match + '"/>\n'


def xsltCopy(match, select):
    return '''\
        <xsl:template match="''' + match + '''">
            <xsl:copy>
                <xsl:apply-templates select="@*" />
                <xsl:copy-of select="''' + select + '''"/>
                <xsl:apply-templates select="node()" />
            </xsl:copy>
        </xsl:template>
    '''


def xsltMove(match, select):
    return xsltRemove(select) + xsltCopy(match, select)


def xsltCopyCreateSubtree(match, element, select):
    return '''\
        <xsl:template match="''' + match + '[not(' + element + ''')]">
            <xsl:copy>
                <xsl:apply-templates select="@*" />
                <''' + element + '''>
                    <xsl:copy-of select="''' + select + '''"/>
                </''' + element + '''>
                <xsl:apply-templates select="node()" />
            </xsl:copy>
        </xsl:template>
    '''


def write(tree, filename):
    ET.indent(tree, space="    ")
    tree.write(sys.argv[2],
               encoding=encoding,
               xml_declaration=True,
               pretty_print=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Requires two arguments, input and output file names.")
        exit

    tree = ET.parse(sys.argv[1])
    encoding = tree.docinfo.encoding

    xslt = xsltHeader + xsltCopyAll

    xslt += xsltMove(
        "//phase[./type='AqueousLiquid']/properties",
        "//medium/properties/property[./name='relative_permeability']")

    properties = ['permeability', 'porosity', 'storage', 'biot_coefficient']
    property_selector = ' or '.join(["./name='" + p + "'" for p in properties])

    xslt += xsltMove(
        "//medium/properties", "//phase[./type='Solid']/properties/property[" +
        property_selector + "]")
    xslt += xsltCopyCreateSubtree(
        "//medium", "properties",
        "//phase[./type='Solid']/properties/property[" + property_selector +
        "]")

    xslt += xsltFooter

    write(transform(tree, ET.XML(xslt)), sys.argv[2])
