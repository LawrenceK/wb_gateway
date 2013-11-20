<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML, 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1-strict-dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      xmlns:py="http://purl.org/kid/ns#" py:extends="'master.kid'">

<head>
  <title py:content="label">Panel label goes here</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <link rel="stylesheet" href="/static/css/panel.css" />
  <script src="${std.tg_js}/MochiKit.js"/>
  <script src="${std.tg_js}/WebBrick.js"/>
</head>

<body header='No'>
  <table width="100%">
    <c py:replace="''">Scan through list of elements in supplied dictionary</c>
    <div py:for="elem in elems" py:strip="True">

      <div py:strip="True"
           py:if="elem.has_key('Control') and  elem['Control'].has_key('Selection')">
        <?python ctype = elem['Control']['Selection']['ctype'] ?>

        <!--                          -->
        <!-- On/Off 2-position switch -->
        <!--                          -->
        <div py:if="ctype=='Wb:SwitchOnOff'" py:strip="True">
          <td colspan="2" class="caption" py:content="label" />
          <tr>
              <td class="PushButton">On</td>
              <td class="PushButton">Off</td>
          </tr>
        </div>

        <!--                      -->
        <!-- On/Off toggle switch -->
        <!--                      -->
        <div py:if="ctype=='Wb:SwitchToggle'" py:strip="True">
          <td class="caption" py:content="label" />
          <tr py:if="ctype=='Wb:SwitchToggle'">
              <td class="PushButton">On/Off</td>
              <td class="PushButton">
                <object height="120" width="120" data="/static/images/next.svg"/>
              </td>
          </tr>
        </div>

      </div>

    </div>
  </table>
</body>

</html>
