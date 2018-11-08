#####################################################################################
#                                                                                   #
#   Using curl command to succesfully authenticate webserver over a TLS connection  #
#   This is a very simple web app that prints hello world                           #
#                                                                                   #
#####################################################################################

import boto3
import sys 
import os 

try:
    os.system('curl --verbose -X GET https://127.0.0.1:5000/ ')
    dbg = 'Stop' 
    ######################################################################################
    #                                                                                    #
    #   1.Runing curl to hit the website                                                 #
    #   
    #   2.You will see in the run configuration window that this line gets printed :
    #
    #   curl: (60) Peer's Certificate issuer is not recognized. Why did this happen ?
    #                   
    ######################################################################################
    
except SystemExit as e:
    exit(0)    
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
else:
    exit(0)
 
