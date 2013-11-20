<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/" 
    py:extends="'master.kid', 'embedschedule.kid'">

${output_head( "Schedule" )}

<body>

    ${output_nav(scheduleName)}

    <div width="50%">
        ${output_schedule(scheduleName)}
    </div>
</body>

<script language="javascript">
    pollerInterval = 10.0;
    pollerSoonDelay = 2.0;
</script>

</html>
