<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python 
kid.enable_import()
import WebBrickGateway.templates.widgets_tabbed
?>

<html   xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:py="http://purl.org/kid/ns#" 
        xmlns:wb="http://id.webbrick.co.uk/"
        py:extends="WebBrickGateway.templates.widgets_tabbed">
    
    <div py:def="output_status(zone_key, css_id, zone_name)" id="${css_id}" class="tempstatus">
		<div class="controltitle">${zone_name}</div>
		<div class="statusbox">
			<table class='bluebox'>
				<tr>
					<td class='tl'></td>
					<td class='t'></td>
					<td class='tr'></td>
				</tr>
				<tr>
					<td class='l'></td>
					<td class='m'>
						<div class='statusboxcontent'>
							<div class="label1">STATUS</div>
							<div class="label2">TARGET</div>
							<div class="label3">ACTUAL</div>
							<div class="value1">
							    <wb:textDisplay 
	                                    wbSource="/eventstate/${zone_key}/state?attr=status" 
	                                    prefix="" 
	                                    postfix=""
	                                    baseClassName="status">
                                    &nbsp;
                                </wb:textDisplay>
							</div>
							<div class="value2">
							        <wb:numericDisplay 
							                wbSource="/eventstate/${zone_key}/state?attr=targetsetpoint" 
							                prefix="" 
							                format="##.#" 
							                postfix=""
							                baseClassName="value">
						                &nbsp;
					                </wb:numericDisplay>
							    &deg;C
						    </div>
							<div class="value3">
						            <wb:numericDisplay 
							                wbSource="/eventstate/${zone_key}/sensor?attr=val" 
							                prefix="" 
							                format="##.#" 
							                postfix=""
							                baseClassName="value">
						                &nbsp;
					                </wb:numericDisplay>
							    &deg;C
						    </div>
						</div>
					</td>
					<td class='r'></td>
				</tr>
				<tr>
					<td class='bl'></td>
					<td class='b'></td>
					<td class='br'></td>
				</tr>
			</table>					
		</div>
	</div>





    <div py:def="output_oil_status(css_id)" id="${css_id}" class="tempstatus">
		<div class="controltitle">Oil</div>
		<div class="statusbox">
			<table class='bluebox'>
				<tr>
					<td class='tl'></td>
					<td class='t'></td>
					<td class='tr'></td>
				</tr>
				<tr>
					<td class='l'></td>
					<td class='m'>
						<div class='statusboxcontent'>
							<div class="label1">TANK</div>
							<div class="label2">USED TODAY</div>
							<div class="label3">YTD</div>
							<div class="value1">
							        <wb:numericDisplay 
							                wbSource="/eventstate/oil/level?attr=val" 
							                prefix="" 
							                format="##.#" 
							                postfix="l"
							                baseClassName="value">
						                &nbsp;
					                </wb:numericDisplay>
							</div>
							<div class="value2">
							        <wb:numericDisplay 
							                wbSource="/eventstate/oil/used?attr=val" 
							                prefix="" 
							                format="##.#" 
							                postfix="l"
							                baseClassName="value">
						                &nbsp;
					                </wb:numericDisplay>
						    </div>
							<div class="value3">
						            <wb:numericDisplay 
							                wbSource="/eventstate/oil/ytd?attr=val" 
							                prefix="" 
							                format="##.#" 
							                postfix="l"
							                baseClassName="value">
						                &nbsp;
					                </wb:numericDisplay>
						    </div>
						</div>
					</td>
					<td class='r'></td>
				</tr>
				<tr>
					<td class='bl'></td>
					<td class='b'></td>
					<td class='br'></td>
				</tr>
			</table>					
		</div>
	</div>
	
	
	<div py:def="output_boiler_ashp_status(css_id, hs_key, hs_name, hs_number)" id="${css_id}" class="tempstatus">
		<div class="controltitle" style="font-size: 18px">Current Status
		</div>
		<div class="statusbox">
			<table class='bluebox'>
				<tr>
					<td class='tl'></td>
					<td class='t'></td>
					<td class='tr'></td>
				</tr>
				<tr>
					<td class='l'></td>
					<td class='m'>
						<div class='statusboxcontent'>
							<div class="label1">AVAILABLE</div>
							<div class="label2">RUNNING</div>
							<div class="label3">FAULT    </div>
							<div class="value1">
							        <wb:textDisplay 
							                wbSource="/eventstate/heatsource/${hs_key}/availability?attr=string" 
							                prefix="" 
							                baseClassName="hs_status">
						                &nbsp;
					                </wb:textDisplay>
							</div>
							<div class="value2">
							        <wb:textDisplay 
							                wbSource="/eventstate/heatsource/${hs_key}/running?attr=string" 
							                prefix="" 
							                baseClassName="hs_status">
						                &nbsp;
					                </wb:textDisplay>
						    </div>
							<div class="value3">
						            <wb:textDisplay 
							                wbSource="/eventstate/${hs_name}/${hs_number}/alarm?attr=string" 
							                prefix="" 
							                baseClassName="hs_status">
						                &nbsp;
					                </wb:textDisplay>
						    </div>
						</div>
					</td>
					<td class='r'></td>
				</tr>
				<tr>
					<td class='bl'></td>
					<td class='b'></td>
					<td class='br'></td>
				</tr>
			</table>					
		</div>
	</div>

    
</html>
