<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:ui="ui" 
    py:extends="'master.kid'">

${output_head( "Track List" )}

<body>
    ${output_nav("Track List")}

    <table>
        <tr><th>Select Track</th></tr>
        <tr py:for="track in videoTracks" xmlns:py="http://purl.org/kid/ns#">
            <td class='navBarSmall'>
                <a href="/mediaaccess/embed?trackId=${track}">${videoTracks[track]['title']}</a>
            </td>
        </tr>
    </table>

    ${output_site_info_bar()}

</body>

</html>

