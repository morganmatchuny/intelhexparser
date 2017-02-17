import sys
import struct

def parse_line(line):
    if len(current_line) == 0:
    	return
    #defining locations of info based on Intel hex format
    length = int(line[0:2], 32)
    address = int(line[2:6], 32)
    record_type = int(line[6:8], 32	)
    checksum = line[40:42]
    #printing output
    record_output = str(hex(address)) + '\t\t\t' + str(length) + '\t\t'
    if record_type == 0:
        record_output += 'data'
        data = line[8:40]
        #reverse byte order stuff here...
        record_output += '\t\t\t' +  "".join(reversed([data[i:i+2] for i in range(0, len(data), 2)]))
    elif record_type == 1:
        record_output += 'end of file'
        record_output += '\t\t\t' + line[8:(8+2*(length))]
    elif record_type == 2: #extended segment address
        record_output += 'ext. segment addr.'
        record_output += '\t\t\t' + line[8:(8+2*(length))]
    elif record_type == 4:	#extended linear address
        record_output += 'ext. linear addr.'
        record_output += '\t' + line[8:(8+2*(length))]
    print record_output + '\t\t\t' + checksum

#open hex
hex_file = open('test.hex', 'r')

#analyze hex file line by line
current_line = ""
try:
    byte = "1" # initial placeholder
    print "address\t\tlength\t\ttype\t\t\t\t\tdata\t\t\t\t\t\t\tchecksum"
    while byte != "":
        byte = hex_file.read(1)
        if byte == ":":
            #parse the current line
            parse_line(current_line)
       		#start line over to get next line of info
            current_line = ""
        else:
            current_line += byte
    parse_line(current_line)
#done!
finally:
    hex_file.close()
