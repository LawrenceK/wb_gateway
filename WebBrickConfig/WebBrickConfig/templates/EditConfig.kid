<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?python
from WebBrickLibs import WbDefs

def bit(val, mask):
    return (val & mask) != 0

def bitN(val, bn):
    return bit(val, 1<<bn)

def selectAttr(val, item, old={}):
    new = old.copy()
    new.update({ "selected": (val==item and "selected") or None })
    return new

def checkedAttr(val, old={}):
    new = old.copy()
    new.update({ "checked": (val and "checked") or None })
    return new

def checkboxAttr(val, item):
    return { "type":    "checkbox"
           , "id":      val
           , "name":    val
           , "value":   val
           , "checked": (item and "checked") or None }

def mkList(vals):
    return "(" + ",".join(vals) + ")"

def dinOptionsStr(din):
    opts     = din["options"]
    optnames = ["Rise", "Fall", "0x04", "0x08", "0x10", "0x20", "0x40", "0x80"]
    return mkList( [ optnames[i] for i in range (8) if bitN(opts, i) ] )

def triggerStr(trg):
    action = trg["actionNr"]
    if action == WbDefs.AT_NONE:      return "None"
    if action == WbDefs.AT_OFF:       return "Off " + triggerTgt(trg)
    if action == WbDefs.AT_ON:        return "On "  + triggerTgt(trg)
    if action == WbDefs.AT_TOGGLE:    return "Tog " + triggerTgt(trg)
    if action == WbDefs.AT_DWELL:     return "Dw%u "%(trg["dwell"]) + triggerTgt(trg)
    if action == WbDefs.AT_DWELLCAN:  return "Dc%u "%(trg["dwell"]) + triggerTgt(trg)
    if action == WbDefs.AT_NEXT:      return "Nxt " + triggerStp(trg)
    if action == WbDefs.AT_PREV:      return "Prv " + triggerStp(trg)
    return "?act %i"%(action)

def triggerTgt(trg):
    tgtype = trg["typeNr"]
    fmt    = "??%u"
    if tgtype == WbDefs.TT_DIGITAL:   fmt = "D%u"
    if tgtype == WbDefs.TT_ANALOGUE:  fmt = "A%u"
    if tgtype == WbDefs.TT_SCENE:     fmt = "S%u"
    return fmt%(trg["pairChn"])

def triggerStp(trg):
    tgtype = trg["typeNr"]
    fmt    = "??%u"
    if tgtype == WbDefs.TT_ANALOGUE:  fmt = "A%u"
    if tgtype == WbDefs.TT_SCENE:     fmt = "Scene"
    return fmt%(trg["pairChn"])

def triggerActionVal(trg):
    actnum = trg["actionNr"]
    if trg["typeNr"] == WbDefs.TT_SCENE:
        if actnum == WbDefs.AT_NEXT: return WbDefs.AT_NEXTSCENE
        if actnum == WbDefs.AT_PREV: return WbDefs.AT_PREVSCENE
    return actnum

def pairList(num):
    return [ (i,i) for i in range(num) ]

triggerActions = ( ( WbDefs.AT_OFF       , "Off"    )
                 , ( WbDefs.AT_ON        , "On"     )
                 , ( WbDefs.AT_TOGGLE    , "Toggle" )
                 , ( WbDefs.AT_DWELL     , "Dwell"  )
                 , ( WbDefs.AT_DWELLCAN  , "Dwell-cancel" )
                 , ( WbDefs.AT_NEXT      , "Next" )
                 , ( WbDefs.AT_NEXTSCENE , "Next scene" )
                 , ( WbDefs.AT_PREV      , "Previous" )
                 , ( WbDefs.AT_PREVSCENE , "Previous scene" )
                 )

sceneDigitalOpts = ( ( True,  "On"  )
                   , ( False, "Off" )
                   , ( None,  "--" )
                   )

