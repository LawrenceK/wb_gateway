/***********************************
    Slider Widget
    Version 2.1
    by Jeff Greenberg        
    DynAPI2 version: 2.53

***********************************/

/***********************************
     SLIDER OBJECT
***********************************/

function Slider(orientation,gridWidth,gridLength,range,defVal,slotColor,knobColor) {

this.DynLayer = DynLayer;
this.DynLayer();

this.callerID=".widget";

if (orientation != "v" && orientation != "h")
    {
    this.error("Invalid orientation");return false;
    }

this.grid=new grid(this);
this.knob=new knob(this);
this.slot=new slot(this);
this.scale=new scale(this);

//--Init and defaults--

this.widgetBorderTest = "false";
this.knobBorderTest = "false";
this.slotBorderTest = "false";
this.gridBorderTest = "false";
this.scaleBorderTest = "false";

knobPerpDef = gridWidth;
knobParaDef = gridWidth;

this.orientation = orientation;

this.gridWidth = gridWidth;
this.gridLength = gridLength;

this.range = range;

this.callback="null";

this.grid.size(gridWidth,gridLength);
this.setWidth(this.grid.getWidth());
this.setHeight(this.grid.getHeight());

this.slot.size(gridWidth,gridLength);
if (slotColor)
    {
    this.slot.setBgColor(slotColor);
    }

this.knob.size(knobPerpDef,knobParaDef);
if (knobColor)
    {
    this.knob.setBgColor(knobColor);
    }

if (defVal)
    {
    if (defVal>=0 && defVal <=this.range) {this.value=defVal}
    else
        {
        if (defVal < 0) {this.value=0}
        if (defVal > this.range) {this.value=this.range}
        }
    }
else
    {
    this.value=0;
    }

this.setOffset();

this.grid.addChild(this.slot);
this.grid.addChild(this.knob);
this.addChild(this.grid);

this.setKnob(this.value);

// --Event Code--

this.dragEvents = new EventListener(this);

this.dragEvents.ondragmove = function (e) {

var o = e.getTarget();

if (o.orientation == "v") {o.updateValue(o.slot.getHeight()-(o.knob.getY()+Math.round(o.knob.getHeight()/2)-o.slot.getY()))}
if (o.orientation == "h") {o.updateValue((o.knob.getX()+Math.round(o.knob.getWidth()/2))-o.slot.getX())}

if (o.callback != "null")
    {
    o.callback();
    }

e.setBubble(false);
};

this.dragEvents.ondragstart = function (e) {
var o = e.getTarget();
e.setBubble(false);
};

this.dragEvents.ondragend = function (e) {
var o = e.getTarget();
e.setBubble(false);
};

this.setKnobBounds();

DragEvent.enableDragEvents(this.knob);

this.knob.addEventListener(this.dragEvents);


this.slotListener = new EventListener(this);

this.slotListener.onmousedown = function(e) {

o=e.getTarget();

if (o.orientation == "v") 
    {
    var where=e.getY();
    var whereReal=e.getY();
    o.updateKnob(where);
    }
    
if (o.orientation == "h") 
    {
    var where=e.getX();
    var whereReal=e.getX();
    o.updateKnob(where);
    }

if (o.callback != "null")
    {
    o.callback();
    }
}

this.slot.addEventListener(this.slotListener);
}

Slider.prototype=new DynLayer;

//---------------
//   Slider Methods
//---------------

Slider.prototype.error=function(msg) {

alert("Slider Widget Error --> " + msg);

}


Slider.prototype.setOffset=function() {

if (this.orientation == "v")
    {
    this.offset=this.slot.getHeight();
    }

if (this.orientation == "h")
    {
    this.offset=this.slot.getWidth();
    }

this.valStep=this.range/this.offset;

}

Slider.prototype.updateValue=function(midKnobLoc) {


if (this.orientation == "v")
    {
    this.value = Math.round(midKnobLoc * this.valStep);
    }

if (this.orientation == "h")
    {
    this.value = Math.round(midKnobLoc * this.valStep);
    }

if (this.value < 0) {this.value=0}
if (this.value > this.range) {this.value=this.range}

eval(this.callback());

}


