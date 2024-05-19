# Example Sequence File For Landscape_DataStream v1.0
import numpy as np

# Functions
def ________start_of_functions________(*args):
    return 0

def array1D(start, end, step):
    if start <= end:
        step = +abs(step)
    else:
        step = -abs(step)
    array = np.arange(start, end, step)
    array = np.append(array, end)
    array = array.tolist()
    return array

def array1Dnum(start, end, number):
    array = np.linspace(start, end, number)
    array = array.tolist()
    return array

def sarray1D(start,end,step,*args):
    # First column is file suffix: 0 is original dataset, 1 is retrace dataset, 2 is dump dataset
    # Second column is index: 0,1,2,3,4,5,...
    # From the third column is the scan array
    line = 0
    array1 = []
    for d1 in array1D(start, end, step):
        array1.append([0, line, d1])
        line = line + 1
    for d1 in array1D(start, end, step)[::-1]:
        array1.append([1, line, d1])
        line = line + 1
    return array1

def sarray2D(start1, end1, step1, start2, end2, step2):
    # First column is file suffix: 0 is original dataset, 1 is retrace dataset, 2 is dump dataset
    # Second column is index: 0,1,2,3,4,5,...
    # From the third column is the scan array
    line = 0
    array2 = []
    for d2 in array1D(start2, end2, step2):
        for d1 in array1D(start1, end1, step1):
            array2.append([0, line, d1, d2])
            line = line + 1
        for d1 in array1D(start1, end1, step1)[::-1]:
            array2.append([1, line, d1, d2])
            line = line + 1
    return array2

def ________end_of_functions________(*args):
    return 0

### ------------------------------------------------------------------------------------------ ###

# Instrument

def ________start_of_instruments________(*args):
    return 0

def pyspeedtester(*args):
    # instrument_parameters is a list of (string, string) tuples
    instrument_parameters = [
        ("Description", "Python Speed Test"),
        ("Version", "1.0"),
        ("Type", "Python"), # Default\External\Python
        # Default = Internal communication module, recommended for standard instrument
        # External = Custom LabView VI, Action = Call, Initialize, Retrieve, Scan, Approach, Write, Read, Close
        # Python = Custom Python based communication module
        ("Address", "Complete file path of the Python Speed Tester"),
        # Default = Instrument VISA address
        # External = Complete file path of the LabView VI
        # Python = Complete file path of the Python file
        # Scan Setup
        ("Scan Name", "Test_Scan"), # Required for All
        # The column name of the scan value
        ("Mode", "Speed Test"),
        ("Retrieve Command", r""), # Required by Default
        ("Scan Command", r""), # Required by Default
        ("Ramp Step", "10ms"), # Required by Default
        # The Default module can recogonize 10m,10n,10k,10M,... suffix
        ("Ramp Delay", "10ms"), # Required by Default
        ("Scan Limit", r"-10V\+10V"), # Required by Default
        ("Scan Stablize", "False"), # Required by Default
        # If true, will wait for a specific amount of time (Scan Stablize Timeout) after scan
        ("Scan Stablize Timeout", "0s"), # Required by Default
        ("External VI Behavior", "Mini"), # Required by Custom LabView VI
        #Showm\Mini\Hide
        # Read Setup
        ("Read Command", r""), # Required by Default
        ("Read Name", r"Test_set_read\Test_read_1\Test_read_2"), # Required for all
        ("Buffer", "True"), # Required by Default
        # All paramters will be passed to module during Call action, and updated after Call
    ]
    return instrument_parameters

def ________end_of_instruments________(*args):
    return 0

### ------------------------------------------------------------------------------------------ ###

# Measurement Sequence

def ________start_of_sequence________(*args):
    return 0

def get_all_sequence(*arg):

    allsequence = [
        "Speed_Test",
    ]
    return allsequence

def Speed_Test(*arg):
    # First column is file suffix 0 is original dataset, 1 is retrace dataset, ...
    # Second column is index: 0,1,2,3,4,5,...
    # From the third column is the scan array

    description = "Test Speed"

    dataset_info = [
        ("Description", description),
        ("File Name", "Speedtest"),
        ("Dataset Name", "Speedtest"),
        ("Note", ""),
        ("Scan Delay", "0ms"),
        ("Read Interval", "0ms"),
        ("Read Repeat", "1"),
        ("Read After Scan", "False"),
        ("Skip Countdown", "True"),
    ]

    # scan_instrument is the name of the Scan Instrument function
    scan_instrument = [
        "pyspeedtester",
    ]

    # read_instrument is the name of the Read Instrument function
    read_instrument = [
        "pyspeedtester",
    ]

    # Instrument 1
    start_1 = 0
    end_1 = 10000
    step_1 = 1

    # Outer Loop Instrument
    start_2 = 0
    end_2 = 0
    step_2 = 0.1

    dataset_info = dataset_info + [
        ("x_start", str(start_1)),
        ("x_end", str(end_1)),
        ("x_step", str(step_1)),
        ("y_start", str(start_2)),
        ("y_end", str(end_2)),
        ("y_step", str(step_2)),
        ("z", "gx"),
    ]

    data_processing = [
    ]

    #return (dataset_info, scan_instrument, read_instrument , [], data_processing)
    return (dataset_info, scan_instrument, read_instrument , sarray1D(start_1, end_1, step_1, start_2, end_2, step_2), data_processing)

def ________end_of_sequence________(*args):
    return 0

### ------------------------------------------------------------------------------------------ ###

def main():
    pass

if __name__ == '__main__':
    main()