sceneAnalogOpts = ( ( 0,    "Set 0" )
                  , ( 1,    "Set 1" )
                  , ( 2,    "Set 2" )
                  , ( 3,    "Set 3" )
                  , ( 4,    "Set 4" )
                  , ( 5,    "Set 5" )
                  , ( 6,    "Set 6" )
                  , ( 7,    "Set 7" )
                  , ( None, "--" )
                  )

def sceneDigital(sd):
    def dflag(j):
        dval = sd["Digital"][j]
        if dval == True:  return "1"
        if dval == False: return "0"
        return "-"
    return "D:"+"".join([dflag(j) for j in range(WbDefs.DOCOUNT)])

def sceneAnalog(sa):
    def aflag(j):
        aval = sa["Analog"][j]
        return (isinstance(aval,int) and str(aval)) or "-"
    return "A:("+",".join([aflag(j) for j in range(WbDefs.AOCOUNT)])+")"

def scheduleDays(sch):
    daylist = "SMTWTFS"
    days    = sch["days"]
    return "".join([((bitN(days,j)) and daylist[j]) or "-" for j in range(7)])

def scheduleTime(sch):
    return "%02u:%02u"%(sch["hours"],sch["mins"])
?>

<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:py="http://purl.org/kid/ns#">

<head>
  <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
  <title>WebBrick Configuration Editor</title>
  <!-- 
  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
  -->
  <!-- 
  -->
  <script src="/static/javascript/MochiKit.js"></script>
  <script src="/static/javascript/WebBrick.js"></script>
  <script src="/static/javascript/EditConfig.js"></script>
  <!-- For local testing:
  <script src="../resources/static/javascript/MochiKit.js"></script>
  <script src="../resources/static/javascript/WebBrick.js"></script>
  <script src="../resources/static/javascript/EditConfig.js"></script>
  -->
</head>

<!--
    Note: all event handlers are invoked via MochiKit's Signal module.
    File WebBrick.js invokes the initial window.onload handler that scans
    the entire DOM looking for wbLoad attributes and calling the corresponding 
    functions when the page has been loaded.

    DO NOT specify an onload handler on the <body> element.
-->

<body>

  <select py:def="selectWidget(idbase, idx, optiter, curval, size)"
          id="${idbase}_${idx}" name="${idbase}_${idx}" size="${size}"  >
    <option py:for="val,txt in optiter"
            py:attrs='selectAttr(val,curval,{"value": str(val)})'
            py:content="txt" />
  </select>

  <tr py:def="triggerEdit(legend, idbase, idx, trig)">
    <td py:content="legend">Trigger action:
    </td>
    <td>
      <select py:replace='selectWidget(idbase+"Action", idx, triggerActions, triggerActionVal(trig), 1)' />
    </td>
    <td>
      <span>Dwell
        <select py:replace='selectWidget(idbase+"Dwell", idx, pairList(8), trig["dwell"], 1)' />
      </span>
      <span>Dig. out
        <select py:replace='selectWidget(idbase+"DO", idx, pairList(8), trig["pairChn"], 1)' />
      </span>
      <span>An. out
        <select py:replace='selectWidget(idbase+"AO", idx, pairList(4), trig["pairChn"], 1)' />
      </span>
      <span>Set point
        <select py:replace='selectWidget(idbase+"SetP", idx, pairList(8), trig["pairChn"], 1)' />
      </span>
      <span>Scene
        <select py:replace='selectWidget(idbase+"Scene", idx, pairList(8), trig["pairChn"], 1)' />
      </span>
    </td>
  </tr>

<!--
tr.callout {
  display: none ;
  }
-->

<!-- Constructed using http://www.somacon.com/p141.php -->

<style type="text/css">
.Message { text-align: left; color: blue; }
.Error   { text-align: left; color: red; }
.Hide    { display: none; }
.ItemNum { font-weight: bold; }
.Spacing { font-weight: bold; color: white; }

table.config {
  width: 100%;
  border-width: 2px 2px 2px 2px;
  /* border-width: 0px 0px 0px 0px; */
  border-spacing: 2px;
  border-style: outset outset outset outset;
  border-color: gray gray gray gray;
  border-collapse: separate;
  background-color: white;
  }