Slider.prototype.updateKnob=function(midKnob) {

eval(this.callback());

if (this.orientation == "v")
    {
    this.value = Math.round((this.slot.getHeight()-midKnob) * this.valStep);
    this.knob.setY(midKnob+Math.round(this.knob.getHeight()/2));
    }

if (this.orientation == "h")
    {
    this.value = Math.round(midKnob * this.valStep);
    this.knob.setX((midKnob+this.slot.getX())-Math.round(this.knob.getWidth()/2));
    }

if (this.value < 0) {this.value=0}
if (this.value > this.range) {this.value=this.range}
}

Slider.prototype.setKnob=function(val) {

this.value=val;

if (this.orientation == "v")
    {
    compare = Math.round((this.offset-(val/this.valStep))+(this.slot.getY()-this.grid.getY())-(this.knob.getHeight()/2));
    if ((compare+this.knob.getHeight()) < this.slot.getY()+(this.knob.getHeight()/2)) {compare=this.slot.getY()-(this.knob.getHeight/2)}
    if (val == 0) {compare=this.slot.getHeight()+(this.knob.getHeight()/2)}
    if (val == this.range) {compare=this.slot.getY()-(this.knob.getHeight()/2)}
    this.knob.setY(compare);
    }

if (this.orientation == "h")
    {
    compare = Math.round((val/this.valStep)+(this.slot.getX()-this.grid.getX()));
    if (compare < this.slot.getX()) {compare=this.slot.getX()}
    if (val == 0) {compare=this.slot.getX()-(this.knob.getWidth()/2)}
    if (val == this.range) {compare=this.slot.getWidth()+(this.knob.getWidth()/2)}
    this.knob.setX(compare)
    }

}


Slider.prototype.setKnobBounds=function() {

if (this.orientation == "v")
    {
    DragEvent.setDragBoundary(this.knob,this.slot.getY()-(this.knob.getHeight()/2),this.knob.getX()+this.knob.getWidth(),this.slot.getY()+this.slot.getHeight()+(this.knob.getHeight()/2),this.knob.getX());
    }

if (this.orientation == "h")
    {
    DragEvent.setDragBoundary(this.knob,this.knob.getY(),this.slot.getX()+this.slot.getWidth()+(this.knob.getWidth()/2),this.knob.getY()+this.knob.getHeight(),this.slot.getX()-(this.knob.getWidth()/2));
    }

}

Slider.prototype.createBorders=function() {

eval("this" + this.callerID + "BorderL = new DynLayer();");
eval("this" + this.callerID + "BorderT = new DynLayer();");
eval("this" + this.callerID + "BorderR = new DynLayer();");
eval("this" + this.callerID + "BorderB = new DynLayer();");

eval("this.addChild(this" + this.callerID + "BorderL);");
eval("this.addChild(this" + this.callerID + "BorderT);");
eval("this.addChild(this" + this.callerID + "BorderR);");
eval("this.addChild(this" + this.callerID + "BorderB);");

eval("this" + this.callerID + "BorderTest = \"true\";");

}

Slider.prototype.borderSize=function(l,t,r,b) {

eval("if (this" + this.callerID + "BorderTest == \"false\") {this.error(\"Borders not created.\");}");


eval("this" + this.callerID + "BorderL.moveTo(0,0);this" + this.callerID + "BorderL.setSize(l,this.getHeight());");
eval("this" + this.callerID + "BorderT.moveTo(0,0);this" + this.callerID + "BorderT.setSize(this.getWidth(),t);");
eval("this" + this.callerID + "BorderR.moveTo(this.getWidth()-r,0);this" + this.callerID + "BorderR.setSize(r,this.getHeight());");
eval("this" + this.callerID + "BorderB.moveTo(0,this.getHeight()-b);this" + this.callerID + "BorderB.setSize(this.getWidth(),b);");

}

