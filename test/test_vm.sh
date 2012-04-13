#!/bin/bash
#
# Test vm machines
#
# prerequisite 2 vm-container already up and running
#
# no virtual compute already installed
#
# maxrun time 2 hours

function reportError {
	echo $1
	exit -1
}


function Pause {
	echo $1 and press any key to continue execution
	OLDCONFIG=`stty -g`
	stty -icanon -echo min 1 time 0
	dd count=1 2>/dev/null
	stty $OLDCONFIG
}


echo Creating a compute node and installing it...
rocks add host vm vm-container-0-0 compute
rocks start host vm compute-0-0-0
sleep 120
ping -c 1 -q compute-0-0-0
if [ $? != "0" ]; then
	reportError("problem when starting up compute-0-0-0")
fi
test=1
while [ $test != "0" ];do 
	ssh compute-0-0-0 "echo 2>&1"
	test=$?
done

echo Testing pause on virtual compute node
rocks pause host vm compute-0-0-0
ssh compute-0-0-0 "echo 2>&1" && reportError("VM did not pause")
rocks resume host vm compute-0-0-0
ssh compute-0-0-0 "echo 2>&1" || reportError("VM did not resume")

echo Testing moving virtual compute node
rocks move host vm compute-0-0-0 vm-container-0-1
ssh compute-0-0-0 "echo 2>&1" || reportError("VM was not migrated properly")

echo Testing cluster
rocks add cluster 137.110.119.101 2
rocks start host vm frontend-0-0-0

echo Starting frontend 
rocks create keys key=private.key passphrase=no > pubblic.key
rocks add host key frontend-0-0-0 key=public.key
rocks open host console frontend-0-0-0 key=private.key

Pause "Install frontend and when installation it's over "

echo Starting virtual frontend 
rocks start host vm frontend-0-0-0
Pause "Start insert-ether on the new frontend and "
echo Starting virtual compute nodes
rocks start host vm hosted-vm-0-0-0
sleep 60
rocks start host vm hosted-vm-0-1-0


