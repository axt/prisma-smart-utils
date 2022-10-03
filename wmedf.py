#!/usr/bin/env python
import sys
import datetime


def transform_range(digvalue, digmin, digmax, physmin, physmax):
    return (digvalue - digmin) * (physmax - physmin) / (digmax - digmin) + physmin

def parse_header(buffer):
    version = buffer[0:8].decode('utf-8')
    patient_name = buffer[8:88].decode('utf-8')
    recording_information = buffer[88:168].decode('utf-8')
    start_date = buffer[168:176].decode('utf-8')
    start_time = buffer[176:184].decode('utf-8')
    header_length = buffer[184:192].decode('utf-8')
    reserved = buffer[192:236].decode('utf-8')
    number_of_data_records = buffer[236:244].decode('utf-8')
    duration_of_a_data_record_in_seconds = buffer[244:252].decode('utf-8')
    number_of_signals = int(buffer[252:256].decode('utf-8'))
    startts = int(datetime.datetime.strptime(start_date + 'T' + start_time, '%d.%m.%yT%H.%M.%S').timestamp())


    print("Version: " + version)
    print("Patient name: " + patient_name)
    print("Recording information: " + recording_information)
    print("Start date: " + start_date)
    print("Start time: " + start_time)
    print("Timestamp:" + str(startts))
    print("Header length: " + header_length)
    print("Reserved: " + reserved)
    print("Number of data records: " + number_of_data_records)
    print("Duration of a data record in seconds: " + duration_of_a_data_record_in_seconds)
    print("Number of signals: " + str(number_of_signals))


    pos = 256
    signal_names = [buffer[pos+i*16:pos+(i+1)*16].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*16
    transducer_types = [buffer[pos+i*80:pos+(i+1)*80].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*80
    physical_dimensions = [buffer[pos+i*8:pos+(i+1)*8].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*8
    physical_minima = [buffer[pos+i*8:pos+(i+1)*8].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*8
    physical_maxima = [buffer[pos+i*8:pos+(i+1)*8].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*8
    digital_minima = [buffer[pos+i*8:pos+(i+1)*8].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*8
    digital_maxima = [buffer[pos+i*8:pos+(i+1)*8].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*8
    prefiltering = [buffer[pos+i*80:pos+(i+1)*80].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*80
    number_of_samples_in_each_data_record = [buffer[pos+i*8:pos+(i+1)*8].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*8
    reserved = [buffer[pos+i*32:pos+(i+1)*32].decode('utf-8').strip() for i in range(0, number_of_signals)]
    pos += number_of_signals*32

    signal_bytes = []
    signal_data = []
    for i in range(0, number_of_signals):
        signal_data.append([])
        digital_range = int(digital_maxima[i]) - int(digital_minima[i])
        if (digital_range < 256):
            signal_bytes.append(1)
        elif (digital_range < 65536):
            signal_bytes.append(2)
        else:
            raise Exception("Digital range not handled")


        print("Signal name       : ", (signal_names[i]))
        print("Transducer type   : ", (transducer_types[i]))
        print("Physical dimension: ", (physical_dimensions[i]))
        print("Physical minima   : ", (physical_minima[i]))
        print("Physical maxima   : ", (physical_maxima[i]))
        print("Digital minima    : ", (digital_minima[i]))
        print("Digital maxima    : ", (digital_maxima[i]))
        print("Prefiltering      : ", (prefiltering[i]))
        print("Number of samples in each data record: ", (number_of_samples_in_each_data_record[i]))
        print("Reserved          : ", (reserved[i]))
        print("")


    if int(number_of_data_records) == -1:
        bytes = 0
        for i in range(0, number_of_signals):
            bytes += int(number_of_samples_in_each_data_record[i]) * signal_bytes[i]
        number_of_data_records = (len(buffer) - int(header_length)) /  bytes
    
    for k in range(0, int(number_of_data_records)):
        for i in range(0, number_of_signals):
            for j in range(0, int(number_of_samples_in_each_data_record[i])):
                if (signal_bytes[i] == 1):
                    if int(digital_minima[i]) >= 0:
                        signal_data[i].append(int.from_bytes(buffer[pos:pos+signal_bytes[i]], byteorder='big', signed=False))
                    else:
                        signal_data[i].append(int.from_bytes(buffer[pos:pos+signal_bytes[i]], byteorder='big', signed=True))
                elif (signal_bytes[i] == 2):
                    signal_data[i].append(int.from_bytes(buffer[pos:pos+signal_bytes[i]], byteorder='big', signed=True))
                else:
                    raise Exception("Signal byte not handled")
                pos += signal_bytes[i]

    for i in range(0, number_of_signals):
        with open(signal_names[i] + ".txt", 'w') as f:
            for j in range(0, len(signal_data[i])):
                f.write("%s\t%s\n" % (
                    startts+ j* float(duration_of_a_data_record_in_seconds) / float(number_of_samples_in_each_data_record[i]),
                    str(
                    transform_range(
                        signal_data[i][j], 
                        int(digital_minima[i]), 
                        int(digital_maxima[i]), 
                        float(physical_minima[i]), 
                        float(physical_maxima[i])
                    ))))


if len(sys.argv) < 2:
    print("Usage: %s <wmedf file>" % sys.argv[0])
    sys.exit(1)

with open(sys.argv[1], 'rb') as f:
    buffer = f.read()
    parse_header(buffer)