table.config th {
  border-width: 0px 0px 0px 0px;
  padding: 2px 2px 2px 2px;
  border-style: inset inset inset inset;
  border-color: gray gray gray gray;
  background-color: white;
  vertical-align: top;
  font-family: sans-serif;
  font-size: large;
  }
table.config td {
  border-width: 0px 0px 0px 0px;
  padding: 2px 2px 2px 2px;
  border-style: inset inset inset inset;
  border-color: gray gray gray gray;
  background-color: white;
  vertical-align: top;
  }

table.callout {
  border-width: 2px 2px 2px 2px;
  border-spacing: 2px;
  border-style: outset outset outset outset;
  border-color: gray gray gray gray;
  border-collapse: separate;
  background-color: rgb(240, 240, 240);
  }
table.callout th {
  border-width: 0px 0px 0px 0px;
  padding: 2px 2px 2px 2px;
  border-style: inset inset inset inset;
  border-color: gray gray gray gray;
  background-color: rgb(240, 240, 240);
  vertical-align: top;
  }
table.callout td {
  border-width: 0px 0px 0px 0px;
  padding: 2px 2px 2px 2px;
  border-style: inset inset inset inset;
  border-color: gray gray gray gray;
  background-color: rgb(240, 240, 240);
  vertical-align: top;
  }

</style>

<form name="ConfigEdit" action="/wbcnf/ConfigEdit" method="post">

<h3>WebBrick configuration</h3>

<table class="config">
<tbody>
<!-- <th colspan="5">WebBrick general configuration</th> -->
<tr>
  <td wbLoad="loadNoCallout()">
    Node number
  </td>
  <td wbLoad="loadNoCallout()">
    <input type="text" size="4" maxlength="4"
           id="WbNode" name="WbNode" value="${WbCnf.getNodeNumberStr()}" />
  </td>
  <td wbLoad="loadNoCallout()">
    Name
    <input type="text" size="12" maxlength="12"
           id="WbName" name="WbName" value="${WbCnf.getNodeName()}" />
  </td>
  <td wbLoad="loadNoCallout()">
    IP address
    <input type="text" size="15" maxlength="15"
           id="WbIpAddr" name="WbIpAddr" value="${WbCnf.getIpAddress()}" />
  </td>
  <td wbLoad="loadNoCallout()">
    MAC address
    <input type="text" size="17" maxlength="17"
           id="WbMacAddr" name="WbMacAddr" value="${WbCnf.getMacAddress()}" />
  </td>
</tr>

<tr>
  <td wbLoad="loadNoCallout()">
    Infrared address
  </td>
  <td wbLoad="loadNoCallout()">
    <input type="text" size="4" maxlength="4"
           id="WbIrAddr" name="WbIrAddr" value="${WbCnf.getIrAddress()}" />
  </td>
  <td wbLoad="loadNoCallout()">
    <input type="checkbox" id="WbIrRecv" name="WbIrOpts" value="Receive" 
           py:attrs="checkedAttr(WbCnf.getIrReceive())" />
    Enable IR receive
  </td>
  <td wbLoad="loadNoCallout()">
    <input type="checkbox" id="WbIrSend" name="WbIrOpts" value="Send"
           py:attrs="checkedAttr(WbCnf.getIrTransmit())" />
    Enable IR transmit
  </td>
  <td wbLoad="loadNoCallout()">
  </td>
</tr>

<tr>
  <td>
    Fade rate
  </td>
  <td wbLoad="loadNoCallout()">
    <input type="text" size="4" maxlength="4"
           id="WbFadeRate" name="WbFadeRate" value="${WbCnf.getFadeRateStr()}" />
  </td>
  <td wbLoad="loadNoCallout()">
    Mimic low level
    <input type="text" size="4" maxlength="4"
           id="WbMimicLoLevel" name="WbMimicLoLevel" value="${WbCnf.getMimicLoLevelStr()}" />
  </td>
  <td wbLoad="loadNoCallout()">
    Mimic high level
    <input type="text" size="4" maxlength="4"
           id="WbMimicHiLevel" name="WbMimicHiLevel" value="${WbCnf.getMimicHiLevelStr()}" />
  </td>
  <td wbLoad="loadNoCallout()">
    Mimic fade rate
    <input type="text" size="4" maxlength="4"
           id="WbMimicFadeRate" name="WbMimicFadeRate" value="${WbCnf.getMimicFadeRateStr()}" />
  </td>
