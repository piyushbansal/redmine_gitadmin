#!/usr/bin/python

LAB_HOME='/labs/'
DEBUG=False
def run_command(command=None):
    import commands
    if command is None:
        return ['1',"error"]
#### here we would get two values status, output as response of commands.getstatusoutput(command) function.
    response = commands.getstatusoutput(command)
    if DEBUG:
	print "command is "+command
	print response[1]
    return response

def request_parser(param):
    import json
    request = None
    try:
        request = json.loads(param)
    except e:
        print "Error parsing "+ e
    return request

def response_gen(response_obj):
#### Here we are using a lightweight data interchange python module called json .
    import json
    response = None
#### json.dumps would take a dictionary (similar to hash in ruby) and return a string (remember that response_obj was containing response of create or discard functions.
    try:
        response = json.dumps(response_obj)
#### except error, in which case it would return an error message saying that json could not process .
    except e:
        print "unable to process to json "+ e
    return response



def create(labid,repo):
	# check if the repo exists 
	import os
	if os.path.exists(LAB_HOME+labid+'/'+repo):		
		return {'status' : 0 , 'summary' : 'repo exists'}
	# create the repo 
	repo_location = LAB_HOME+labid+'/'+repo
	#print repo_location
	print repo_location
#### here we are going into the directory /labs/"labid"/ and initialising an empty git repo there.
	run_command('cd '+ LAB_HOME+ labid + ' ;git init --bare '+repo+' ; chmod -R g+w '+repo)[1]
#### we create a folder /tmp/ldk 
	run_command('mkdir -p /tmp/ldk')[1]
#### here we clone all the files at repo_location to /tmp/ldk
	run_command('git clone file://'+repo_location+' /tmp/ldk')[1]
#### now we copy contents of ldk/ into /tmp/ldk
	run_command('cp -r ldk/* /tmp/ldk')[1]
#### cd into /tmp/ldk add new changes , commit and remove the temporary repo.
	run_command('cd /tmp/ldk ; git add * ;git commit -m "LDK committed"')[1]
	run_command('cd /tmp; rm -rf /tmp/ldk')[1]
	# fix repo cache group write issue
	run_command('chmod g+w '+repo_location+'/db/rep-cache.db')
	return {'status' : 1 ,'summary' : 'Repo initialized with ldk' }

def discard(labid,repo):
#### we delete the repository , and then return a dictionary with status 1 (successful) and summary-"repo removed".
	run_command('rm -rf '+LAB_HOME+labid+'/'+repo)
	return {'status' : 1 ,'summary' : 'Repo removed' }


if __name__ == '__main__':
    import sys
#### we obtain the various parameters as command line arguments 
    params = sys.argv
#### the first parameter would either be 'add' or discard' - add to create a repo and discard to delete one 
    if params[1] == 'add':
#### here response_obj is a variable that contains the output of "create" function , params[2] and params[3] are variables passed to create/discard as 'labid' and 'repo' respectively 
    	response_obj = create(params[2],params[3])
    elif params[1] == 'discard': 
	response_obj = discard(params[2],params[3])
#### response_gen is another function declared above
    print response_gen(response_obj)
