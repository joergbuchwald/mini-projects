# van Genuchten WRC curve
def inv_van_genuchten(p_cap, S_L_res, S_L_max, m, p_b):
    if p_cap <= 0:
        return S_L_max
    p = p_cap / p_b
    n = 1. / (1.-m)
    p_to_n = p**n

    S_eff = (p_to_n +1)**-m
    S = S_eff * S_L_max - S_eff*S_L_res + S_L_res
    if S < S_L_res:
        return S_L_res
    elif S > S_L_max:
        return S_L_max
    return S

def van_genuchten(S_L, S_L_res, S_L_max, m, p_b):
    S_eff = (S_L - S_L_res)/(S_L_max-S_L_res)
    return p_b*(S_eff**(-1/m)-1)**(1-m)