Slider.prototype.borderColor=function(l,t,r,b) {

eval("if (this" + this.callerID + "BorderTest == \"false\") {this.error(\"Borders not created.\");}");

eval("this" + this.callerID + "BorderL.setBgColor(l);");
eval("this" + this.callerID + "BorderT.setBgColor(t);");
eval("this" + this.callerID + "BorderR.setBgColor(r);");
eval("this" + this.callerID + "BorderB.setBgColor(b);");
}

/***********************************
     COMPONENT DEFINITIONS
***********************************/

//---------------
//   Knob Object
//---------------

function knob(obj) {

this.DynLayer = DynLayer;
this.DynLayer();

this.container=obj;
this.callerID=".knob";

this.createBorders=this.container.createBorders;

this.borderSize=this.container.borderSize;

this.borderColor=this.container.borderColor;

this.error=this.container.error;

}

knob.prototype=new DynLayer;

//---------------
//   Knob Methods
//---------------

knob.prototype.size=function(w,h) {

if (this.container.orientation=="v")
    {
    this.setSize(w,h);
    this.setX(Math.round((this.container.grid.getWidth()/2)-(this.getWidth()/2)));    
    }

if (this.container.orientation=="h")
    {
    this.setSize(h,w);
    this.setY(Math.round((this.container.grid.getHeight()/2)-(this.getHeight()/2)));
    }
    
this.container.setOffset();
this.container.setKnobBounds();
this.container.setKnob(this.container.value);
}

//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

//---------------
//   Slot Object
//---------------

function slot(obj) {

this.DynLayer = DynLayer;
this.DynLayer();

this.container=obj;
this.callerID=".slot";

this.createBorders=this.container.createBorders;

this.borderSize=this.container.borderSize;

this.borderColor=this.container.borderColor;

this.error=this.container.error;
}

slot.prototype=new DynLayer;

//---------------
//   Slot Methods
//---------------

slot.prototype.size=function(w,h) {

if (this.container.orientation=="v")
    {
    this.setSize(w,h);
    this.moveTo(Math.round((this.container.grid.getWidth()/2) - (this.container.slot.getWidth()/2)),Math.round((this.container.grid.getHeight()/2) - (this.container.slot.getHeight()/2)));
    }

if (this.container.orientation=="h")
    {
    this.setSize(h,w);
    this.moveTo(Math.round((this.container.grid.getWidth()/2) - (this.container.slot.getWidth()/2)),Math.round((this.container.grid.getHeight()/2) - (this.container.slot.getHeight()/2)));
    }

this.container.setOffset();
this.container.setKnobBounds();
this.container.setKnob(this.container.value);
}

//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

//---------------
//   Scale Object
//---------------

function scale(obj) {

this.DynLayer = DynLayer;
this.DynLayer();

this.container=obj;
this.callerID=".scale";

this.container.addChild(this);

this.createBorders=this.container.createBorders;

this.borderSize=this.container.borderSize;

this.borderColor=this.container.borderColor;

this.error=this.container.error;

}

scale.prototype=new DynLayer;

//---------------
//   Scale Methods
//---------------


