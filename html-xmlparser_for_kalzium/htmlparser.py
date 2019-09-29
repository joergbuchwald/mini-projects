from html.parser import HTMLParser
from html.entities import name2codepoint

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.element=""
        self.isotope=""
        self.readinelement=False
        self.readinisotope=False
        self.decayenergy=""
        self.multipledecay=0
        self.columncount=0
        self.spin=""
        self.kind=""
        self.halflife=""
        self.masscolumn=7
        self.readindata=False
        self.readinunit=False
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag=="tr":
            self.columncount=0
        if tag=="td":
            self.columncount+=1
            self.readindata=True
            for i,attr in enumerate(attrs):
                if i==0:
                    if attr[0]=="align" and attr[1]=="right":
                        self.readinelement=True
        if tag=="sup":
            self.readinisotope=True

    def handle_endtag(self, tag):
        if tag=="td":        
            self.readinelement=False
            self.readindata=False
            self.readinunit=False
        if tag=="sup":
            self.readinisotope=False
    def handle_data(self, data):
        data=data.strip()
        if self.readinisotope==True:
            if data!=self.isotope:
                self.isotope=data.strip()
        if self.readinisotope==False and self.readinelement==True:
            if self.element!=data:
                self.element=data
                if self.element != "H":
                    print("</isotopeList>")
                string="<isotopeList id=\""+ self.element+ "\">"
                print(string)
                if self.element=="Tc" or self.element=="Po" or self.element=="Fr" or self.element=="Pm" or self.element=="Pa" or self.element=="Np" or self.element=="Am":
                    self.masscolumn=6
                if self.element=="Ru" or self.element=="Sm" or self.element=="Th" or self.element=="U" or self.element=="Pu":
                    self.masscolumn=7
            self.decayenergy=""
            self.kind=""
            string="\n<isotope id=\""+ self.element+ self.isotope+ "\" number=\""+  self.isotope + "\" elementType=\"" + self.element + "\">"
            print(string)
        if self.readindata==True and self.columncount==2:
            if not "<" in data: 
                if not ">" in data:
                    if not "stabil" in data:
                        if "·10" in data:
                            self.halflife=data.replace("·10","")
                        elif self.readinisotope==True:
                            self.readinunit=True
                            self.halflife=str(float(self.halflife.replace(",","."))*10**float(data.replace("−","-")))
                        elif self.readinunit==True:
                            if data.strip()=="s":
                                pass
                            if data.strip()=="ms":
                                self.halflife=str(float(self.halflife)/1000.0)
                            if data.strip()=="µs":
                                self.halflife=str(float(self.halflife)/1000.0e3)
                            if data.strip()=="ns":
                                self.halflife=str(float(self.halflife)/1000.0e6)
                            if data.strip()=="ps":
                                self.halflife=str(float(self.halflife)/1000.0e9)
                            if data.strip()=="min":
                                self.halflife=str(float(self.halflife)*60)
                            if data.strip()=="h":
                                self.halflife=str(float(self.halflife)*3600)
                            if data.strip()=="d":
                                self.halflife=str(float(self.halflife)*3600*24)
                            if data.strip()=="a":
                                self.halflife=str(float(self.halflife)*3600*24*365)
                            string="<scalar dictRef=\"bo:halfLife\" units=\"siUnits:s\">" + self.halflife + "</scalar>"
                            print(string)
                        else:
                            halflife=data.split()
                            halflife[0]=halflife[0].replace(",",".")
                            if len(halflife)==2:
                                if halflife[1].strip()=="s":
                                    pass
                                if halflife[1].strip()=="ms":
                                    halflife[0]=str(float(halflife[0])/1000.0)
                                if halflife[1].strip()=="µs":
                                    halflife[0]=str(float(halflife[0])/1000.0e3)
                                if halflife[1].strip()=="ns":
                                    halflife[0]=str(float(halflife[0])/1000.0e6)
                                if halflife[1].strip()=="ps":
                                    halflife[0]=str(float(halflife[0])/1000.0e9)
                                if halflife[1].strip()=="min":
                                    halflife[0]=str(float(halflife[0])*60)
                                if halflife[1].strip()=="h":
                                    halflife[0]=str(float(halflife[0])*3600)
                                if halflife[1].strip()=="d":
                                    halflife[0]=str(float(halflife[0])*3600*24)
                                if halflife[1].strip()=="a":
                                    halflife[0]=str(float(halflife[0])*3600*24*365)
                                string="<scalar dictRef=\"bo:halfLife\" units=\"siUnits:s\">" + halflife[0] + "</scalar>"
                                print(string)
                    else:
                        self.readindata=False
                else:
                    self.readindata=False
            else:
                self.readindata=False
        if self.readindata==True and self.columncount==3:
            self.decayenergy+=data
        if self.readindata==True and self.columncount==4:
            self.spin=data
            string="<scalar dictRef=\"bo:spin\">" + data.replace("−","-") +"</scalar>"
            print(string)
        if self.readindata==True and self.columncount==5:
