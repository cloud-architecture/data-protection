"""
#############################################################
#    server side encryption - kms clean up for usecase-1    #
#############################################################
"""
from pathlib import Path
import subprocess
import sys
import os 
import json
import boto3
import time 
import subprocess

def main():
    """
    #######################################################
    #     Cleaning up all S3 buckets and files created    #
    #######################################################
    """
    try:
        print "\n It takes about 10 minutes for the final cleanup to complete and all CF stacks to be deleted from your account" 
        print "\n Please leave this browser window open until all CF stacks created for this workshop are deleted"
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        s3_client = boto3.client('s3', region)
        cf_client = boto3.client('cloudformation')
        s3_resource = boto3.resource('s3')

        response = s3_client.list_buckets()
        
        for bucket_name in response['Buckets']:
            if bucket_name['Name'].startswith('data-protection-env-setup'):
                try:
                    response = s3_client.get_bucket_tagging(
                        Bucket=bucket_name['Name']
                    )
                    
                    if 'TagSet' in response: 
                        for tag in response['TagSet']:
                            if (tag['Key'] == 'bucket-for-what') and (tag['Value'] == region + '-' + 'system-cloudtrail-log-storage'):
                                # Delete the objects stored in S3 within reinvent-builders-bucket
                                s3_bucket = s3_resource.Bucket(bucket_name['Name'])
                                s3_bucket.objects.all().delete()
                    
                    response = s3_client.delete_bucket(
                        Bucket=bucket_name['Name']
                    )          
                except:
                    pass
        
        
        
        # # Remove Cloudformation stacks        
        response = cf_client.list_stacks(
            StackStatusFilter=[
                'CREATE_COMPLETE',
            ]
        )
        #print response
        
        for stack in response['StackSummaries']:
            if stack['StackName'] == 'template-workshops-setup':
                print subprocess.check_output(['aws','cloudformation','delete-stack','--stack-name','template-workshops-setup'])
                time.sleep(200)

        print "\n Final CF stack cleanup initiated - you can go ahead and close this browser window" 
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    