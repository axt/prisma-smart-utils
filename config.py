import sys
import xml.etree.ElementTree as ET


skip_events = [] 

event_id_map = {

    # Prisma smart
    
    '6': 'PRISMA_SMART_MODE',
    '9': 'PRISMA_SMART_PRESSURE',
    '10': 'PRISMA_SMART_PRESSURE_MAX',
    '11': 'PRISMA_SMART_PSOFT_MIN',
    '12': 'PRISMA_SMART_PSOFT',
    '13': 'PRISMA_SMART_SOFTPAP',
    '14': 'PRISMA_SMART_SOFTPAP_LOCK',
    '15': 'PRISMA_SMART_APAP_DYNAMIC',
    '16': 'PRISMA_SMART_HUMIDLEVEL',
    '17': 'PRISMA_SMART_AUTOSTART',
    '18': 'PRISMA_SMART_SOFTSTART_TIME_MAX',
    '19': 'PRISMA_SMART_SOFTSTART_TIME',
    '21': 'PRISMA_SMART_TUBE_TYPE',
    '38': 'PRISMA_SMART_PMAXOA',
    

    # Prisma Line
    '1001' : 'ModulVersion',
    '1002' : 'Device',
    '1003' : 'Mode',
    '1011' : 'TI',
    '1012' : 'TE',
    
    '1014' : 'RampEx',
    '1015' : 'WmTrackEx',
    '1016' : 'TargetVolume',
    '1017' : 'IpapSpeed',
    '1020' : 'IntraBreathPressCtrl',

    '1083' : 'HumidifierLevel',
    '1084' : 'AutoStart',
    '1085' : 'MaskTestPress',
    '1086' : 'MaskTestDuration',
    '1091' : 'TubeType',
    '1092' : 'BacteriumFilter',

    '1123' : 'SoftPapLevel',
    '1125' : 'SoftStartPress',
    '1127' : 'SoftStartTime',
    '1128' : 'SoftStartTimeMax',

    '1138' : 'EepapMin',
    '1139' : 'EepapMax', 
    '1140' : 'PdiffNorm',
    '1141' : 'PdiffMax',

    '1150' : 'AbsolutPdiffMinTimed',
    '1154' : 'ExtraObstructionProtection',
    '1156' : 'BackFrequAuto', #?
    '1157' : 'BackGroundFrequ', #?

    '1158' : 'RelativeInspirationDuration',
    
    '1160' : 'RampIn',
    '1162' : 'WmTrack',

    '1199' : 'IPapMax',
    '1200' : 'IPap',
    '1201' : 'Epap',
    '1202' : 'AlarmLeakActive',
    '1203' : 'AlarmDisconnectionActive',

    '1206' : 'AlertApneaLevel',
    '1207' : 'AlertVtLowLevel',
    '1208' : 'AlertAmvLowLevel',
    '1209' : 'Apap_dyn',
    
    '1212' : 'SoftStopTimeMax',
    '1213' : 'SoftStopTime',
    '1214' : 'TiMin',
    '1215' : 'TiMax',
    '1216' : 'TiTimed',
    '1217' : 'HumClimaCtrl',
    '1218' : 'AutoStop',
    '1219' : 'AutoPdiffActive',
    '1220' : 'SoftStartDiffRamp',

    '1223' : 'TargetFlow',
    '1224' : 'O2Flow',



}

