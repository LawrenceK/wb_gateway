<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
      xmlns:py="http://purl.org/kid/ns#" 
      xmlns:wb="http://id.webbrick.co.uk/">

<?python
if tg.useragent.browser in ['msie', 'firefox']:
    javascript = 'yes'
else:
    javascript = 'no'
?>

<td py:if="javascript == 'yes' and item.tag=='{http://id.webbrick.co.uk/}simpleLink'" 
            onClick="window.location=&apos;${item.get('target')}&apos;" 
            class="navBarSmall" 
            width="${item.get('width')}"
            >
    ${item.text}
    ${item.getchildren()}
</td>

<td py:if="javascript == 'yes' and item.tag=='{http://id.webbrick.co.uk/}textDisplay'" 
            wbType="Text" 
            wbLoad='loadTextDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("postfix")}&apos;)'
            wbSource="${item.get('wbSource')}"
            width="${item.get('width')}"
            >
    ${item.text}
    ${item.getchildren()}
</td>

<td py:if="javascript == 'yes' and item.tag=='{http://id.webbrick.co.uk/}numericDisplay'" 
            wbType="Numeric" 
            wbLoad='loadNumericDisplay(&apos;${item.get("prefix")}&apos;,&apos;${item.get("format")}&apos;,&apos;${item.get("postfix")}&apos;)'
            wbSource="${item.get('wbSource')}"
            width="${item.get('width')}"
            >
    ${item.text}
    ${item.getchildren()}
</td>

</html>
