# !/bin/sh
#
# $Id: RunCITests.sh 3631 2010-04-19 08:30:38Z philipp.schuster $
#
# Run WebBrick continuous integration tests
#
# (Currently, runs a single unit test suite - later will pick up details of tests to
# run from a conf.d subdirectory.)
#
#
HG_REPOSITORY=https://svn2.hosted-projects.com/webbrick/WebBrick/HomeGateway2/Trunk
HG_WORKINGCOPY=/opt/webbrick/ci/HomeGateway2/
ERR_LOG=/var/log/webbrick/ci/RunCITests.log
ERR_SEEN=0
#
#remove logfiles
rm -f /var/log/webbrick/ci/*
#
# Arguments:
#  --checkout   new checkout from repository
#  --update     update from repository (default)
#  --run-never  never run tests
#  --run-always always run tests
#  --run-change run tests if repository has changed (default)
#  --config=nam configuration file name (default CITests.conf)
#  --sync       resyncronize the repository mirrors before updating
#               the local working copy
#
FRESH_CHECKOUT=0
SYNC_MIRROR=0
RUNTESTS=changed
TESTCONFIG=/opt/webbrick/ci/HomeGateway2/CITests.conf
for p in $@
do
    if   [[ "$p" =~ "^--ch" ]];     then FRESH_CHECKOUT=1
    elif [[ "$p" =~ "^--up" ]];     then FRESH_CHECKOUT=0
    elif [[ "$p" =~ "^--run-n" ]];  then RUNTESTS=never
    elif [[ "$p" =~ "^--run-a" ]];  then RUNTESTS=always
    elif [[ "$p" =~ "^--run-c" ]];  then RUNTESTS=changed
    elif [[ "$p" =~ "^--sync" ]];   then SYNC_MIRROR=1
    elif [[ "$p" =~ "^--conf" ]];   then TESTCONFIG=${p#--conf*=}
    else
       echo "RunCITests - unrecogniozed option $p"
       echo ""
       echo "usage: RunCITets.sh optionss"
       echo "where options are:"
       echo "  --checkout   new checkout from repository"
       echo "  --update     update from repository (default)"
       echo "  --run-never  never run tests"
       echo "  --run-always always run tests"
       echo "  --run-change run tests if repository has changed (default)"
       echo "  --sync       resyncronize the repository mirrors before updating"
       echo "  --config=nam configuration file name (default CITests.conf)"
       echo ""
       exit 1
    fi
done

echo "RunCITests - Started: " `date` >$ERR_LOG
pushd /opt/webbrick/ci/ >>$ERR_LOG

RUN=0
if [[ "$RUNTESTS" = "always" ]]; then RUN=1; fi

# Bring hosted-projects and local repository mirrors up to date befor checkout

if (( SYNC_MIRROR )); then
    ssh -i /root/.ssh/ci_svn_dsa ci@webbricksystems-svn sudo /var/svk/MirrorRepository.sh next >>$ERR_LOG
fi

# Checkout new working copy - remove old working copy first
if (( FRESH_CHECKOUT )); then
  rm -rf $HG_WORKINGCOPY
  svn checkout $HG_REPOSITORY $HG_WORKINGCOPY >>$ERR_LOG
  RUN=1
# Update existing copy 
else
  OLDREV=`svn info /var/WebBrickCI/HomeGateway2/ | grep "^Revision: "`
  svn update $HG_WORKINGCOPY >>$ERR_LOG
  NEWREV=`svn info /var/WebBrickCI/HomeGateway2/ | grep "^Revision: "`
  if [[ "$OLDREV" != "$NEWREV" && "$RUNTESTS" = "changed" ]]; then RUN=1; fi
fi

# Run tests

# for each entry in config file

ERR_SEEN=0

if (( RUN )); then
    if [ -e "$TESTCONFIG" ]; then
        # dos2unix -o $TESTCONFIG   # May need this if conf file has <CRLF>
        # cat $TESTCONFIG | while read DIR CMD  # '|' creates new subshell scope for loop
        while read DIR CMD                      # NOTE '< $TESTCONFIG' below
        do
            if [[ "$DIR" != "#" && "$DIR" != "" ]]; then
                pushd $DIR >>$ERR_LOG
                $CMD 2>&1 >>$ERR_LOG
                ExitStatus=$?
                popd >>$ERR_LOG
                if (( ExitStatus != 0 )); then
                   let ERR_SEEN=ERR_SEEN+1
                   echo "RunCITests - Fail: Dir $DIR, command $CMD, errs $ERR_SEEN" >>$ERR_LOG
                   echo "Fail: Dir $DIR, command $CMD" >>$ERR_LOG
                else
                   echo "Pass: Dir $DIR, command $CMD" >>$ERR_LOG
                fi
            fi    
        done < $TESTCONFIG
    else
       echo "RunCITests - Configuration file '$TESTCONFIG' does not exist"
    fi
fi

echo "RunCITests - all tests run, errors seen: $ERR_SEEN" >>$ERR_LOG

# If error seen, send message to webbrick alias

if (( ERR_SEEN > 0 )); then
   tar -czf logs/logs.tgz logs/*
   uuencode logs/logs.tgz >> $ERR_LOG 
   EMAILSUBJ="WebBrickDev - RunCITests failure `date`"
   EMAILADDR="philipp.schuster@webbricksystems.com"
   /bin/mail -s "$EMAILSUBJ" "$EMAILADDR" < $ERR_LOG
else
    # Create new eggs
fi

# Restore original working directory

popd >>$ERR_LOG

# End.