# ugly, process decay energy of prev. column
            decayenergy=self.decayenergy.split(", ")
            self.multipledecay=len(decayenergy)
            decayenergy[0]=decayenergy[0].replace(",",".")
            self.decayenergy=decayenergy[0]
            self.kind+=data
        if self.readindata==True and self.columncount==self.masscolumn:
            kind=self.kind.split(", ")
            if len(kind) == 1 and not "=" in kind[0]:
                kind[0]=kind[0].replace(" ","")
                if not "=" in kind[0]:
                    if "p" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:protonDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:protonDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "2p" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:2protonDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:2protonDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "n" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:neutronDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:neutronDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "2n" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:2neutronDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:2neutronDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "ε" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:ecDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:ecDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "2ε" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:2ecDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:2ecDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β−" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaminusDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaminusDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "2β−" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:2betaminusDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:2betaminusDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β+" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaplusDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaplusDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "2β+" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:2betaplusDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:2betaplusDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "α" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:alphaDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:alphaDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β−n" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaminusneutronDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaminusneutronDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β−2n" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaminus2neutronDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaminus2neutronDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β−3n" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaminus3neutronDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaminus3neutronDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β−4n" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaminus4neutronDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaminus4neutronDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β−α" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaminusalphaDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaminusalphaDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β−2α" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaminus2alphaDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaminus2alphaDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β−3α" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaminus3alphaDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaminus3alphaDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β−αn" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaminusalphaneutronDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaminusalphaneutronDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β+p" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaplusprotonDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaplusprotonDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β+2p" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaplus2protonDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaplus2protonDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β+3p" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaplus3protonDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaplus3protonDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β+α" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaplusalphaDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaplusalphaDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "β+2α" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:betaplus2alphaDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:betaplus2alphaDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "αβ−" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:alphabetaminusDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:alphabetaminusDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "pα" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:protonalphaDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:protonalphaDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "εp" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:ecprotonDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:ecprotonDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "ε2p" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:ec2protonDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:ec2protonDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "ε3p" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:ec3protonDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:ec3protonDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "εα" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:ecalphaDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:ecalphaDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
                    if "εαp" == kind[0]:
                        if self.multipledecay==1:
                            string="<scalar dictRef=\"bo:ecalphaprotonDecay\">" + self.decayenergy + "</scalar>"
                            print(string)
                        string="<scalar dictRef=\"bo:ecalphaprotonDecayLikeliness\" units=\"bo:percentage\">100.0</scalar>"
                        print(string)
            else:
#                print(kind)
                for item in kind:
                    item=item.replace(" ","")
                    it=item.split("=")
                    if len(it)>1:
