import os
import fileinput

environmentDir = os.environ["CONDA_PREFIX"] + "\\"
pyFirmataDir = "Lib\\site-packages\\pyfirmata\\"

with fileinput.input(environmentDir + pyFirmataDir + "pyfirmata.py", inplace = True) as f:
    n = 0
    for line in f:
        n += 1
        if n > 148 and n < 152:
            if not line[0] == "#":
                line = "#" + line
        print(line, end='')
        
print("pyFirmata successfully debugged.")

