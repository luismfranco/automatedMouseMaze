from setuptools import setup, find_packages

setup(
      
      # App Info
      name = "automatedMouseMaze",
      version = "1.0.0", 
      description = "GUI for experiments in an automated maze for mice",
      author = "Luis M. Franco",
      author_email = "luisfran@uoregon.edu",
      license = "MIT",
      url = "https://github.com/luismfranco/automatedMouseMaze",

      # Dependencies
      packages = find_packages(),
      python_requires = "== 3.10.14",
      install_requires = [
                          "pillow == 10.4.0",
                          "pyFirmata == 1.1.0",
                          "pyserial == 3.5",
                          "simpleaudio == 1.0.4",
                          "pandas == 2.2.2",
                          "numpy == 1.25.2",
                          "ntplib == 0.4.0",
                          "open-ephys-python-tools == 0.1.12",
                          "psychopy == 2024.2.1",
                          "moderngl == 5.11.1",
                          "pyglm == 2.7.1",
                          "pygame == 2.6.0",
                          "pywavefront == 1.3.3",
       ],
      
      # Classifiers
      classifiers = [
                     "Development Status :: 3 - Alpha",
                     "Intended Audience :: Science/Research",
                     "Operating System :: Windows",        
                     "Programming Language :: Python :: 3.10.14",
      ],
      
)