import sys
import contextlib

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

TWISS_KEYS = {
    "ALFX": 0,
    "BETX": 1,
    "MUX": 2,
    "DX": 3,
    "DPX": 4,
    "ALFY": 5,
    "BETY": 6,
    "MUY": 7,
    "DY": 8,
    "DPY": 9,
    "X": 10,
    "PX": 11,
    "Y": 12,
    "PY": 13,
    "SUML": 14,
}


def parse_survey_rows(line3, line4):
    ffe3 = ff.FortranRecordReader("(4E16.9)")
    ffe4 = ff.FortranRecordReader("(3E16.9)")

    line3 = ffe3.read(line3)
    line4 = ffe3.read(line4)

    row = {}

    # Survey bits
    row["X"] = try_float(line3[0])
    row["Y"] = try_float(line3[1])
    row["Z"] = try_float(line3[2])
    row["SUML"] = try_float(line3[3])
    row["THETA"] = try_float(line4[0])
    row["PHI"] = try_float(line4[1])
    row["PSI"] = try_float(line4[2])

    return row


def parse_twiss_row(line1, line2, line3):
    ffr = ff.FortranRecordReader("(5E16.9)")
    line1 = ffr.read(line1)
    line2 = ffr.read(line2)
    line3 = ffr.read(line3)

    row = {}
    all_lines = line1 + line2 + line3
    for key, index in TWISS_KEYS.items():
        with contextlib.suppress(TypeError, ValueError):
            entry = float(all_lines[index])
        row[key] = entry

    return row


def try_float(arg):
    try:
        return float(arg)
    except (TypeError, ValueError):
        return arg


class MAD8FileFormatError(Exception):
    pass


def read(path):
    file_type = get_file_type(path)
    if file_type == "TWISS":
        return read_twiss(path)
    elif file_type == "SURVEY":
        return read_twiss(path)
    elif file_type == "CHROM":
        return read_chrom(path)
    else:
        raise MAD8FileFormatError(f"Unknown DATAVRSN: {file_type}")


def get_file_type(path):
    with open(path, "r") as f:
        header = parse_header(f.readline(), f.readline())
        return header["DATAVRSN"]


def read_twiss(twiss):
    assert get_file_type(twiss) == "TWISS"

    twiss_rows = []
    metadata = {}
    with open(twiss, "r") as f:
        d = parse_header(f.readline(), f.readline())
        metadata.update(d)
        nrecords = metadata["NPOS"]

        for _ in range(nrecords):
            row_common = parse_common_two_lines(f.readline(), f.readline())
            row_twiss = parse_twiss_row(f.readline(), f.readline(), f.readline())

            twiss_rows.append(row_common)
            twiss_rows[-1].update(row_twiss)
        metadata.update(parse_twiss_trailer(f.readline(), f.readline(), f.readline()))

    return make_df(twiss_rows, metadata, list(TWISS_KEYS))


def read_survey(survey):
    assert d["DATAVRSN"] == "SURVEY"
    survey_rows = []  # The data to be read in and converted to a DataFrame
    metadata = {}
    with open(survey, "r") as f:
        metadata.update(parse_header(f.readline(), f.readline()))

        nrecords = metadata["NPOS"]
        for _ in range(nrecords):
            row_common = parse_common_two_lines(f.readline(), f.readline())
            row_survey = parse_survey_row(line3, line4)
            survey_dictionary.append(row_common)
            survey_dictionary[-1].update(row_survey)

        metadata.update(parse_survey_trailer(f.readline(), f.readline()))

    return _make_df(survey_rows, metadata, SURVEY_COLUMNS)


def make_df(rows, metadata, extra_columns):
    index = list(range(len(rows)))
    df = pd.DataFrame(rows, index=index, columns=COMMON_COLUMNS + extra_columns)
    df.attrs.update(metadata)
    return df


def parse_common_two_lines(line1, line2):
    line1 = ff.FortranRecordReader("(A4,A16,F12.6,4E16.9,A19,E16.9)").read(line1)
    line2 = ff.FortranRecordReader("(5E16.9)").read(line2)

    keyword = line1[0].strip()
    name = line1[1].strip()

    row = {key: 0.0 for key in COMMON_COLUMNS + SURVEY_COLUMNS}
    row["KEYWORD"] = keyword
    row["NAME"] = name
    row["NOTE"] = ""

    if keyword == "":
        return row

    data = line1[2:6] + line2 + [line1[6], line1[7], line1[8]]
    keyword_columns = COMMON_COLUMN_POSITIONS[keyword]

    for key, index in keyword_columns.items():
        row[key] = data[index]

    return row


def parse_twiss_trailer(line1, line2, line3):
    line1 = ff.FortranRecordReader("3E16.9").read(line1)
    line2 = ff.FortranRecordReader("5E16.9").read(line2)
    line3 = ff.FortranRecordReader("5E16.9").read(line3)

    keys = [
        "DELTAP",
        "GAMTR",
        "C",
        "COSMUX",
        "QX",
        "QX'",
        "BXMAX",
        "DXMAX",
        "COSMUY",
        "QY",
        "QY'",
        "BYMAX",
        "DYMAX",
    ]

    trailer = {}
    all_lines = line1 + line2 + line3
    for i, key in enumerate(keys):
        trailer[key] = all_lines[i]
    return trailer


def parse_survey_trailer(line1, line2):
    ffe4 = ff.FortranRecordReader("(3E16.9)")
    metadata = {}

    metadata["X"] = trailer1[0]
    metadata["Y"] = trailer1[1]
    metadata["Z"] = trailer1[2]

    metadata["RMIN"] = trailer2[0]
    metadata["RMAX"] = trailer2[1]
    metadata["C"] = trailer2[2]

    return metadata


def parse_header(header_line_1, header_line_2):
    ffhr1 = ff.FortranRecordReader("(5A8,I8,L8,I8)")
    ffhr2 = ff.FortranRecordReader("(A80)")

    header_line_1 = ffhr1.read(header_line_1)
    header_line_2 = ffhr2.read(header_line_2)

    h1_names = [
        "PROGVRSN",
        "DATAVRSN",
        "DATE",
        "TIME",
        "JOBNAME",
        "SUPER",
        "SYMM",
        "NPOS",
    ]

    result = {name: data for name, data in zip(h1_names, header_line_1)}
    result["TITLE"] = header_line_2[0]

    # Strip any strings in the result
    for key, value in result.items():
        try:
            result[key] = value.strip()
        except AttributeError:
            pass

    return result


if __name__ == "__main__":
    df = read(sys.argv[1])
    from IPython import embed

    embed()