</tr>
</tbody>
</table>

<!-- I/O, scene and schedule configuration -->

<table class="config">
<tbody>

<!--
<tr>
  <th colspan="9">I/O configuration</th>
</tr>
-->

<!-- Digital Outputs -->

<tr>
  <td wbLoad="loadNoCallout()">Digital outputs
  </td>
  <td py:for="i in range(WbDefs.DOCOUNT)" wbLoad="loadDOCallout(${i})">
    <span class="ItemNum">${i}</span>
    <input type="text" size="10" maxlength="10"
           id="WbDOName_${i}" name="WbDOName_${i}" value="${WbCnf.getDigOutName(i)}" />
  </td>
</tr>

<tr py:for="i in range(WbDefs.DOCOUNT)"
    id="DOCallout_${i}" class="callout" wbLoad="registerCallout()" >
  <td wbLoad="loadNoCallout()">
  </td>
  <td colspan="8">
    <table class="callout">
    <tbody>
    <tr>
      <td colspan="2">
        <h4>Digital output: ${i}</h4>
      </td>
    </tr>
    <tr>
      <td>
        Name:
      </td>
      <td>
        <input type="text" size="10" maxlength="10"
               id="WbDOName_${i}" name="WbDOName_${i}" value="${WbCnf.getDigOutName(i)}" />
      </td>
      <td>
        <span>Mimic
          <select id="WbDOMimic_${i}" name="WbDOMimic_${i}" size="1">
            <option py:content='"None"'
                    py:attrs='selectAttr(-1,WbCnf.getDigOutMimic(i))' />
            <option py:for='j in range(8)'
                    py:content='str(j)'
                    py:attrs='selectAttr(j,WbCnf.getDigOutMimic(i))' />
          </select>
        </span>
      </td>
    </tr>
    </tbody>
    </table>
  </td>
</tr>

<!-- Digital Outputs (end) -->

<!-- Analog Outputs -->

<tr>
  <td wbLoad="loadNoCallout()">Analog outputs
  </td>
  <td py:for="i in range(WbDefs.AOCOUNT)" wbLoad="loadAOCallout(${i})">
    <span class="ItemNum">${i}</span>
    <input type="text" size="10" maxlength="10"
           id="WbAOName_${i}" name="WbAOName_${i}" value="${WbCnf.getAnalogOutName(i)}" />
  </td>
</tr>

<tr py:for="i in range(WbDefs.AOCOUNT)"
    id="AOCallout_${i}" class="callout" wbLoad="registerCallout()" >
  <td wbLoad="loadNoCallout()">
  </td>
  <td colspan="8">
    <table class="callout">
    <tbody>

    <tr>
      <td colspan="2">
        <h4>Analog output: ${i}</h4>
      </td>
    </tr>

    <tr>
      <td>
        Name:
      </td>
      <td>
        <input type="text" size="10" maxlength="10"
               id="WbAOName_${i}" name="WbAOName_${i}" value="${WbCnf.getAnalogOutName(i)}" />
      </td>
      <td>
        <span>Mimic
          <select id="WbAOMimic_${i}" name="WbAOMimic_${i}" size="1">
            <option py:content='"None"'
                    py:attrs='selectAttr(-1,WbCnf.getAnalogOutMimic(i))' />
            <option py:for='j in range(8)'
                    py:content='str(j)'
                    py:attrs='selectAttr(j,WbCnf.getAnalogOutMimic(i))' />
          </select>
        </span>
      </td>
    </tr>
    </tbody>
    </table>
  </td>
</tr>

<!-- Analog Outputs (end) -->

<!-- Digital inputs -->

