// $Id:

function positiveIntInputOnly(e) 
{
// returns true if 0-9 or BS hit, or can't get key value; otherwise false
  var k = -1;
  if (e && e.which) k = e.which; // NS
  else if (window.event && window.event.keyCode) k = window.event.keyCode; // IE
  return (k > -1 ? ((k > 47 && k < 58) || k == 8) : true);
}

function anyIntInputOnly(e) 
{
// returns true if 0-9, - or BS hit, or can't get key value; otherwise false
  var k = -1;
  if (e && e.which) k = e.which; // NS
  else if (window.event && window.event.keyCode) k = window.event.keyCode; // IE
  return (k > -1 ? ((k > 47 && k < 58) || k == 45 || k == 8) : true);
}

function positiveFloatInputOnly(e) 
{
// returns true if 0-9, . or BS hit, or can't get key value; otherwise false
  var k = -1;
  if (e && e.which) k = e.which; // NS
  else if (window.event && window.event.keyCode) k = window.event.keyCode; // IE
  return (k > -1 ? ((k > 47 && k < 58) || k == 46 || k == 8) : true);
}

function anyFloatInputOnly(e) 
{
// returns true if 0-9, -, . or BS hit, or can't get key value; otherwise false
  var k = -1;
  if (e && e.which) k = e.which; // NS
  else if (window.event && window.event.keyCode) k = window.event.keyCode; // IE
  return (k > -1 ? ((k > 47 && k < 58) || k == 45 || k == 46 || k == 8) : true);
}

