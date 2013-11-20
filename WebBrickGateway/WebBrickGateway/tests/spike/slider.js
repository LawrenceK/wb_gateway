/****************************************************************
 * Slider
 *   
 * Slider050723
 * by Christiaan Hofman, July 2005
 *   
 * You may use or modify this code provided that this copyright notice
 * appears on all copies.
 *   
 *  Constructor:
 *    var slider = new Slider( [name] );
 *       (default: name = "slider0", "slider1", ...)
 *   
 *  Creating Methods
 *    slider.writeSlider();
 *    slider.placeSlider( [imgName] );
 *        (default: imgName = name+"RailImg")
 * 
 *  Control Methods:
 *    slider.getValue();
 *    slider.setValue( [value] );
 *
 *  Event Handlers:
 *    slider.onmouseover( e );
 *    slider.onmouseout( e );
 *    slider.onmousedown( e );
 *    slider.onmouseup( e );
 *    slider.onslide( e );
 *    slider.onchange( e );
 *    slider.onclick( e );
 * 
 *  Default Initial Settings:   
 * 
 *    slider.leftValue = 0;
 *    slider.rightValue = 1;
 *    slider.defaultValue = 0;
 *    slider.offsetX = 1;
 *    slider.offsetY = 1;
 *    slider.maxSlide = 258;
 *    slider.buttonWidth = 40;
 *    slider.buttonHeight = 28;
 *    slider.buttonImg = "sliderbutton.gif";
 *    slider.buttonHiliteImg = "sliderhibutton.gif";
 *    slider.imgPath = "";
 *    slider.orientation = "h";
 * 
 ****************************************************************
 *  EXAMPLE:
 *
 *  <html>
 *  <head>
 *  <script language="javascript" src="slider.js"></script>
 *  <script language="javascript">
 *    mySlider = new Slider( "MySlider" );
 *  </script>
 *  </head>
 *  <body onload="mySlider.placeSlider()">
 *  <img src="sliderbg.gif" name="MySliderRailImg">
 *  <script language="javascript">
 *    mySlider.writeSlider();
 *  </script>
 *  </body>
 * </html>
 ****************************************************************
 */

// Constructor

function Slider(name) {
    this.leftValue = 0;
    this.rightValue = 1;
    this.defaultValue = 0;
    this.offsetX = 1;
    this.offsetY = 1;
    this.maxSlide = 258;
    this.buttonWidth = 40;
    this.buttonHeight = 28;
    this.buttonImg = "sliderbutton.gif";
    this.buttonHiliteImg = "sliderhibutton.gif";
    this.buttonHoverImg = null;
    this.imgPath = "";
    this.orientation = "h";
    
    this.writeSlider = Slider.writeSlider;
    this.placeSlider = Slider.placeSlider;
    this.makeEventHandler = Slider.makeEventHandler;
    this.isPrototype = Slider.isPrototype;
    this.getValue = Slider.getValue;
    this.setValue = Slider.setValue;
     
    this.MouseOver = Slider.MouseOver;
    this.MouseOut = Slider.MouseOut;
    this.MouseDown = Slider.MouseDown;
    this.MouseUp = Slider.MouseUp;
    this.MouseSlide = Slider.MouseSlide;

    this.onmouseover = null;
    this.onmouseout = null;
    this.onmousedown = null;
    this.onmouseup = null;
    this.onslide = null;
    this.onchange = null;
    this.onclick = null;

    if (!window.sliders)  window.sliders = new Array();
    this.name = name || "slider"+window.sliders.length;
    window.sliders[window.sliders.length] = this;
    window.sliders[this.name] = this;
    if (!window.sliderDrag)  window.sliderDrag = new Object();
}

// method write the button DIV

