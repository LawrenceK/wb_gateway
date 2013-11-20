/*
 *	Utility functions for FORM testing
 *  and getting command line params
 */

function clearDropDownList(dropDownList)
{
  var intTotalItems= dropDownList.options.length;
  for(var intCounter=intTotalItems;intCounter>=0;intCounter--)
 {
     dropDownList.remove(intCounter);
 }
}
 
 
function addDropDownListItem(dropDownList,value,Text)
{
    var newOption = document.createElement("option");
    newOption.text = Text;
    newOption.value = value;
    dropDownList.options.add(newOption);
} 


function genericEvent(inObj,name)
{
	// creates an event with the value of the input object, used to name a button
	val = inObj.value ;
    eventSpec = "/sendevent/" + name + "?type=formConfig&val=" + val ;
    doTimedXMLHttpRequest(eventSpec, pollerTimeout) ;
}


function firstOpts(sel)
{
	for (i=0;i<opts.length;i++)
        {
        if (i != sel)
            {
            opt = "<option value='" + i + "'>" + opts[i] + "</option>" ;
            document.write(opt) ;
            }
        else
            {
            opt = "<option selected='true' value='" + i + "'>" + opts[i] + "</option>" ;
            document.write(opt) ;
            }
        }
}

function WASdoSecond(choiceObj)
{
	choice = choiceObj.options[choiceObj.selectedIndex].value;
	//alert ("choice: " + choice) ;
    var second=document.getElementsByName("Second") ;
    //alert(second[0].name + " second found")
	//second[0].options[0].text = "stuff " + choice ;
	//alert ("Choice: " + choice + " Length: " + fOpts[choice].length );
	for (i=0;i<fOpts[choice].length;i++)
		{   
			second[0].options[i].text = fOpts[choice][i] ;
		}
firstVal = choice ;	
}

function doSecond(choiceObj)
{
	choice = choiceObj.options[choiceObj.selectedIndex].value;
    var second=document.getElementsByName("Second") ;
    // clear the list
    clearDropDownList(second[0]) ;
    // build the list 
	for (i=0;i<fOpts[choice].length;i++)
		{   
            //alert ("Adding:" +  fOpts[choice][i]) ;
            addDropDownListItem(second[0],i,fOpts[choice][i] ) ;
		}
firstVal = choice ;	
}




function setSecond(choiceObj)
{
	secondVal = choiceObj.options[choiceObj.selectedIndex].value;
}


function secondOpts(sel)
{
	for (i=0;i<fOpts[sel].length;i++)
        {
        if (i != sel)
            {
            opt = "<option value='" + i + "'>" + fOpts[sel][i] + "</option>" ;
            document.write(opt) ;
            }
        else
            {
            opt = "<option selected='true' value='" + i + "'>" + fOpts[sel][i] + "</option>" ;
            document.write(opt) ;
            }
        }
}


function wbSpecSet(obj)
{
	wbSpec = obj.value ;
}

function wbNumSet(obj)
{
	wbNum = obj.value ;
}

function wbMonSet(obj)
{
	wbNum = obj.value ;
}


/* send all the parameters using sendevent */
function sendEv(buttonID)
{
	first = opts[firstVal] ;
	second = fOpts[firstVal][secondVal] ;
	//alert ("First Opt: " + firstVal + " Val: " + first + " Second Opt: " + secondVal + " Val: " + second + " wbSpec: " + wbSpec + " wbNum: " + wbNum) ;
    eventSpec = "/sendevent/formConfig/" + buttonID + "?type=formConfig&first=" + firstVal + "&firstOpt=" + first + "&second=" + secondVal + "&secondOpt=" + second + "&wbSpec=" + wbSpec + "&wbNum=" + wbNum + "&wbMon=" + wbMon ;
    doTimedXMLHttpRequest(eventSpec, pollerTimeout) ;
}