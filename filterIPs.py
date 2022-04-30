#!/bin/python3

import sys
import getopt
import ipaddress

def main(argv):
   inScopeFile = []
   exFile = []
   fileCheck = []
   excludeList = []
   includeList = []
   checkList = []
   singleCheck = ''
   outFileName = ''

   try:
       opts, args = getopt.getopt(argv,"hi:o:x:s:f:",["ifile=","outfile=","xfile="])
   except getopt.GetoptError:
      print ('filterIPs.py -x <ExcludedIPsFile> -i <inScopeIPsFile>') 
      sys.exit(2)

   #go into each argument param
   for opt, arg in opts:
      if opt == '-h':
         print ('filterIPs.py -x <ExcludedIPsFile> -i <inScopeIPsFile> ')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         with open(arg) as tempFile:
            inScopeFile = tempFile.readlines()
      elif opt in ("-x", "--xfile"):
         with open(arg) as tempFile:
            exFile = tempFile.readlines()
      elif opt in ("-f"):
         with open(arg) as tempFile:
            fileCheck = tempFile.readlines()
      elif opt in ("-s"):
         singleCheck = arg
      elif opt in ("-o", "--outfile"):
         outFileName = arg

   #get excluded list and convert any /x into full IP list
   for ip in exFile:
      print("testing IP:", ip)
      if "/" in ip:
          print (ip, "is a cidr notation\n")
          arrayTemp = [str(stripIp) for stripIp in ipaddress.IPv4Network(testIP)]
          print("this is the new IPs", arrayTemp)
      else:
          print (ip, "NOT cidr notation\n")

if __name__ == "__main__":
   main(sys.argv[1:])
