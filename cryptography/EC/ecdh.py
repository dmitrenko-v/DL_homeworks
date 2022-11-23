from funcs import BasePointGGet, ScalarMult

G = BasePointGGet()

def ecdh():
    # da and db are private keys
    da = 4
    db = 7

    # ha and hb are public keys
    ha = ScalarMult(G, da)
    hb = ScalarMult(G, db)

    # generating secrets
    S1 = ScalarMult(ha, db)
    S2 = ScalarMult(hb, da)

    # we need to round coordinates because there is a very little error
    S1.x = round(S1.x, 2)
    S1.y = round(S1.y, 2)
    S2.x = round(S2.x, 2)
    S2.y = round(S2.y, 2)

    return S1.x == S2.x and S1.y == S2.y


print(ecdh())