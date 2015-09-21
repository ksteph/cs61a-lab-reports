#Usage
##Lab Report
To generate the report for lab i, use command

```
ipython/python lab_report.py <data_directory> labi
```
where <data_directory> is the directory where data file and map file are stored or the directory containing labi subdirectory. Data file should be named as ```labi.dat``` while map file should be named as ```labi_caseId_str2numId.map``` or ```labi_order.map```. ```labi_order.map``` is the first priority for map file.

Report will be stored in ```report/labi_report```.

##Cross-lab Report
To generate cross-lab report, use command

```
ipython/python cross_lab_report.py <data_directory> <LABS>
```
where <data_directory> is the directory where all data files and map files are stored or the directory containing all lab directories.

Labs contained in the report are listed in LABS variable divided by space, for example,

```
ipython cross_lab_report.py <data_directory> lab01 lab02 lab03
```
will generate a cross-lab report for lab01, lab02 and lab03.

Report will be stored in ```report/cross_lab_report```.

#Requirement
To use the pipeline, make sure following libraries are installed:

- Python library: jinja2
- Python library: numpy
- Python library: matplotlib
- Python library: scipy
- Full latex lib or basic latex lib plus booktabs (not sure if booktabs only is enough)