#                        print(it[0],it[1])
                        if not "?" in it[1]:
                            it[1]=it[1].replace(",",".")
                            if "p" == it[0]:
                                print("<scalar dictRef=\"bo:protonDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:protonDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                    "</scalar>")
                            if "2p" == it[0]:
                                print("<scalar dictRef=\"bo:2protonDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:2protonDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "n" == it[0]:
                                print("<scalar dictRef=\"bo:neutronDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:neutronDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "2n" == it[0]:
                                print("<scalar dictRef=\"bo:2neutronDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:2neutronDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "ε" == it[0]:
                                print("<scalar dictRef=\"bo:ecDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:ecDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "2ε" == it[0]:
                                print("<scalar dictRef=\"bo:2ecDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:2ecDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β−" == it[0]:
                                print("<scalar dictRef=\"bo:betaminusDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaminusDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "2β−" == it[0]:
                                print("<scalar dictRef=\"bo:2betaminusDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:2betaminusDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β+" == it[0]:
                                print("<scalar dictRef=\"bo:betaplusDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaplusDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "2β+" == it[0]:
                                print("<scalar dictRef=\"bo:2betaplusDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:2betaplusDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                         "</scalar>")
                            if "α" == it[0]:
                                print("<scalar dictRef=\"bo:alphaDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:2betaplusDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β−n" == it[0]:
                                print("<scalar dictRef=\"bo:betaminusneutronDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaminusneutronDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β−2n" == it[0]:
                                print("<scalar dictRef=\"bo:betaminus2neutronDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaminus2neutronDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                    "</scalar>")
                            if "β−3n" == it[0]:
                                print("<scalar dictRef=\"bo:betaminus3neutronDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaminus3neutronDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                     "</scalar>")
                            if "β−4n" == it[0]:
                                print("<scalar dictRef=\"bo:betaminus4neutronDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaminus4neutronDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β−αn" == it[0]:
                                print("<scalar dictRef=\"bo:betaminusalphaneutronDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaminusalphaneutronDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β−α" == it[0]:
                                print("<scalar dictRef=\"bo:betaminusalphaDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaminusalphaDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β−2α" == it[0]:
                                print("<scalar dictRef=\"bo:betaminus2alphaDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaminus2alphaDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β−3α" == it[0]:
                                print("<scalar dictRef=\"bo:betaminus3alphaDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaminus3alphaDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β+p" == it[0]:
                                print("<scalar dictRef=\"bo:betaplusprotonDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaplusprotonDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β+2p" == it[0]:
                                print("<scalar dictRef=\"bo:betaplus2protonDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaplus2protonDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β+α" == it[0]:
                                print("<scalar dictRef=\"bo:betaplusalphaDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaplusalphaDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β+2α" == it[0]:
                                print("<scalar dictRef=\"bo:betaplus2alphaDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaplus2alphaDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "β+3α" == it[0]:
                                print("<scalar dictRef=\"bo:betaplus3alphaDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:betaplus3alphaDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "αβ−" == it[0]:
                                print("<scalar dictRef=\"bo:alphabetaminusDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:alphabetaminusDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "pα" == it[0]:
                                print("<scalar dictRef=\"bo:protonalphaDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:protonalphaDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "εp" == it[0]:
                                print("<scalar dictRef=\"bo:ecprotonDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:ecprotonDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "ε2p" == it[0]:
                                print("<scalar dictRef=\"bo:ec2protonDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:ec2protonDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "ε3p" == it[0]:
                                print("<scalar dictRef=\"bo:ec3protonDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:ec3protonDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "εα" == it[0]:
                                print("<scalar dictRef=\"bo:ecalphaDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:ecalphaDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
                            if "εαp" == it[0]:
                                print("<scalar dictRef=\"bo:ecalphaprotonDecay\"></scalar>")
                                print("<scalar dictRef=\"bo:ecalphaprotonDecayLikeliness\" units=\"bo:percentage\">" + it[1] +
                                        "</scalar>")
            print("</isotope>")
if __name__=='__main__':
    file="5_Periode.html"
    datei=open(file,"r")
    html=datei.read()
    parser = MyHTMLParser()
    parser.feed(html)