Slider.writeSlider = function () {
	if (!document.getElementById) return; // no W3C support
	
    var proto = this.prototype || this;

    // create images for the prototype, if not already set
    if (!proto.loImg) {
        proto.loImg = new Image(proto.buttonWidth,proto.buttonHeight);
        proto.loImg.src = proto.imgPath + proto.buttonImg;
       if (proto.buttonHiliteImg) {
            proto.hiImg = new Image(proto.buttonWidth,proto.buttonHeight);
            proto.hiImg.src = proto.imgPath + (proto.buttonHiliteImg || proto.buttonImg);
        }
        if (proto.buttonHoverImg) {
            proto.hoImg = new Image(proto.buttonWidth,proto.buttonHeight);
            proto.hoImg.src = proto.imgPath + proto.buttonHoverImg;
        }
    }
    // set the properties according to the prototype
    if (proto != this) {
        this.loImg = proto.loImg;
        if (proto.hiImg)  this.hiImg = proto.hiImg;
        if (proto.hoImg)  this.hoImg = proto.hoImg;
        this.orientation = proto.orientation;
        this.maxSlide = proto.maxSlide;
    }

    // style for the slider button
    var style = '<STYLE TYPE="text/css"><!--\n' +
        '#'+this.name+'Button {visibility:hidden; position:absolute; width:'+ proto.buttonWidth +'px; height:'+ proto.buttonHeight +'px; z-index:1; }\n' +
        '--></STYLE>';

    // html for the button div
    var content = '<DIV ID="'+this.name+'Button">'+
        '<IMG ID="'+this.name+'ButtonImg" SRC="'+proto.loImg.src+'" WIDTH='+proto.buttonWidth+' HEIGHT='+proto.buttonHeight+'>'+
        '</DIV>';

    // write the button style and content in the document
	document.writeln(style);
	document.writeln(content);

    // set button properties and mouse event handlers
	this.button = document.getElementById(this.name+"Button");
	this.button.img = document.getElementById(this.name+"ButtonImg");
	this.button.style.width = proto.buttonWidth + 'px';
	this.button.style.height = proto.buttonHeight + 'px';
	if (this.button.addEventListener) {
		this.button.addEventListener("mousedown",this.MouseDown,false);
		this.button.addEventListener("mouseout",this.MouseOut,false);
		this.button.addEventListener("mouseover",this.MouseOver,false);
    } else {
        this.button.onmousedown = this.MouseDown;
        this.button.onmouseout = this.MouseOut;
        this.button.onmouseover = this.MouseOver;
    }
    // set event handlers as functions
    this.onmouseover = this.makeEventHandler(this.onmouseover);
    this.onmouseout  = this.makeEventHandler(this.onmouseout);
    this.onmousedown = this.makeEventHandler(this.onmousedown);
    this.onmouseup   = this.makeEventHandler(this.onmouseup);
    this.onslide     = this.makeEventHandler(this.onslide);
    this.onchange    = this.makeEventHandler(this.onchange);
    this.onclick     = this.makeEventHandler(this.onclick);
    // tell button who we are
    this.button.slider = this;
    // from now on button refers to the style object
    this.button = this.button.style;
}

// method to put the slider button in place

Slider.placeSlider = function (imgName) {
	if (!document.getElementById) return; // no W3C support
	
    var proto = this.prototype || this;

    // set name or default name
    imgName = imgName || this.name+'RailImg';
    // find the rail image
    this.rail = (typeof(imgName) == 'string')? document.getElementById(imgName) : imgName;
    // offset w.r.t rail
    var x = proto.offsetX;
    var y = proto.offsetY;
    // add global position of rail and parents in global document to the offset
    if (this.rail.offsetParent) {
        var parent = this.rail;
         while (parent) {
            x += parent.offsetLeft;
            y += parent.offsetTop;
            parent = parent.offsetParent;
        }
        // Fix for IE 5 for Mac
        if (navigator.userAgent.indexOf("MSIE")+1 && navigator.userAgent.indexOf("Mac")+1) {
            x += parseInt(document.body.currentStyle.marginLeft);
            y += parseInt(document.body.currentStyle.marginTop);
        }
    } else {
        x += (typeof(this.rail.pageX) == 'number')? this.rail.pageX : this.rail.x;
        y += (typeof(this.rail.pageY) == 'number')? this.rail.pageY : this.rail.y;
    }
    // set position of button
    this.button.left = x + 'px';
    this.button.top = y + 'px';
    // offset is remembered for later sliding
    this.offset = (proto.orientation == "v")? y : x;
    // put button in default position and make visible
    this.setValue(this.defaultValue);
    this.button.visibility = 'inherit';
}

// makes slider a prototype for all previously defined sliders

Slider.isPrototype = function () {
    for (var i=0; i<window.sliders.length; i++)  
        window.sliders[i].prototype = window.sliders[i].prototype || this;
}

// mouseover handler of the button, only calls handler of slider

Slider.MouseOver = function (e) {
    window.sliderDrag.isOver = true;
    if (this.slider.hoImg && !window.sliderDrag.isDown)  this.img.src = this.slider.hoImg.src;   
    if (this.slider.onmouseover)  this.slider.onmouseover(e);
}

// mouseout handler of the button, only calls handler of slider

Slider.MouseOut = function (e) {
    window.sliderDrag.isOver = false;
    if (this.slider.hoImg && !window.sliderDrag.isDown)  this.img.src = this.slider.loImg.src;   
    if (this.slider.onmouseout)  this.slider.onmouseout(e);
}

// mousedown handler of the button

Slider.MouseDown = function (e) {
    var slider = this.slider;
    // remember me
    window.sliderDrag.dragLayer = this;
    window.sliderDrag.dragged = false;
    window.sliderDrag.isDown = true;
    // event position
    var evtX = evtY = 0;
    if (!e) e = window.event;
    if (typeof(e.pageX) == 'number') {
        evtX = e.pageX;
        evtY = e.pageY;
    } else if (typeof(e.clientX) == 'number') {
        evtX = e.clientX + (document.body.scrollLeft || 0);
        evtY = e.clientY + (document.body.scrollTop || 0);
    }
    // ignore right mouse button
    if ((e.which && e.which == 3) || (e.button && e.button == 2)) return true;
    // set starting offset of event
	window.sliderDrag.offX  =  evtX - parseInt(this.style.left) + slider.offset;
	window.sliderDrag.offY  =  evtY - parseInt(this.style.top) + slider.offset;
	if (e.cancelable) e.preventDefault();
	if (e.stopPropagation) e.stopPropagation();
	e.cancelBubble = true; 
    // document handles move and up events
    document.onmousemove = slider.MouseSlide;
    document.onmouseup = slider.MouseUp;
    if (document.captureEvents) document.captureEvents(Event.MOUSEMOVE|Event.MOUSEUP);
    // show hilite img
    if (slider.hiImg) this.img.src = slider.hiImg.src;
    // call event handler of slider
    if (slider.onmousedown)  slider.onmousedown(e);
    return false;
}