scale.prototype.createScale=function(pos,color) {

this.color=color;

if (this.container.orientation=="v")
    {
    this.setSize(30,this.container.getHeight());
    this.container.setWidth(this.container.getWidth()+30);
    this.container.borderSize(this.container.widgetBorderL.getWidth(),this.container.widgetBorderT.getHeight(),this.container.widgetBorderR.getWidth(),this.container.widgetBorderB.getHeight());
    if (pos == 1)
        {
        this.container.grid.setX(this.container.grid.getX()+30);
        this.scaleCenter=this.getWidth()-4;
        this.labelX=this.scaleCenter-22;
        this.whereX=0;
        this.whereY=0;                
        }
    if (pos == 2)
        {
        this.scaleCenter=4;
        this.labelX=this.scaleCenter+6;
        this.whereX=this.container.grid.getX()+this.container.grid.getWidth();
        this.whereY=0;
        }
    
    this.moveTo(this.whereX,this.whereY);
    
    if (color != false) {
    
    this.scaleLength=new DynLayer();
    this.scaleLength.moveTo(this.scaleCenter,this.container.slot.getY());
    this.scaleLength.setSize(1,this.container.slot.getHeight());
    this.scaleLength.setBgColor(color);

    this.scaleTop=new DynLayer();
    this.scaleTop.moveTo(this.scaleCenter-3,this.container.slot.getY());
    this.scaleTop.setSize(7,1);
    this.scaleTop.setBgColor(color);

    this.scaleBottom=new DynLayer();
    this.scaleBottom.moveTo(this.scaleCenter-3,this.container.slot.getY()+this.container.slot.getHeight()-1);
    this.scaleBottom.setSize(7,1);
    this.scaleBottom.setBgColor(color);

    this.addChild(this.scaleLength);
    this.addChild(this.scaleTop);
    this.addChild(this.scaleBottom);

    this.scaleTopLabel=new DynLayer();
    this.scaleTopLabel.setSize(11,this.fontSize);
    this.scaleTopLabel.moveTo(this.labelX,this.scaleLength.getY()-(Math.round(this.scaleFontSize/2)));
    this.scaleTopLabel.setHTML('<DIV ID="top" STYLE="fontFamily:' + this.scaleFontFace + ';font-size:' + this.scaleFontSize + 'px;color:' + this.scaleFontColor + ';">' + this.container.range + '</DIV>');

    this.scaleBottomLabel=new DynLayer();
    this.scaleBottomLabel.setSize(11,this.fontSize);
    this.scaleBottomLabel.moveTo(this.labelX,this.scaleLength.getY()+this.scaleLength.getHeight()-(Math.round(this.scaleFontSize/2))-2);
    this.scaleBottomLabel.setHTML('<DIV ID="bot" STYLE="fontFamily:' + this.scaleFontFace + ';font-size:' + this.scaleFontSize + 'px;color:' + this.scaleFontColor + ';">0</DIV>');
        
    this.addChild(this.scaleTopLabel);
    this.addChild(this.scaleBottomLabel);
    }    
    }

if (this.container.orientation=="h")
    {
    this.setSize(this.container.getWidth(),25);
    this.container.setHeight(this.container.getHeight()+25);
    this.container.borderSize(this.container.widgetBorderL.getWidth(),this.container.widgetBorderT.getHeight(),this.container.widgetBorderR.getWidth(),this.container.widgetBorderB.getHeight());
    if (pos == 1)
        {
        this.container.grid.setY(this.container.grid.getY()+25);
        this.scaleCenter=this.getY()+19;
        this.labelY=this.scaleCenter-18;
        this.whereY=0;
        this.whereX=0; 
        }
    if (pos == 2)
        {
        this.scaleCenter=this.getY()+this.getHeight()-20;
        this.labelY=this.scaleCenter+4;  
        this.whereX=0;
        this.whereY=this.container.grid.getY()+this.container.grid.getHeight();    
        }
        
    this.moveTo(this.whereX,this.whereY);

    if (color != false) {

    this.scaleLength=new DynLayer();
    this.scaleLength.moveTo(this.container.slot.getX(),this.scaleCenter);
    this.scaleLength.setSize(this.container.slot.getWidth(),1);
    this.scaleLength.setBgColor(color);

    this.scaleBottom=new DynLayer();
    this.scaleBottom.moveTo(this.container.slot.getX(),this.scaleCenter-3);
    this.scaleBottom.setSize(1,7);
    this.scaleBottom.setBgColor(color);

    this.scaleTop=new DynLayer();
    this.scaleTop.moveTo(this.container.slot.getX()+this.container.slot.getWidth()-1,this.scaleCenter-3);
    this.scaleTop.setSize(1,7);
    this.scaleTop.setBgColor(color);

    this.addChild(this.scaleLength);
    this.addChild(this.scaleTop);
    this.addChild(this.scaleBottom);

    this.scaleBottomLabel=new DynLayer();
    this.scaleBottomLabel.setSize(11,this.fontSize);
    this.scaleBottomLabel.moveTo(this.scaleLength.getX()-2,this.labelY); //change "-2" to get contentWidth/2
    this.scaleBottomLabel.setHTML('<DIV ID="bot" STYLE="fontFamily:' + this.scaleFontFace + ';font-size:' + this.scaleFontSize + 'px;color:' + this.scaleFontColor + ';">0</DIV>');

    this.scaleTopLabel=new DynLayer();
    this.scaleTopLabel.setSize(11,this.fontSize);
    this.scaleTopLabel.moveTo(this.scaleLength.getX()+this.scaleLength.getWidth()-(Math.round(11/2))-2,this.labelY);
    this.scaleTopLabel.setHTML('<DIV ID="top" STYLE="fontFamily:' + this.scaleFontFace + ';font-size:' + this.scaleFontSize + 'px;color:' + this.scaleFontColor + ';">' + this.container.range + '</DIV>');
       
    this.addChild(this.scaleTopLabel);
    this.addChild(this.scaleBottomLabel);    
    }
    }
}

