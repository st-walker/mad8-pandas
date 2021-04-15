import sys

import pandas as pd
import fortranformat as ff

COMMON_COLUMNS = [
    "KEYWORD",
    "NAME",
    "ANGLE",
    "APER",
    "E",
    "E1",
    "E2",
    "EFIELD",
    "FREQ",
    "H1",
    "H2",
    "HKICK",
    "K0L",
    "K1",
    "K1L",
    "K2",
    "K2L",
    "K3",
    "K3L",
    "KS",
    "L",
    "LAG",
    "NOTE",
    "T0",
    "T1",
    "T2",
    "T3",
    "TILT",
    "VKICK",
    "VOLT",
    "XSIZE",
    "YSIZE",
]

SURVEY_COLUMNS = ["X", "Y", "Z", "SUML", "THETA", "PHI", "PSI"]


COMMON_COLUMN_POSITIONS = {
    "DRIF": {"L": 0, "APER": 9, "NOTE": 10, "E": 11},
    "RBEN": {
        "L": 0,
        "ANGLE": 1,
        "K1": 2,
        "K2": 3,
        "TILT": 4,
        "E1": 5,
        "E2": 6,
        "H1": 7,
        "H2": 8,
        "APER": 9,
        "NOTE": 10,
        "E": 11,
    },
    "SBEN": {
        "L": 0,
        "ANGLE": 1,
        "K1": 2,
        "K2": 3,
        "TILT": 4,
        "E1": 5,
        "E2": 6,
        "H1": 7,
        "H2": 8,
        "APER": 9,
        "NOTE": 10,
        "E": 11,
    },
    "QUAD": {"L": 0, "K1": 2, "TILT": 4, "APER": 9, "NOTE": 10, "E": 11},
    "SEXT": {"L": 0, "K2": 3, "TILT": 4, "APER": 9, "NOTE": 10, "E": 11},
    "OCTU": {"L": 0, "TILT": 4, "K3": 5, "APER": 9, "NOTE": 10, "E": 11},
    "MULT": {
        "K0L": 1,
        "K1L": 2,
        "K2L": 3,
        "T0": 4,
        "K3L": 5,
        "T1": 6,
        "T2": 7,
        "T3": 8,
        "APER": 9,
        "NOTE": 10,
        "E": 11,
    },
    "SOLE": {"L": 0, "KS": 5, "APER": 9, "NOTE": 10, "E": 11},
    "RFCAVITY": {
        "L": 0,
        "FREQ": 5,
        "VOLT": 6,
        "LAG": 7,
        "APER": 9,
        "NOTE": 10,
        "E": 11,
    },
    "ELSEPARATOR": {"L": 0, "TILT": 4, "EFIELD": 5, "APER": 9, "NOTE": 10, "E": 11},
    "KICK": {"L": 0, "HKICK": 4, "VKICK": 5, "APER": 9, "NOTE": 10, "E": 11},
    "HKIC": {"L": 0, "HKICK": 4, "APER": 9, "NOTE": 10, "E": 11},
    "VKIC": {"L": 0, "VKICK": 5, "APER": 9, "NOTE": 10, "E": 11},
    "SROT": {"L": 0, "ANGLE": 5, "APER": 9, "NOTE": 10, "E": 11},
    "YROT": {"L": 0, "ANGLE": 5, "APER": 9, "NOTE": 10, "E": 11},
    "MONI": {"L": 0, "APER": 9, "NOTE": 10, "E": 11},
    "HMONITOR": {"L": 0, "APER": 9, "NOTE": 10, "E": 11},
    "VMONITOR": {"L": 0, "APER": 9, "NOTE": 10, "E": 11},
    "MARK": {"L": 0, "APER": 9, "NOTE": 10, "E": 11},
    "ECOL": {"L": 0, "XSIZE": 4, "YSIZE": 5, "APER": 9, "NOTE": 10, "E": 11},
    "RCOL": {"L": 0, "XSIZE": 4, "YSIZE": 5, "APER": 9, "NOTE": 10, "E": 11},
    "MARK": {"L": 0, "NOTE": 10, "E": 11},
    "INST": {"L": 0, "NOTE": 10, "E": 11},
    "WIRE": {"L": 0, "NOTE": 10, "E": 11},
    "IMON": {"L": 0, "NOTE": 10, "E": 11},
    "PROF": {"L": 0, "NOTE": 10, "E": 11},
    "BLMO": {"L": 0, "NOTE": 10, "E": 11},
    "LCAV": {"L": 0, "FREQ": 5, "VOLT": 6, "LAG": 7, "APER": 9, "NOTE": 10, "E": 11},
    "MATR": {"L": 0, "APER": 9, "E": 11},
}

