import sys
import xml.etree.ElementTree as ET

# '1230', '1231','1240','1241' : somehow related to start and end of therapy session

skip_events = ['1230', '1231','1240','1241'] # '261', '262', '330', '304', '306']

event_id_map = {
    '1' : 'eSO',
    '2' : 'eMO',
    '3' : 'eFL',
    '4' : 'eS',
    '5' : 'eCS',
    '6' : 'Humidifier is empty',
    '101' : 'oA',
    '102' : 'cA',
    '103' : 'A leakage',
    '104' : 'uA_Softstart',
    '105' : 'A high pressure',
    '106' : 'A movement',
    '108' : 'hPr',
    '111' : 'oH',
    '112' : 'cH',
    '113' : 'H leakage',
    '114' : 'uH_Softstart',
    '115' : 'uH_HighPressure',
    '116' : 'uH_PosChange',
    '121' : 'RERA',
    '131' : 'Snore',
    '141' : 'Artefact',
    '151' : 'Flattening',
    '161' : 'Critical leakage',
    '171' : 'Disconnection',
    '172' : 'Mask test',
    '181' : 'CS respiration',
    '191' : 'Glottal closure',
    '211' : 'IPAP not reached',
    '221' : 'Timed breath',
    '231' : 'Init phase',
    '241' : 'softSTART',
    '242' : 'softSTOP',
    '251' : 'Desaturation',
    '252' : 'Hypoxemia',
    '254' : 'Artefact(SpO2)',
    '301' : 'Leakage alert',
    '303' : 'Disconn. alert',
    '305' : 'Leakage alert',
    '307' : 'Disconnection alert',
    '309' : 'MV low alert',
    '311' : 'Apnea alert',
    '313' : 'VT low alert',
    '315' : 'Volume low alert',
    '316' : 'Volume high alert',
    '317' : 'Frequency low alert',
    '318' : 'Frequency high alert',
    '320' : 'MV high alert',
    '321' : 'Pressure low alert',
    '322' : 'Pressure high alert',

    '1001':'DEBUG_EPOCH_SLEEP_ONSET',
    '1002':'DEBUG_EPOCH_SOFTSTART',
    '1003':'DEBUG_EPOCH_TOOSHORT',
    '1004':'DEBUG_EPOCH_FORCEDEND',
    '1005':'DEBUG_EPOCH_LEAK',
    '1006':'DEBUG_EPOCH_UNRELIABLE',
    '1007':'DEBUG_EPOCH_CENTRAL',
    '1008':'DEBUG_EPOCH_SEVERE_EVENT',
    '1101':'DEBUG_APNEA_TOOSHORT',
    '1102':'DEBUG_APNEA_TOOLONG',
    '1103':'DEBUG_APNEA_UNSPECIFIED',
    '1104':'DEBUG_APNEA_MIXED',
    '1105':'DEBUG_APNEA_FORCEDEND',
    '1106':'DEBUG_INVALID_APNEA_TOOSHORT',
    '1107':'DEBUG_APNEA_COMBINED',
    '1111':'DEBUG_HYPOPNEA_TOOSHORT',
    '1112':'DEBUG_HYPOPNEA_TOOLONG',
    '1113':'DEBUG_HYPOPNEA_OBSTRUCTIVE_FLAT',
    '1114':'DEBUG_HYPOPNEA_INVALID_APNEA',
    '1115':'DEBUG_HYPOPNEA_UNSPECIFIED',
    '1116':'DEBUG_HYPOPNEA_MIXED',
    '1117':'DEBUG_HYPOPNEA_FORCEDEND',
    '1118':'DEBUG_INVALID_HYPOPNEA_TOOSHORT',
    '1120':'DEBUG_RERA_TOO_SHORT',
    '1121':'DEBUG_RERA_INVALID_LEAK',
    '1122':'DEBUG_RERA_INVALID_APNEA',
    '1123':'DEBUG_RERA_INVALID_HYPOPNEA',
    '1124':'DEBUG_RERA_INVALID_DELTA_PDIFF',
    '1125':'DEBUG_RERA_INVALID_DELTA_LEAK',
    '1126':'DEBUG_RERA_MILD',
    '1127':'DEBUG_RERA_MILDSNORE',
    '1128':'DEBUG_RERA_MILDFLAT',
    '1129':'DEBUG_RERA_SEVERE',
    '1130':'DEBUG_RERA_FORCEDEND',
    '1131':'DEBUG_SNORE_INVALID_LEAK',
    '1132':'DEBUG_SNORE_INVALID_HIGHPRESSURE',
    '1133':'DEBUG_SNORE_INVALID_TOOSHORT',
    '1134':'DEBUG_SNORE_FORCEDEND',
    '1141':'DEBUG_ARTEFACT_TOOSHORT',
    '1151':'DEBUG_FLATTENING_INVALID_LEAK',
    '1152':'DEBUG_FLATTENING_INVALID_TOOSHORT',
    '1153':'DEBUG_FLATTENING_FORCEDEND',
    '1154':'DEBUG_FLATTENING_INVALID',
    '1201':'DEBUG_AASM_TITRATION_CYCLE',
    '1221':'DEBUG_TIMED_BREATH',
    '1222':'DEBUG_TIMED_BREATH_OBSTRUCTIVE',
    '1223':'DEBUG_TIMED_BREATH_CENTRAL',
    '1224':'DEBUG_TIMED_BREATH_INVALID_TOOSHORT'
  }

def load_events(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for item in root.findall('./RespEvent'):
        event_id = item.attrib['RespEventID']
        if event_id in skip_events:
            continue
        if event_id in event_id_map:
            print(event_id_map[event_id])
        else:
            print('### UNKNOWN %s' % event_id)

    

def main():
    if len(sys.argv) < 2:
        print("Usage: %s <event file>" % sys.argv[0])
        sys.exit(1)
    FILE = sys.argv[1]
    events = load_events(FILE)

main()