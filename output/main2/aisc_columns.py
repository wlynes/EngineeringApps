aisc_cols = {
    # These are the ACTUAL excel column indices (index = 1)
    'edition':1,
    'type':3,
    'shape':4,
    'Ag':11,
    'd':12,
    'tw':13,
    'bf':15,
    'tf':16,
    'bf_2tf':21,
    'h_tw':22,
    'Ix':26,
    'Zx':27,
    'Sx':28,
    'rx':29,
    'Iy':32,
    'Zy':33,
    'Sy':34,
    'ry':35,
    'J':55,
    'Cw':85,
    'b_t':107,
    'D_t':102,
    'h_tdes':100,
    'b_tdes':101,
    'e0':41
}

aisc_cols_csv = {}
for k, v in aisc_cols.items():
    vcsv = v-1
    aisc_cols_csv.update({k:vcsv})

