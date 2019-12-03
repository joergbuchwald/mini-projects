decays={'bo:alphaDecay': False,
        'bo:alphaDecayLikeliness': False,
        'bo:protonDecay': False,
        'bo:protonDecayLikeliness': False,
        'bo:2protonDecay': False,
        'bo:2protonDecayLikeliness': False,
        'bo:neutronDecay': False,
        'bo:neutronDecayLikeliness': False,
        'bo:2neutronDecay': False,
        'bo:2neutronDecayLikeliness': False,
        'bo:ecDecay': False,
        'bo:ecDecayLikeliness': False,
        'bo:2ecDecay': False,
        'bo:2ecDecay': False,
        'bo:betaminusDecay': False,
        'bo:betaminusDecayLikeliness': False,
        'bo:betaminusfissionDecay': False,
        'bo:betaminusfissionDecayLikeliness': False,
        'bo:2betaminusDecay': False,
        'bo:2betaminusDecayLikeliness': False,
        'bo:betaplusDecay': False,
        'bo:betaplusDecayLikeliness': False,
        'bo:2betaplusDecay': False,
        'bo:2betaplusDecayLikeliness': False,
        'bo:betaminusneutronDecay': False,
        'bo:betaminusneutronDecayLikeliness': False,
        'bo:betaminus2neutronDecay': False,
        'bo:betaminus2neutronDecayLikeliness': False,
        'bo:betaminus3neutronDecay': False,
        'bo:betaminus3neutronDecayLikeliness': False,
        'bo:betaminus4neutronDecay': False,
        'bo:betaminus4neutronDecayLikeliness': False,
        'bo:betaminusalphaneutronDecay': False,
        'bo:betaminusalphaneutronDecayLikeliness': False,
        'bo:betaminusalphaDecay': False,
        'bo:betaminusalphaDecayLikeliness': False,
        'bo:betaminus2alphaDecay': False,
        'bo:betaminus2alphaDecayLikeliness': False,
        'bo:betaminus3alphaDecay': False,
        'bo:betaminus3alphaDecayLikeliness': False,
        'bo:betaplusprotonDecay': False,
        'bo:betaplusprotonDecayLikeliness': False,
        'bo:betaplus2protonDecay': False,
        'bo:betaplus2protonDecayLikeliness': False,
        'bo:betaplusalphaDecay': False,
        'bo:betaplusalphaDecayLikeliness': False,
        'bo:betaplus2alphaDecay': False,
        'bo:betaplus2alphaDecayLikeliness': False,
        'bo:betaplus3alphaDecay': False,
        'bo:betaplus3alphaDecayLikeliness': False,
        'bo:alphabetaminusDecay': False,
        'bo:alphabetaminusDecayLikeliness': False,
        'bo:protonalphaDecay': False,
        'bo:protonalphaDecayLikeliness': False,
        'bo:ecprotonDecay': False,
        'bo:ecprotonDecayLikeliness': False,
        'bo:ec2protonDecay': False,
        'bo:ec2protonDecayLikeliness': False,
        'bo:ec3protonDecay': False,
        'bo:ec3protonDecayLikeliness': False,
        'bo:ecalphaDecay': False,
        'bo:ecalphaDecayLikeliness': False,
        'bo:ecalphaprotonDecay': False,
        'bo:ecalphaprotonDecayLikeliness': False
        }
for i in decays:
    if "Likeliness" not in i:
        print("        if ((isotope)->"+ i[3:].replace("2","two").replace("3","three").replace("4","four").replace("Decay","likeliness()")+" > 0.0) {")
        print("            if ((isotope)->"+i[3:].replace("2","two").replace("3","three").replace("4","four").lower()+"() > 0.0) {")
        print("                html.append(i18n(\"%1 MeV\", (isotope)->"+i[3:].replace("2","two").replace("3","three").replace("4","four").lower()+"()));")
        print("            }")
        print("            html.append(i18n());")
        print("            if ((isotope)->"+i[3:].replace("2","two").replace("3","three").replace("4","four").replace("Decay","likeliness()") + " < 100.0) {")
        print("                html.append(i18n(\"(%1%)\", (isotope)->"+i[3:].replace("2","two").replace("3","three").replace("4","four").replace("Decay","likeliness()") +"));")
        print("            }")
        decays[i]=True
        print("            if (")
        for j,decay in enumerate(decays):
            if "Likeliness" not in decay:
                if j < (len(decays)-1):
                    if decays[decay] is False:
                        print("                (isotope)->"+decay[3:].replace("2","two").replace("3","three").replace("4","four").replace("Decay","likeliness()") + "  > 0.0 || ")
                if decay=="bo:ecalphaprotonDecay":
                    if decays[decay] is False:
                        print("                (isotope)->"+decay[3:].replace("2","two").replace("3","three").replace("4","four").replace("Decay","likeliness()") + "  > 0.0 ) {")
        print("                html.append(i18n(\", \"));")
        print("            }")
        print("        }")

