<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.master
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/"
    py:extends="WebBrickGateway.templates.master">
    
${output_head("Childs Room Interface Example")}

<body>

${output_nav("My Room")}
  
<table>
    <colgroup span="3"></colgroup>
	<tr>
		<!-- Slider goes here -->
        <td rowspan="6" width='90px' height='440px'
			wbType="FlashButton" 
			wbSource='/wbsts/house3/AO/3'
			wbTarget=''
			title='My Heat'
			flashMovie="/static/flash/VerticalSliderHeat.swf"
			>
        </td>
		<!-- Wake goes here -->
		<td rowspan="2">
			<table>
		    <colgroup span="3" width="33%"></colgroup>
		    <tr>
		    	<td />
		    	<td class="infoBar" colspan="1"> I wake up at </td>
			    <td class="infoBar">07:30</td>
			</tr>
			</table>
		</td>
		<!-- Lightcontrol goes here -->
			<td rowspan="3" width='240px' height='240px'
				wbType="FlashButton" 
				wbSource='/wbsts/house3/AO/3'
				wbTarget='/wbcmd/house3/AA/3/'
				title='Light'
				flashMovie="/static/flash/OrnateDimmer.swf"
				>
			</td>

	</tr>  <!-- 1 -->
	<tr/>  <!-- 2 -->
	<tr>
		<td rowspan="2">
		<!-- Shower goes here -->
		 		<table>
			    	<colgroup span="3" width="33%"></colgroup>
			    	<tr>
						<td wbType="PushButton" wbLoad="loadButton()"
								wbTarget="/sendevent/childshoweryes" >
							Shower Please
						</td>
						<td wbType="PushButton" wbLoad="loadButton()"
								wbTarget="/sendevent/childshowerno" >
							No Shower
						</td>
						<td wbType="Indicator" wbLoad="loadIndicator()"
									wbSource="/eventstate/child/shower"
									stateVals="Blank,Clear"
									baseClassName="indicator">
							&nbsp;
						</td>
			    	</tr>
		 		</table>
		</td>
	</tr>  <!-- 3 -->
	<tr>
		<td class="NaN" rowspan="3">
		<!-- Decoration goes here -->
			<img width="30%" src="/static/images/Decorations/Dinosaur.png"/>
		</td>		
	</tr> <!-- 4 -->
	<tr>
		<td rowspan="2">
		<!-- I'm home goes here -->
		 		<table>
			    	<colgroup span="3" width="33%"></colgroup>
			    	<tr>
						<td wbType="PushButton" wbLoad="loadButton()"
								wbTarget="/sendevent/childhome" >
							I'm Home
						</td>
						<td wbType="PushButton" wbLoad="loadButton()"
								wbTarget="/sendevent/childaway" >
							I'm going out
						</td>
						<td wbType="Indicator" wbLoad="loadIndicator()"
									wbSource="/eventstate/child/home"
									stateVals="Away,Home"
									baseClassName="indicator">
							&nbsp;
						</td>
			    	</tr>
		 		</table>
		</td>
	</tr> <!-- 5 -->
	<tr/> <!-- 6 -->

</table>

${output_site_info_bar()}

</body>

</html>
