from collections import defaultdict, namedtuple
from glob import glob
from datetime import datetime
import re

filenames = r'C:\Temp\*.txt'

start_string = 'Start'
end_string = 'End'

uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

uuid_times = defaultdict()


def process_line(line):
    linelist = line.split('|')
    time = linelist[1].strip()
    uuid = re.search(uuid_pattern, line)
    
    if uuid:
        identifer = '{uuid}'.format(uuid=uuid.group(0))
    
        if start_string in line:
            uuid_times[identifer] = {'start': time, 'end': None, 'duration': None}
        
        if end_string in line:
            if identifer not in uuid_times.keys():
                # This uuid has not seen a start time, probably in 
                # a previous log file we don't have.
                return
            
            uuid_times[identifer]['end'] = time
            
            duration = datetime.strptime(uuid_times[identifer]['end'], '%H:%M:%S.%f') - datetime.strptime(uuid_times[identifer]['start'], '%H:%M:%S.%f')
            uuid_times[identifer]['duration'] = duration
			
			

def process_files(filenames):
    for filename in glob(filenames):
        with open(filename,'r') as file:
            for line in file.readlines():
                process_line(line) 
            
if __name__ == '__main__':
    # Process the log files:
	process_files(filenames)
    
    # Print out the duration of each uuid:
    for uuid in uuid_times:
        print uuid, uuid_times[uuid]['duration']