// mouseup handler of the button

Slider.MouseUp = function (e) {
    // button and slider that was draged
    var l = window.sliderDrag.dragLayer;
    var slider = l.slider;
    window.sliderDrag.isDown = false;
    // cancel move and up event handlers of document
    document.onmousemove = null;
    document.onmouseup = null;
    if (document.releaseEvents) document.releaseEvents(Event.MOUSEMOVE|Event.MOUSEUP);
    window.sliderDrag.dragLayer = null;
    // show normal image
    if (slider.hiImg) 
        l.img.src = (window.sliderDrag.isOver && slider.hoImg)? slider.hoImg.src : slider.loImg.src;
    // cal event handlers of slider
    if (slider.onmouseup)  slider.onmouseup(e);
    if (window.sliderDrag.dragged) {
        if (slider.onchange) slider.onchange(e);
    } else {
        if (slider.onclick) slider.onclick(e);
    }
    return false;
}

// mousemove handler of the button for sliding

Slider.MouseSlide = function (e) {
    // button and slider to be draged
    var l = window.sliderDrag.dragLayer;
    var slider = l.slider;
    // we have dragged the slider; for click
    window.sliderDrag.dragged = true;
    // event position
    var evtX = evtY = 0;
    if (!e) e = window.event;
    if (typeof(e.pageX) == 'number') {
        evtX = e.pageX;
        evtY = e.pageY;
    } else if (typeof(e.clientX) == 'number') {
        evtX = e.clientX + (document.body.scrollLeft || 0);
        evtY = e.clientY + (document.body.scrollTop || 0);
    }
    var pos = (slider.orientation == "h")? 
        Math.max(Math.min(evtX - window.sliderDrag.offX,slider.maxSlide),0) + slider.offset :
        Math.max(Math.min(evtY - window.sliderDrag.offY,slider.maxSlide),0) + slider.offset;
    // move slider. 
	if (slider.orientation == "h")  l.style.left = pos + 'px';
	else  l.style.top = pos + 'px';
	if (e.cancelable) e.preventDefault();
	if (e.stopPropagation) e.stopPropagation();
	e.cancelBubble = true;
    // call slider event handlers
    if (slider.onchange)  slider.onchange(e);
    if (slider.onslide)  slider.onslide(e);
    return false;
}

// calculate the value of the slider from position

Slider.getValue = function (n) {
    var pos = (this.orientation == "h")? parseInt(this.button.left) : parseInt(this.button.top);
    var val =  this.leftValue + (this.rightValue-this.leftValue) * (pos-this.offset) / this.maxSlide;
    return (typeof(n) == 'number')?  toDecimals(val,n) :  val;
}

// set the position of the slider from a value

Slider.setValue = function (value,ignore) {
    if (typeof(value) == 'string')  value = parseFloat(value);
    if (isNaN(value))  value = this.defaultValue;
    // set within min/max bounds
    var rangeValue = (this.rightValue >= this.leftValue)? 
        Math.min(Math.max(value,this.leftValue),this.rightValue) - this.leftValue : 
        Math.max(Math.min(value,this.leftValue),this.rightValue) - this.leftValue;
    var pos = this.maxSlide * rangeValue / (this.rightValue-this.leftValue) + this.offset + 'px';
    // move button to calculated position
	if (this.orientation == "h")  this.button.left = pos;
	else  this.button.top = pos;
    // call slider event handler, unless ignore is true
    if (this.onchange && (!ignore))  this.onchange(null);
}

// make an event handler, ensuring that it is a function

Slider.makeEventHandler = function (f) {
    return (typeof(f) == 'string')? new Function('e',f) : ((typeof(f) == 'function')? f : null);
}

// return a value as a string with a fixed number of decimals

function toDecimals(val,n) {
    if (isNaN(n)) return val;
    for (var m=0; m<n; m++)  val *= 10;
    for (var m=0; m>n; m--) val *= 0.1;
    val = Math.round(val);
    if (val < 0) {
        val = -val;
        var sgn = "-";
    } else {
        var sgn = "";
    }
    var valstr = val.toString();
    if (n>0) {
        while (valstr.length<=n) valstr = "0"+valstr;
        var len = valstr.length;
        valstr = valstr.substring(0,len-n) +"."+ valstr.substring(len-n,len);
    } else if (n<0) {
        for (m=0; m>n; m--) valstr = valstr+"0";
    }
    return sgn+valstr;
}
