# -*- coding: utf-8 -*-
"""API for storing EEG data into file"""

from uuid import uuid4
import sqlite3
import pathlib

__all__ = ["Data"]

# ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

CREATE_TABLES_SCRIPT = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS DUMP(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    TIMESTAMP TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    USERID INTEGER NOT NULL,
    RECORDNUMBER TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS BANDS(
    DUMP_ID INTEGER NOT NULL,
    IED_AF3_Theta REAL NOT NULL,
    IED_AF3_Alpha REAL NOT NULL,
    IED_AF3_LBeta REAL NOT NULL,
    IED_AF3_HBeta REAL NOT NULL,
    IED_AF3_Gamma REAL NOT NULL,
    IED_F7_Theta REAL NOT NULL,
    IED_F7_Alpha REAL NOT NULL,
    IED_F7_LBeta REAL NOT NULL,
    IED_F7_HBeta REAL NOT NULL,
    IED_F7_Gamma REAL NOT NULL,
    IED_F3_Theta REAL NOT NULL,
    IED_F3_Alpha REAL NOT NULL,
    IED_F3_LBeta REAL NOT NULL,
    IED_F3_HBeta REAL NOT NULL,
    IED_F3_Gamma REAL NOT NULL,
    IED_FC5_Theta REAL NOT NULL,
    IED_FC5_Alpha REAL NOT NULL,
    IED_FC5_LBeta REAL NOT NULL,
    IED_FC5_HBeta REAL NOT NULL,
    IED_FC5_Gamma REAL NOT NULL,
    IED_T7_Theta REAL NOT NULL,
    IED_T7_Alpha REAL NOT NULL,
    IED_T7_LBeta REAL NOT NULL,
    IED_T7_HBeta REAL NOT NULL,
    IED_T7_Gamma REAL NOT NULL,
    IED_P7_Theta REAL NOT NULL,
    IED_P7_Alpha REAL NOT NULL,
    IED_P7_LBeta REAL NOT NULL,
    IED_P7_HBeta REAL NOT NULL,
    IED_P7_Gamma REAL NOT NULL,
    IED_O1_Theta REAL NOT NULL,
    IED_O1_Alpha REAL NOT NULL,
    IED_O1_LBeta REAL NOT NULL,
    IED_O1_HBeta REAL NOT NULL,
    IED_O1_Gamma REAL NOT NULL,
    IED_O2_Theta REAL NOT NULL,
    IED_O2_Alpha REAL NOT NULL,
    IED_O2_LBeta REAL NOT NULL,
    IED_O2_HBeta REAL NOT NULL,
    IED_O2_Gamma REAL NOT NULL,
    IED_P8_Theta REAL NOT NULL,
    IED_P8_Alpha REAL NOT NULL,
    IED_P8_LBeta REAL NOT NULL,
    IED_P8_HBeta REAL NOT NULL,
    IED_P8_Gamma REAL NOT NULL,
    IED_T8_Theta REAL NOT NULL,
    IED_T8_Alpha REAL NOT NULL,
    IED_T8_LBeta REAL NOT NULL,
    IED_T8_HBeta REAL NOT NULL,
    IED_T8_Gamma REAL NOT NULL,
    IED_FC6_Theta REAL NOT NULL,
    IED_FC6_Alpha REAL NOT NULL,
    IED_FC6_LBeta REAL NOT NULL,
    IED_FC6_HBeta REAL NOT NULL,
    IED_FC6_Gamma REAL NOT NULL,
    IED_F4_Theta REAL NOT NULL,
    IED_F4_Alpha REAL NOT NULL,
    IED_F4_LBeta REAL NOT NULL,
    IED_F4_HBeta REAL NOT NULL,
    IED_F4_Gamma REAL NOT NULL,
    IED_F8_Theta REAL NOT NULL,
    IED_F8_Alpha REAL NOT NULL,
    IED_F8_LBeta REAL NOT NULL,
    IED_F8_HBeta REAL NOT NULL,
    IED_F8_Gamma REAL NOT NULL,
    IED_AF4_Theta REAL NOT NULL,
    IED_AF4_Alpha REAL NOT NULL,
    IED_AF4_LBeta REAL NOT NULL,
    IED_AF4_HBeta REAL NOT NULL,
    IED_AF4_Gamma REAL NOT NULL,
    FOREIGN KEY(DUMP_ID) REFERENCES DUMP(ID)
);
CREATE TABLE IF NOT EXISTS EQ(
    DUMP_ID INTEGER NOT NULL,
    IEE_CHAN_CMS INTEGER NOT NULL,
    IEE_CHAN_DRL INTEGER NOT NULL,
    IEE_CHAN_FP1 INTEGER NOT NULL,
    IEE_CHAN_AF3 INTEGER NOT NULL,
    IEE_CHAN_F7 INTEGER NOT NULL,
    IEE_CHAN_F3 INTEGER NOT NULL,
    IEE_CHAN_FC5 INTEGER NOT NULL,
    IEE_CHAN_T7 INTEGER NOT NULL,
    IEE_CHAN_P7 INTEGER NOT NULL,
    IEE_CHAN_O1 INTEGER NOT NULL,
    IEE_CHAN_O2 INTEGER NOT NULL,
    IEE_CHAN_P8 INTEGER NOT NULL,
    IEE_CHAN_T8 INTEGER NOT NULL,
    IEE_CHAN_FC6 INTEGER NOT NULL,
    IEE_CHAN_F4 INTEGER NOT NULL,
    IEE_CHAN_F8 INTEGER NOT NULL,
    IEE_CHAN_AF4 INTEGER NOT NULL,
    IEE_CHAN_FP2 INTEGER NOT NULL,
    FOREIGN KEY(DUMP_ID) REFERENCES DUMP(ID)
);
CREATE TABLE IF NOT EXISTS EMOSTATE(
    DUMP_ID INTEGER NOT NULL,
    Stress_Raw REAL NOT NULL,
    Stress_Min REAL NOT NULL,
    Stress_Max REAL NOT NULL,
    Stress_Scaled REAL NOT NULL,
    Engagement_Raw REAL NOT NULL,
    Engagement_Min REAL NOT NULL,
    Engagement_Max REAL NOT NULL,
    Engagement_Scaled REAL NOT NULL,
    Relaxation_Raw REAL NOT NULL,
    Relaxation_Min REAL NOT NULL,
    Relaxation_Max REAL NOT NULL,
    Relaxation_Scaled REAL NOT NULL,
    Exitement_Raw REAL NOT NULL,
    Exitement_Min REAL NOT NULL,
    Exitement_Max REAL NOT NULL,
    Exitement_Scaled REAL NOT NULL,
    Interest_Raw REAL NOT NULL,
    Interest_Min REAL NOT NULL,
    Interest_Max REAL NOT NULL,
    Interest_Scaled REAL NOT NULL,
    FOREIGN KEY(DUMP_ID) REFERENCES DUMP(ID)
);
CREATE TABLE IF NOT EXISTS FRAME(
    DUMP_ID INTEGER NOT NULL,
    COUNTER INTEGER NOT NULL,
    INTERPOLATED REAL NOT NULL,
    RAW_CQ INTEGER NOT NULL,
    AF3 REAL NOT NULL,
    F7 REAL NOT NULL,
    F3 REAL NOT NULL,
    FC5 REAL NOT NULL,
    T7 REAL NOT NULL,
    P7 REAL NOT NULL,
    O1 REAL NOT NULL,
    O2 REAL NOT NULL,
    P8 REAL NOT NULL,
    T8 REAL NOT NULL,
    FC6 REAL NOT NULL,
    F4 REAL NOT NULL,
    F8 REAL NOT NULL,
    AF4 REAL NOT NULL,
    GYROX INTEGER NOT NULL,
    GYROY INTEGER NOT NULL,
    TIMESTAMP REAL NOT NULL,
    MARKER_HARDWARE INTEGER NOT NULL,
    ES_TIMESTAMP REAL NOT NULL,
    FUNC_ID INTERGER NOT NULL,
    FUNC_VALUE REAL NOT NULL,
    MARKER INTERGER NOT NULL,
    SYNC_SIGNAL INTERGER NOT NULL,
    FOREIGN KEY(DUMP_ID) REFERENCES DUMP(ID)
);
"""

INSERT_DUMP = """
INSERT INTO DUMP (USERID,RECORDNUMBER) VALUES (?, ?)
"""


INSERT_BANDS = """
INSERT INTO BANDS (
    DUMP_ID,
    IED_AF3_Theta,
    IED_AF3_Alpha,
    IED_AF3_LBeta,
    IED_AF3_HBeta,
    IED_AF3_Gamma,
    IED_F7_Theta,
    IED_F7_Alpha,
    IED_F7_LBeta,
    IED_F7_HBeta,
    IED_F7_Gamma,
    IED_F3_Theta,
    IED_F3_Alpha,
    IED_F3_LBeta,
    IED_F3_HBeta,
    IED_F3_Gamma,
    IED_FC5_Theta,
    IED_FC5_Alpha,
    IED_FC5_LBeta,
    IED_FC5_HBeta,
    IED_FC5_Gamma,
    IED_T7_Theta,
    IED_T7_Alpha,
    IED_T7_LBeta,
    IED_T7_HBeta,
    IED_T7_Gamma,
    IED_P7_Theta,
    IED_P7_Alpha,
    IED_P7_LBeta,
    IED_P7_HBeta,
    IED_P7_Gamma,
    IED_O1_Theta,
    IED_O1_Alpha,
    IED_O1_LBeta,
    IED_O1_HBeta,
    IED_O1_Gamma,
    IED_O2_Theta,
    IED_O2_Alpha,
    IED_O2_LBeta,
    IED_O2_HBeta,
    IED_O2_Gamma,
    IED_P8_Theta,
    IED_P8_Alpha,
    IED_P8_LBeta,
    IED_P8_HBeta,
    IED_P8_Gamma,
    IED_T8_Theta,
    IED_T8_Alpha,
    IED_T8_LBeta,
    IED_T8_HBeta,
    IED_T8_Gamma,
    IED_FC6_Theta,
    IED_FC6_Alpha,
    IED_FC6_LBeta,
    IED_FC6_HBeta,
    IED_FC6_Gamma,
    IED_F4_Theta,
    IED_F4_Alpha,
    IED_F4_LBeta,
    IED_F4_HBeta,
    IED_F4_Gamma,
    IED_F8_Theta,
    IED_F8_Alpha,
    IED_F8_LBeta,
    IED_F8_HBeta,
    IED_F8_Gamma,
    IED_AF4_Theta,
    IED_AF4_Alpha,
    IED_AF4_LBeta,
    IED_AF4_HBeta,
    IED_AF4_Gamma)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

INSERT_EQ = """
INSERT INTO EQ (
    DUMP_ID,
    IEE_CHAN_CMS,
    IEE_CHAN_DRL,
    IEE_CHAN_FP1,
    IEE_CHAN_AF3,
    IEE_CHAN_F7,
    IEE_CHAN_F3,
    IEE_CHAN_FC5,
    IEE_CHAN_T7,
    IEE_CHAN_P7,
    IEE_CHAN_O1,
    IEE_CHAN_O2,
    IEE_CHAN_P8,
    IEE_CHAN_T8,
    IEE_CHAN_FC6,
    IEE_CHAN_F4,
    IEE_CHAN_F8,
    IEE_CHAN_AF4,
    IEE_CHAN_FP2
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

INSERT_EMOSTATE = """
INSERT INTO EMOSTATE (
    DUMP_ID,
    Stress_Raw,
    Stress_Min,
    Stress_Max,
    Stress_Scaled,
    Engagement_Raw,
    Engagement_Min,
    Engagement_Max,
    Engagement_Scaled,
    Relaxation_Raw,
    Relaxation_Min,
    Relaxation_Max,
    Relaxation_Scaled,
    Exitement_Raw,
    Exitement_Min,
    Exitement_Max,
    Exitement_Scaled,
    Interest_Raw,
    Interest_Min,
    Interest_Max,
    Interest_Scaled
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

INSERT_FRAME = """
INSERT INTO FRAME (
    DUMP_ID,
    COUNTER,
    INTERPOLATED,
    RAW_CQ,
    AF3,
    F7,
    F3,
    FC5,
    T7,
    P7,
    O1,
    O2,
    P8,
    T8,
    FC6,
    F4,
    F8,
    AF4,
    GYROX,
    GYROY,
    TIMESTAMP,
    MARKER_HARDWARE,
    ES_TIMESTAMP,
    FUNC_ID,
    FUNC_VALUE,
    MARKER,
    SYNC_SIGNAL
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


def extract_bands(data):
    band_names = [
        'AF3',
        'F7',
        'F3',
        'FC5',
        'T7',
        'P7',
        'O1',
        'O2',
        'P8',
        'T8',
        'FC6',
        'F4',
        'F8',
        'AF4']
    param_names = ['Theta', 'Alpha', 'LBeta', 'HBeta', 'Gamma']
    bands_dict = dict()
    for b in data['bands']:
        key, value = b.popitem()
        bands_dict[key] = value

    bands = list()
    for band in band_names:
        for param in param_names:
            bands.append(bands_dict['IED_' + band][param])
    return bands


def extract_eq(data):
    eq_names = [
        'IEE_CHAN_CMS',
        'IEE_CHAN_DRL',
        'IEE_CHAN_FP1',
        'IEE_CHAN_AF3',
        'IEE_CHAN_F7',
        'IEE_CHAN_F3',
        'IEE_CHAN_FC5',
        'IEE_CHAN_T7',
        'IEE_CHAN_P7',
        'IEE_CHAN_O1',
        'IEE_CHAN_O2',
        'IEE_CHAN_P8',
        'IEE_CHAN_T8',
        'IEE_CHAN_FC6',
        'IEE_CHAN_F4',
        'IEE_CHAN_F8',
        'IEE_CHAN_AF4',
        'IEE_CHAN_FP2']
    eq_values = list()
    for eq_name in eq_names:
        eq_values.append(data['EQ'][eq_name])
    return eq_values


def extract_emostate(data):
    emo_names = ["Stress", "Engagement", "Relaxation", "Exitement", "Interest"]
    params = ['Raw', 'Min', 'Max', 'Scaled']
    emostates = list()
    for emo in emo_names:
        for param in params:
            emostates.append(data["Emostate"][emo][param])
    return emostates


def extract_frames(data):
    fields = [
        "COUNTER",
        "INTERPOLATED",
        "RAW_CQ",
        "AF3",
        "F7",
        "F3",
        "FC5",
        "T7",
        "P7",
        "O1",
        "O2",
        "P8",
        "T8",
        "FC6",
        "F4",
        "F8",
        "AF4",
        "GYROX",
        "GYROY",
        "TIMESTAMP",
        "MARKER_HARDWARE",
        "ES_TIMESTAMP",
        "FUNC_ID",
        "FUNC_VALUE",
        "MARKER",
        "SYNC_SIGNAL"]
    frames = list()
    for frame in data["frames"]:
        values = list()
        for field in fields:
            values.append(frame[field])
        frames.append(values)
    return frames


class Data:
    """EEG data storage"""

    def __init__(self, path):
        base = pathlib.Path(path)
        base.mkdir(parents=True, exist_ok=True)
        self.filename = pathlib.Path(str(uuid4()) + ".db")
        self.filepath = base / self.filename
        self.db = sqlite3.connect(str(self.filepath), check_same_thread=False)
        self.db.executescript(CREATE_TABLES_SCRIPT)

    def append_json(self, data):
        bands = extract_bands(data)
        eq = extract_eq(data)
        emostate = None
        if "Emostate" in data:
            emostate = extract_emostate(data)
        frames = extract_frames(data)

        with self.db:
            c = self.db.cursor()
            c.execute(INSERT_DUMP, [data["userID"], data["RecordNumber"]])
            dump_id = c.lastrowid
            bands.insert(0, dump_id)
            eq.insert(0, dump_id)
            c.execute(INSERT_BANDS, bands)
            c.execute(INSERT_EQ, eq)
            if emostate:
                emostate.insert(0, dump_id)
                c.execute(INSERT_EMOSTATE, emostate)
            for frame in frames:
                frame.insert(0, dump_id)
            c.executemany(INSERT_FRAME, frames)