scale.prototype.setDiv=function(num) {

if (this.container.orientation=="v") 
    {
    scaleLengthV=this.scaleLength.getHeight();
    markOffset="this.scaleCenter-2,divCompare+(this.container.slot.getY()-this.container.grid.getY())";
    labelOffset="this.labelX,currentMark.getY()-(Math.round(this.scaleFontSize/2))";
    markSizeX=5;markSizeY=1;rangeDisplayVal="rangeNumber";
    }
if (this.container.orientation=="h")
    {
    scaleLengthV=this.scaleLength.getWidth();
    markOffset="divCompare+(this.container.slot.getX()-this.container.grid.getX()),this.scaleCenter-2";
    labelOffset="currentMark.getX()-Math.round(11/2),this.labelY";
    markSizeX=1;markSizeY=5;rangeDisplayVal="this.container.range-rangeNumber";
    }

div=scaleLengthV/num;
rangeNumber=this.container.range/num;
divCompare=scaleLengthV-div;

Math.round(divCompare);

rangeTest = rangeNumber;

var counter=0;

while (divCompare > 0)
    {
    eval("rangeDisplay=" + rangeDisplayVal +";");
    eval("this.div" + counter + "=new DynLayer();");
    eval("currentMark=this.div" + counter);
    eval("this.div" + counter + ".setSize(markSizeX,markSizeY);");
    eval("this.div" + counter + ".moveTo(" + markOffset + ");");
    eval("this.div" + counter + ".setBgColor(this.color);");
    eval("this.addChild(this.div" + counter + ");");
    
    eval("this.div" + counter + "Label=new DynLayer();");
    eval("currentLabel=this.div" + counter + "Label;");
    currentLabel.setSize(11,this.fontSize);
    eval("currentLabel.moveTo(" + labelOffset + ");");
    currentLabel.setHTML('<DIV ID="div' + counter + '" STYLE="fontFamily:' + this.scaleFontFace + ';font-size:' + this.scaleFontSize + 'px;color:' + this.scaleFontColor + ';">' + (rangeDisplay) + '</DIV>');
    
    this.addChild(currentLabel);
    
    divCompare=divCompare-div;
    rangeNumber+=rangeTest;
    
    Math.round(divCompare);
    counter++;
    }

}

scale.prototype.setLabelStyle=function(face,size,color) {

this.scaleFontFace=face;
this.scaleFontSize=size;
this.scaleFontColor=color;

}

scale.prototype.size=function() {
this.container.error("There is no built in scale sizing method as of yet, although there may be in the future.");
}

//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

//---------------
//   Grid Object
//---------------

function grid(obj) {

this.DynLayer = DynLayer;
this.DynLayer();

this.container=obj;
this.callerID=".grid";

this.createBorders=this.container.createBorders;

this.borderSize=this.container.borderSize;

this.borderColor=this.container.borderColor;

this.error=this.container.error;

}

grid.prototype=new DynLayer;

//---------------
//   Grid Methods
//---------------

grid.prototype.size=function(w,h) {

if (this.container.orientation=="v")
    {
    this.setSize(w,h);
    }

if (this.container.orientation=="h")
    {
    this.setSize(h,w);
    }

}