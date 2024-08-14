from setuptools import setup

setup(
        name = "automatedMouseMaze",
        version = "0.1.0", 
        description = "GUI for automated maze for mice",
        url = "https://github.com/luismfranco/automatedMouseMaze",
        author = "Luis Franco",
        author_email = "luisfran@uoregon.edu",
        license = "007 license to kill",
        packages = ["automatedMouseMaze"],
        python_requires = "=3.10.14",
        install_requires = [
                            "tkinter = 8.6",
                            "pillow = 10.4.0",
                            "pyfrimata = 1.1.0",
                            "pyserial = 3.5",
                            "simpleaudio = 1.0.4",
                            "pandas = 2.2.2",
                            "numpy = 1.25.2",
                            "psychopy = 2024.2.1",
                           ],

        classifiers = [
                        'Development Status :: 3 - Alpha',
                        'Intended Audience :: Science/Research',
                        'Operating System :: POSIX :: Windows',        
                        'Programming Language :: Python :: 3.10.14',
            ],
)

