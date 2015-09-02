#Usage
##Lab Report
To generate the report for lab i, use command

```
ipython lab_report.py <data_directory> labi
```
where <data_directory> is the directory where data file and map file are stored. Data file should be named as labi.dat while map file should be named as labi_caseId_str2numId.map.

Report will be stored in report/labi_report. 

##Cross-lab Report
To generate cross-lab report, use command

```
ipython cross_lab_report.pu <data_directory>
```
where <data_directory> is the directory where all data files and map files are stored.

Labs contained in the report are listed in LABS variable in cross_lab_report.py.

Report will be stored in report/cross_lab_report.
