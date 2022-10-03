#!/usr/bin/env python
import sys
import json
import datetime

def load_stats(fname):
    with open(fname) as f:
        content = f.read()
        return json.loads(content)

def format_ts(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

def format_duration(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return "%d:%02d" % (hours, minutes)

def percentile(arr, pct):
    summa = sum(arr)
    limit = summa * pct
    cur = 0
    for i, val in enumerate(arr):
        cur += val
        if cur >= limit:
            return i

def high_leak_duration(leak_histogram):
    return round(sum([leak_histogram[i] for  i in range(14,20)]) * 2 / 60)

def percentage(duration, total_duration):
    if total_duration == 0:
        return 0
    else:
        return round(100.0*float(duration)/float(total_duration))

def index(first, second):
    if second == 0:
        return 0
    else:
        return round(float(first)/(float(second) / 60.0))

def ts_to_date(unixTime):
    dt = datetime.datetime(1970, 1, 1, 0, 0, 0).replace(tzinfo=None) + datetime.timedelta(seconds=unixTime)
    if dt.hour < 12:
        dt += datetime.timedelta(days=-1)
    return dt.strftime('%Y-%m-%d')


def read_usage_pattern_histogram(hist):
    ret = [ False ] * 24
    num = 1
    for index in range(23, 0, -1):
        if (hist & num) > 0:
            ret[index] = True
        num <<= 1
    return ret

leakage_values = [0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]

parameter_enum = ['UNUSED', 'DeviceType', 'DevicePlatformType', 'DevicePriceVariant', 'DeviceVariant', 'ActiveFlag', 'Mode', 'Pmin', 'Pmax', 'Pressure', 'PressureMax', 'Psoft_min', 'Psoft',
    'SoftPap', 'SoftPapLock', 'ApapDynamic', 'HumidifierLevel', 'AutoStart', 'SoftStartTimeMax', 'SoftStartTime', 'AutoDIP', 'TubeType', 'TubeTypeLock', 'TherapyStandbyTime', 'ClockChangeMode',
    'AutoDark', 'PressureUnit', 'DisplayBrightness', 'BluetoothMode', 'AlarmClockVolume', 'AlarmClockHour', 'AlarmClockMinute', 'AlarmClockActive', 'AlarmVolume', 'AlarmLock', 'AlarmLeakActive',
    'AlarmDisconnectionActive', 'TeleConfLock', 'PmaxoA']

def get_parameter(cfg, parameter_name):
    idx = parameter_enum.index(parameter_name)
    if idx < 0:
        return None
    raw = cfg[str(idx)]
    if parameter_name in ['Pmin', 'Pmax', 'PmaxoA', 'Pressure', 'PressureMax']:
        return raw / 100.0
    elif parameter_name in ['Mode']:
        return 'CPAP' if raw == 1 else 'APAP' if raw == 2 else None
    else:
        return raw

def main():
    if len(sys.argv) < 2:
        print("Usage: %s <statistics file>" % sys.argv[0])
        sys.exit(1)
    
    stat = load_stats(sys.argv[1])

    print("Version: %s" % stat['version'])
    print("Date   : %s" % format_ts(stat['date']))
    print("Hash   : %s" % format_ts(stat['hash']))
    print("Dev    : %s" % stat['dev'])
    print("Use    :")
    print("Crc    : %s" % stat['crc'])
    print("  therapy         : %s" % format_duration(stat['use']['1']))
    print("  humidifier      : %s" % format_duration(stat['use']['2']))
    print("  usage duration  : %s" % format_duration(stat['use']['3']))
    print("  operating hours : %s" % format_duration(stat['use']['4']))
    print("  timestamp       : %s" % format_ts(stat['use']['31']))

    for daywrapper in stat['days']:
        day = daywrapper['day']
        cfgwrapper = json.loads(day['cfg'])
        cfg = cfgwrapper['cfg']

        timestamp = int(day['5'])
        therapy_minutes = int(day['6'])
        humidifier_minutes = int(day['7'])
        leak_histogram = day['10']
        pressure_demand_histogram = day['21']
        duration_deep_sleep = int(day['42'])
        duration_periodic_breathing = int(day['9'])
        duration_snore = int(day['20'])*2
        duration_flattening = int(day['19'])*2
        ambient_temp = int(day['28'])
        oAhi = int(day['16'])
        cAhi = int(day['17'])
        oAi = int(day['37'])
        cAi = int(day['38'])
        uAi = int(day['41'])


        OAi = index(oAi,therapy_minutes)
        CAi = index(cAi,therapy_minutes)
        UAi = index(uAi,therapy_minutes)
        OAhi = index(oAhi,therapy_minutes)
        CAhi = index(cAhi,therapy_minutes)
        UAhi = UAi
        CHi = CAhi - CAi
        OHi = OAhi - OAi
        Hi = OHi + CHi
        Ai = OAi + CAi +  (UAi if UAi > 0 else 0)
        CAhi_without_cH = CAhi - CHi
        Ahi = OAhi + CAhi_without_cH + (UAhi if UAhi > 0 else 0)
        Ahi_including_cH = OAhi + CAhi + (UAhi if UAhi > 0 else 0)

        print("")
        print("Day %s (%s)"  % (ts_to_date(timestamp), format_ts(timestamp)))
        print("  mode                : %s" % get_parameter(cfg, 'Mode'))
        print("  pressure            : %.1f cmH2O" % get_parameter(cfg, 'Pressure'))
        print("  pressure max        : %.1f cmH2O" % get_parameter(cfg, 'PressureMax'))
        print("  usage               : %s" % format_duration(therapy_minutes))
        print("  usage (humidifier)  : %s" % format_duration(humidifier_minutes))

        print("  leakage  P50        : %s l/min" % leakage_values[percentile(leak_histogram, 0.5)])
        print("  leakage  P95        : %s l/min" % leakage_values[percentile(leak_histogram, 0.95)])
        print("  highleak            : %s\t%d%%" % (format_duration(high_leak_duration(leak_histogram)),percentage(high_leak_duration(leak_histogram), therapy_minutes)))

        print("  pressure P50        : %.1f cmH2O" % (4+percentile(pressure_demand_histogram, 0.5)*0.5))
        print("  pressure P90        : %.1f cmH2O" % (4+percentile(pressure_demand_histogram, 0.9)*0.5))


        print("  periodic breathing  : %s\t%d%%" % (format_duration(duration_periodic_breathing), percentage(duration_periodic_breathing, therapy_minutes)))
        print("  deep sleep          : %s\t%d%%" % (format_duration(duration_deep_sleep), percentage(duration_deep_sleep, therapy_minutes)))
        print("  snore               : %s\t%d%%" % (format_duration(duration_snore), percentage(duration_snore, therapy_minutes)))
        print("  flattening          : %s\t%d%%" % (format_duration(duration_flattening), percentage(duration_flattening, therapy_minutes)))

        print("  RERA index          : %d/h" % index(int(day['18']), therapy_minutes))
        #print("  OAhi                : %d" % OAhi)
        #print("  CAhi                : %d" % CAhi)
        print("  OAi                 : %d" % OAi)
        print("  CAi                 : %d" % CAi)
        #print("  UAi                 : %d" % UAi)

        print("  OHi                 : %d" % OHi)
        print("  CHi                 : %d" % CHi)
        #print("  Hi                  : %d" % Hi)
        #print("  CAhi (without cH)   : %d" % CAhi_without_cH)
        #print("  Ai                  : %d" % Ai)
        print("  Ahi                 : %d" % Ahi)
        print("  Ahi (including cH)  : %d" % Ahi_including_cH)

        print("  usage_pattern       : %s" % "".join(list(map(lambda b: '#' if b else '_', read_usage_pattern_histogram(day['15'])))))


        if ambient_temp > 0:
            print("  ambient temp        : %d"  % ambient_temp)

        # print("  key 44                : %d" % int(day['44']))    # duration sleep fragmentation 
        # print("  key 46                : %d" % int(day['46']))    # unknown

main()