<tr py:for="h in range(0, WbDefs.DICOUNT, 8)">
  <td wbLoad="loadNoCallout()">
    <span py:if="h==0" py:strip="">Digital<br/>inputs</span>
  </td>
  <td py:for="i in range(h, min(WbDefs.DICOUNT,h+8))" 
      wbLoad="loadDICallout(${i})">
    <span class="ItemNum">${i}</span>
    <input type="text" size="10" maxlength="10" readonly="True"
           id='WbDIName_${i}' name='WbDIName_${i}' value='${WbCnf.getDigInName(i)}' />
    <br/>
    <span class="Spacing">${i}</span>${dinOptionsStr(WbCnf.getDigInTrigger(i))}<br/>
    <span class="Spacing">${i}</span>${triggerStr(WbCnf.getDigInTrigger(i))}
  </td>
</tr>

<tr py:for="i in range(WbDefs.DICOUNT)"
    id="DICallout_${i}" class="callout" wbLoad="registerCallout()" >
  <td wbLoad="loadNoCallout()">
  </td>
  <td colspan="8">
    <table class="callout">
    <tbody>
    <tr>
      <td colspan="2">
        <h4>Digital input: ${i}</h4>
      </td>
    </tr>
    <tr>
      <td>
        Name:
      </td>
      <td>
        <input type="text" size="10" maxlength="10"
               id='WbDIName_${i}' name='WbDIName_${i}' 
               value='${WbCnf.getDigInName(i)}' />
      </td>
    </tr>
    <tr py:replace='triggerEdit("Trigger action:", "WbDI", i, WbCnf.getDigInTrigger(i))' />
    <tr>
      <td>
        Options:
      </td>
      <td>
        <input py:attrs='checkboxAttr( "WbDIRise_"+str(i), bitN(WbCnf.getDigInTrigger(i)["options"], 1))'/>
        Rising edge trigger
      </td>
      <td>
        <input py:attrs='checkboxAttr( "WbDIFall_"+str(i), bitN(WbCnf.getDigInTrigger(i)["options"], 2))'/>
        Falling edge trigger
      </td>
    </tr>
    </tbody>
    </table>
  </td>
</tr>

<!-- Digital inputs (end) -->

<!-- Analog inputs -->

<tr>
  <td wbLoad="loadNoCallout()">Analog<br/>inputs
  </td>
  <td py:for='i in range(WbDefs.AICOUNT)' wbLoad='loadAICallout(${i})'>
    <span class="ItemNum">${i}</span>
    <input type="text" size="10" maxlength="10" readonly="True"
           id="WbAIName_${i}" name="WbAIName_${i}" value='${WbCnf.getAnalogInName(i)}' />
    <br/>
    <span class="Spacing">${i}</span>L:${triggerStr(WbCnf.getAnalogTriggerLow(i))}
    <br/>
    <span class="Spacing">${i}</span>H:${triggerStr(WbCnf.getAnalogTriggerHigh(i))}
  </td>
</tr>

<tr py:for='i in range(WbDefs.AICOUNT)'
    id="AICallout_${i}" class="callout" wbLoad="registerCallout()">
  <td wbLoad="loadNoCallout()">
  </td>
  <td colspan="8">
    <table class="callout">
    <tbody>
    <tr>
      <td colspan="2">
        <h4>Analog input: ${i}</h4>
      </td>
    </tr>
    <tr>
      <td>
        Name:
      </td>
      <td>
        <input type="text" size="10" maxlength="10"
               id='WbDIName_${i}' name='WbDIName_${i}' value='${WbCnf.getAnalogInName(i)}' />
      </td>
    </tr>
    <tr py:replace='triggerEdit("Low trigger:",  "WbAL", i, WbCnf.getAnalogTriggerLow(i))'  />
    <tr py:replace='triggerEdit("High trigger:", "WbAH", i, WbCnf.getAnalogTriggerHigh(i))' />
    </tbody>
    </table>
  </td>
</tr>

<!-- Analog inputs (end) -->

<!-- Temperature inputs -->