def load_events(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for item in root.findall('./DeviceEvent'):
        dev_event_id = item.attrib['DeviceEventID']
        if dev_event_id == '1':
            continue
        param_id = item.attrib['ParameterID']
        value = item.attrib['NewValue']
        
        if param_id in skip_events:
            continue
        if param_id in event_id_map:
            print("%-30s: %s" % (event_id_map[param_id], value))
        else:
            print('### UNKNOWN %s: %s' % (param_id, value))

    

def main():
    if len(sys.argv) < 2:
        print("Usage: %s <event file>" % sys.argv[0])
        sys.exit(1)
    FILE = sys.argv[1]
    events = load_events(FILE)

main()

#param_Unspecified = 0,
#param_NotUsed = 1,
#param_User = 1004, // 0x000003EC
#param_ActiveFlag = 1005, // 0x000003ED
#param_ModeNameTagAppend = 1006, // 0x000003EE
#param_TubeTypeLock = 1007, // 0x000003EF
#param_VentyFeatures = 1008, // 0x000003F0
#p_SetVolumeOutputToZero = 1009, // 0x000003F1
#param_PdiffMinIntern = 1010, // 0x000003F2
#param_RampInTime = 1013, // 0x000003F5
#param_Eepap = 1018, // 0x000003FA
#p_AutoDiff = 1019, // 0x000003FB
#param_IpapDelta = 1022, // 0x000003FE
#param_Verbose = 1023, // 0x000003FF
#param_AlarmVolume = 1087, // 0x0000043F
#param_AlarmClockVolume = 1088, // 0x00000440
#param_ButtonBeepVolume = 1089, // 0x00000441
#param_ExportedData = 1090, // 0x00000442
#param_DeepStandbyAutomatic = 1093, // 0x00000445
#param_DisplayedComplianceLevel = 1094, // 0x00000446
#param_DisplayedCompliance = 1095, // 0x00000447
#param_DisplayBrightness = 1096, // 0x00000448
#param_DisplayedStandbyInfo = 1097, // 0x00000449
#param_GuiFlowUnit = 1098, // 0x0000044A
#param_GuiPressUnit = 1099, // 0x0000044B
#param_GuiLangExpert = 1100, // 0x0000044C
#param_GuiLangPatient = 1101, // 0x0000044D
#param_TimeZone = 1102, // 0x0000044E
#param_DaylightSaving = 1103, // 0x0000044F
#param_AlarmClockActive = 1104, // 0x00000450
#param_AlarmClockHours = 1105, // 0x00000451
#param_AlarmClockMinutes = 1106, // 0x00000452
#param_TwentyFourHoursClock = 1107, // 0x00000453
#param_ServiceReminder = 1108, // 0x00000454
#param_FilterChangeReminder = 1109, // 0x00000455
#param_GuardMaintenance = 1110, // 0x00000456
#param_GuardChangeFilter = 1111, // 0x00000457
#p_AnalogChannel_1 = 1112, // 0x00000458
#p_AnalogChannel_2 = 1113, // 0x00000459
#p_AnalogChannel_3 = 1114, // 0x0000045A
#p_AnalogChannel_4 = 1115, // 0x0000045B
#p_AnalogChannel_5 = 1116, // 0x0000045C
#p_AnalogChannel_6 = 1117, // 0x0000045D
#p_AnalogChannel_7 = 1118, // 0x0000045E
#p_AnalogChannel_8 = 1119, // 0x0000045F
#param_Pmax = 1120, // 0x00000460
#param_Pmin = 1121, // 0x00000461
#p_CpapPress = 1122, // 0x00000462
#param_SoftPapFreeze = 1124, // 0x00000464
#param_SoftStartPressMin = 1126, // 0x00000466
#param_ApapMin = 1130, // 0x0000046A
#param_ApapMax = 1131, // 0x0000046B
#param_Delta = 1142, // 0x00000476
#param_EpapMin = 1143, // 0x00000477
#param_EpapMax = 1144, // 0x00000478
#param_EpapMinIntern = 1146, // 0x0000047A
#param_IpapMinIntern = 1147, // 0x0000047B
#param_EpapMaxIntern = 1148, // 0x0000047C
#param_AbsolutPdiffMin = 1149, // 0x0000047D
#param_EpapTimed = 1151, // 0x0000047F
#param_IpapMaxIntern = 1152, // 0x00000480
#param_IpapMaxTimed = 1153, // 0x00000481
#param_Scope = 1155, // 0x00000483
#p_SprFrequMerge = 1159, // 0x00000487
#param_FrequAlertLvl = 1161, // 0x00000489
#p_IpapMin = 1198, // 0x000004AE
#param_AlarmLockedForPatient = 1204, // 0x000004B4
#param_CheckSum = 1205, // 0x000004B5
#param_HumidifierLevel_max = 1210, // 0x000004BA
#param_TeleSettingsAllowed = 1211, // 0x000004BB
#param_InspToExp = 1221, // 0x000004C5
#param_Delta2 = 1222, // 0x000004C6
