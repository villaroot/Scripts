#!/bin/python3

import sys
import struct
import socket
import getopt
import ipaddress

#expand the CIDR IPs and return array of IPs
def expandCIDR(tempIP):
    expandArray = []
    (ip, cidr) = tempIP.split('/')
    cidr = int(cidr)
    host_bits = 32 - cidr
    i = struct.unpack('>I', socket.inet_aton(ip))[0] # note the endianness
    start = (i >> host_bits) << host_bits # clear the host bits
    end = start | ((1 << host_bits) - 1)
    for i in range(start,end):
        expandArray.append(socket.inet_ntoa(struct.pack('>I',i)))
    return expandArray

def helpFunc():
    print("""
filterIPs.py is used for checking if an IP is In Scope and not in the Excluded IP List.
It can take CIDR IPs and expands them to the full IP list. Meaning it's possible to provide a value such as 192.0.0.0/24 and the script will expand it to all IPs in the /24 subnet.

    filterIPs.py
      -x Excluded IPs file
      -i In Scope IPs file
      -s single IP to check
      -f file of IPs to check

      Usage:
        python3 filterIPs.py [-x FILE] [-i FILE] [-s STRING] [-f FILE]

      Example:
        python3 filterIPs.py -x 'c:\excludedIP.txt' -i 'c:\inScopeIPs.txt' -s 10.10.10.10

        python3 filterIPs.py -x 'c:\excludedIP.txt' -i 'c:\inScopeIPs.txt' -f 'c:\\targets.txt'
        """)

def main(argv):
   inScopeFile = []
   excludeFile = []
   fileCheck = []

   excludeList = []
   inScopeList = []
   checkList = []
   approvedList = []
   neitherList = []
   deniedList = []

   singleCheck = ''
   manualInScopeLocation = "" #option to manually put location MAKE SURE TO PUT TWO SLASHES
   manualExcludeLocation = "" #option to manually put location MAKE SURE TO PUT TWO SLASHES

   try:
       opts, args = getopt.getopt(argv,"hi:x:s:f:",["ifile=","xfile="])
   except getopt.GetoptError:
      print ('filterIPs.py -x <ExcludedIPsFile> -i <inScopeIPsFile> -s <targetIP>')
      sys.exit(2)

   #go into each argument param
   for opt, arg in opts:
      if opt == '-h':
         #print ('filterIPs.py -x <ExcludedIPsFile> -i <inScopeIPsFile> -s <targetIP>')
         helpFunc()
         sys.exit()
      elif opt in ("-i", "--ifile"):
         with open(arg) as tempFile:
            inScopeFile = tempFile.readlines()
      elif opt in ("-x", "--xfile"):
         with open(arg) as tempFile:
            excludeFile = tempFile.readlines()
      elif opt in ("-f"):
         with open(arg) as tempFile:
            fileCheck = tempFile.readlines()
      elif opt in ("-s"):
         singleCheck = str(arg)

   if not excludeFile and manualExcludeLocation:
       with open(manualExcludeLocation) as tempFile:
          excludeFile = tempFile.readlines()
       print ("[+] Excluded file:", manualExcludeLocation)
   else:
       print ("[!] Excluded List was not provided")
       print ("Usage: filterIPs.py -x <ExcludedIPsFile> -i <inScopeIPsFile> -s <targetIP>")

   if not inScopeFile and manualInScopeLocation:
       with open(manualInScopeLocation) as tempFile:
          inScopeFile = tempFile.readlines()
       print ("[+] In Scope file:", manualInScopeLocation)
   else:
       print ("[!] In Scope file was not provided")
       print ("Usage: filterIPs.py -x <ExcludedIPsFile> -i <inScopeIPsFile> -s <targetIP>")

   #Go through the excluded IP array and convert any CIDR /x into full IP list
   for tempIP in excludeFile:
      if "/" in tempIP:
          excludeList.extend(expandCIDR(tempIP))
      else:
          excludeList.append(tempIP.rstrip())

   #Go through the In Scope IP array and convert any CIDR /x into full IP list
   for tempIP in inScopeFile:
      if "/" in tempIP:
          inScopeList.extend(expandCIDR(tempIP))
      else:
          inScopeList.append(tempIP.rstrip())

   #if a file of targets were given, add to 'checkList' and expand any CIDRs
   if fileCheck:
      for tempIP in fileCheck:
         if "/" in tempIP:
             checkList.extend(expandCIDR(tempIP))
         else:
             checkList.append(tempIP.rstrip())

   #check if the 'single' IP provided is a CIDR, expand if it is, if not add to checkList
   if singleCheck:
    if "/" in singleCheck:
       checkList.extend(expandCIDR(singleCheck))
    else:
       checkList.append(singleCheck.rstrip())

   print("")

   #check elements in checkList to see if either exluded or in scope list, or not in either
   for verifyIP in checkList:
      if verifyIP in excludeList:
         deniedList.append(verifyIP)
      elif verifyIP in inScopeList:
         approvedList.append(verifyIP)
      else:
         neitherList.append(verifyIP)

   if approvedList:
       print("[+] Below are approved for testing")
       for item in approvedList:
           print(item, end="\n")
   else:
       print("[-] No IPs were approved for testing!")

   if neitherList:
       print("[!] IPs were provided that are in neither the In Scope or Exluded Lists")
       for item in neitherList:
           print(item, end="\n")

if __name__ == "__main__":
   main(sys.argv[1:])