<tr>
  <td wbLoad="loadNoCallout()">Temperature<br/>inputs
  </td>
  <td py:for='i in range(WbDefs.TEMPCOUNT)' wbLoad="loadTICallout(${i})">
    <span class="ItemNum">${i}</span>
    <input type="text" size="10" maxlength="10" readonly="True"
           id="WbTIName_${i}" name="WbTIName_${i}" value='${WbCnf.getTempInName(i)}' />
    <br/>
    <span class="Spacing">${i}</span>L:${triggerStr(WbCnf.getTempTriggerLow(i))}
    <br/>
    <span class="Spacing">${i}</span>H:${triggerStr(WbCnf.getTempTriggerHigh(i))}
  </td>
</tr>

<tr py:for='i in range(WbDefs.TEMPCOUNT)'
    id="TICallout_${i}" class="callout" wbLoad="registerCallout()">
  <td wbLoad="loadNoCallout()">
  </td>
  <td colspan="8">
    <table class="callout">
    <tbody>
    <tr>
      <td colspan="2">
        <h4>Temperature input: ${i}</h4>
      </td>
    </tr>
    <tr>
      <td>
        Name:
      </td>
      <td>
        <input type="text" size="10" maxlength="10"
               id="WbTIName_${i}" name="WbTIName_${i}" value='${WbCnf.getTempInName(i)}' />
      </td>
    </tr>
    <tr py:replace='triggerEdit("Low trigger:",  "WbTL", i, WbCnf.getTempTriggerLow(i))'  />
    <tr py:replace='triggerEdit("High trigger:", "WbTH", i, WbCnf.getTempTriggerHigh(i))' />
    </tbody>
    </table>
  </td>
</tr>

<!-- Temperature inputs (end) -->

<!-- Set points -->

<tr>
  <td wbLoad="loadNoCallout()">Set points
  </td>
  <td py:for='i in range(WbDefs.SPCOUNT)' wbLoad="loadNoCallout()">
    <span class="ItemNum">${i}</span>
    <input type="text" size="4" maxlength="4"
           id="WbSetPoint_${i}" name="WbSetPoint_${i}" value='${WbCnf.getSetPoint(i)}' />
  </td>
</tr>

<!-- Set points (end) -->

<!-- Dwells -->

<tr>
  <td wbLoad="loadNoCallout()">Dwells
  </td>
  <td py:for='i in range(WbDefs.DWELLCOUNT)' wbLoad="loadNoCallout()">
    <span class="ItemNum">${i}</span>
    <input type="text" size="4" maxlength="4"
           id="WbDwell_${i}" name="WbDwell_${i}" value='${WbCnf.getDwellStr(i)}' />
  </td>
</tr>

<!-- Dwells (end) -->

<!-- Rotary encoders -->

<tr wbLoad="loadNoCallout()">
  <td wbLoad="loadNoCallout()">Rotary encoders
  </td>
  <td py:for='i in range(WbDefs.ROTARYCOUNT)' wbLoad="loadNoCallout()">
    <span class="ItemNum">${i}</span>
    <input type="text" size="4" maxlength="4"
           id="WbREncode_${i}" name="WbREncode_${i}" value='${WbCnf.getRotary(i)}' />
  </td>
</tr>

<!-- Rotary encoders (end) -->

<!-- Scenes -->

<tr py:for='h in range(0, WbDefs.SCENECOUNT, 8)'>
  <td wbLoad="loadNoCallout()">
    <span py:if='h==0' py:strip="">Scenes</span>
  </td>
  <td py:for='i in range(h, min(WbDefs.SCENECOUNT,h+8))' wbLoad="loadSceneCallout(${i})">
    <span class="ItemNum">${i}</span>&nbsp;${sceneDigital(WbCnf.getSceneAlt(i))}<br/>
    <span class="Spacing">${i}</span>&nbsp;${sceneAnalog(WbCnf.getSceneAlt(i))}
  </td>
</tr>