def fill_survey_row(line1, line2, line3, line4):
    keyword = line1[0].strip()
    name = line1[1].strip()

    row = {key: 0. for key in COMMON_COLUMNS + SURVEY_COLUMNS}
    row["KEYWORD"] = keyword
    row["NAME"] = name
    row["NOTE"] = ""

    if keyword == "":
        return row

    data = line1[2:6]+line2+[line1[6],line1[7],line1[8]]
    keyword_columns = COMMON_COLUMN_POSITIONS[keyword]

    for key, index in keyword_columns.items():
        row[key] = data[index]

    # Survey bits
    row["X"] = try_float(line3[0])
    row["Y"] = try_float(line3[1])
    row["Z"] = try_float(line3[2])
    row["SUML"] = try_float(line3[3])
    row["THETA"] = try_float(line4[0])
    row["PHI"] = try_float(line4[1])
    row["PSI"] = try_float(line4[2])

    return row

def try_float(arg):
    try:
        return float(arg)
    except (TypeError, ValueError):
        return args

class MAD8FileFormatError(Exception): pass
    
def read_survey(survey):
    df = pd.DataFrame(columns=(COMMON_COLUMNS + SURVEY_COLUMNS))

    with open(survey, "r") as f:
        d = parse_header(f.readline(), f.readline())

        df.attrs.update(d)

        nrecords = df.attrs["npos"]

        if d["datatype"] != "SURVEY":
            raise MAD8FileFormatError(f"Not a SURVEY file: {f.name}")

        ffe1 = ff.FortranRecordReader("(A4,A16,F12.6,4E16.9,A19,E16.9)")
        ffe2 = ff.FortranRecordReader("(5E16.9)")
        ffe3 = ff.FortranRecordReader("(4E16.9)")
        ffe4 = ff.FortranRecordReader("(3E16.9)")

        for i in range(nrecords):
            line1 = ffe1.read(f.readline())
            line2 = ffe2.read(f.readline())
            line3 = ffe3.read(f.readline())
            line4 = ffe4.read(f.readline())

            row = fill_survey_row(line1, line2, line3, line4)

            df = df.append(row, ignore_index=True)

        trailer1 = ffe4.read(f.readline())
        trailer2 = ffe4.read(f.readline())

        df.attrs["x_centre"] = trailer1[0]
        df.attrs["y_centre"] = trailer1[1]
        df.attrs["z_centre"] = trailer1[2]

        df.attrs["rmin"] = trailer2[0]
        df.attrs["rmax"] = trailer2[1]
        df.attrs["circumference"] = trailer2[2]

    return df


def parse_header(header_line_1, header_line_2):
    ffhr1 = ff.FortranRecordReader("(5A8,I8,L8,I8)")
    ffhr2 = ff.FortranRecordReader("(A80)")

    header_line_1 = ffhr1.read(header_line_1)
    header_line_2 = ffhr2.read(header_line_2)

    h1_names = [
        "version",
        "datatype",
        "date",
        "time",
        "jobname",
        "super",
        "symm",
        "npos",
    ]

    result = {name: data for name, data in zip(h1_names, header_line_1)}
    result["title"] = header_line_2[0]

    # Strip any strings in the result
    for key, value in result.items():
        try:
            result[key] = value.strip()
        except AttributeError:
            pass

    return result


if __name__ == "__main__":
    df = read(sys.argv[1])
    from IPython import embed; embed()