<tr py:for='i in range(WbDefs.SCENECOUNT)'
    id="SceneCallout_${i}" class="callout" wbLoad="registerCallout()">
  <td wbLoad="loadNoCallout()">
  </td>
  <td colspan="8">
    <table class="callout">
    <tbody>
    <tr>
      <td colspan="2">
        <h4>Scene: ${i}</h4>
      </td>
    </tr>
    <tr>
      <td>Digital outputs:
      </td>
      <td py:for='j in range(WbDefs.DOCOUNT)'>${j}:
        <select py:replace='selectWidget("WbSceneDO_"+str(i), j, sceneDigitalOpts, WbCnf.getSceneAlt(i)["Digital"][j], 1)' />
      </td>
    </tr>
    <tr>
      <td>Analog outputs:
      </td>
      <td py:for='j in range(WbDefs.AOCOUNT)'>${j}:
        <select py:replace='selectWidget("WbSceneAO_"+str(i), j, sceneAnalogOpts, WbCnf.getSceneAlt(i)["Analog"][j], 1)' />
      </td>
    </tr>
    </tbody>
    </table>
  </td>
</tr>

<!-- Scenes (end) -->

<!-- Schedules -->

<tr py:for='h in range(0, WbDefs.SCHEDCOUNT, 8)'>
  <td wbLoad="loadNoCallout()">
    <span py:if='h==0' py:strip="">Schedules</span>
  </td>
  <td py:for='i in range(h, min(WbDefs.SCHEDCOUNT,h+8))' wbLoad="loadScheduleCallout(${i})">
    <span class="ItemNum">${i}</span>&nbsp;${scheduleDays(WbCnf.getScheduledEvent(i))}<br/>
    <span class="Spacing">${i}</span>${scheduleTime(WbCnf.getScheduledEvent(i))}<br/>
    <span class="Spacing">${i}</span>${triggerStr(WbCnf.getScheduledEvent(i))}
  </td>
</tr>

<tr py:for='i in range(WbDefs.SCHEDCOUNT)' 
    id="ScheduleCallout_${i}" class="callout" wbLoad="registerCallout()">
  <td wbLoad="loadNoCallout()">
  </td>
  <td colspan="8">
    <table class="callout">
    <tbody>
    <tr>
      <td colspan="2">
        <h4>Schedule: ${i}</h4>
      </td>
    </tr>
    <tr>
      <td>
        Time (hh:mm):
      </td>
      <td>
        <input type="text" size="5" maxlength="5"
               id="WbScheduleTime_${i}" name="WbScheduleTime_${i}" 
               value="${scheduleTime(WbCnf.getScheduledEvent(i))}" />
      </td>
      <td>
        <input py:attrs='checkboxAttr( "WbScheduleSun_"+str(i), bitN(WbCnf.getScheduledEvent(i)["days"], 1))' />
        Sun,
        <input py:attrs='checkboxAttr( "WbScheduleMon_"+str(i), bitN(WbCnf.getScheduledEvent(i)["days"], 2))' />
        Mon,
        <input py:attrs='checkboxAttr( "WbScheduleTue_"+str(i), bitN(WbCnf.getScheduledEvent(i)["days"], 3))' />
        Tue,
        <input py:attrs='checkboxAttr( "WbScheduleWed_"+str(i), bitN(WbCnf.getScheduledEvent(i)["days"], 4))' />
        Wed,
        <input py:attrs='checkboxAttr( "WbScheduleThu_"+str(i), bitN(WbCnf.getScheduledEvent(i)["days"], 5))' />
        Thu,
        <input py:attrs='checkboxAttr( "WbScheduleFri_"+str(i), bitN(WbCnf.getScheduledEvent(i)["days"], 6))' />
        Fri,
        <input py:attrs='checkboxAttr( "WbScheduleSat_"+str(i), bitN(WbCnf.getScheduledEvent(i)["days"], 7))' />
        Sat
      </td>
    </tr>
    <tr py:replace='triggerEdit("Trigger action:", "WbScheduleAction", i, WbCnf.getScheduledEvent(i))' />
    </tbody>
    </table>
  </td>
</tr>

<!-- Schedules (end) -->

</tbody>
</table>

</form>

<h2 class="Message" id="Message"></h2>

</body>
</html>
