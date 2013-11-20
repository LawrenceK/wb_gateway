var UI={};
UI.version="0.5.0";
UI.Lang={};
UI.Lang.Language=function(_1,_2){
bindMethods(this);
this.code=_1;
this.messages=_2;
};
UI.Lang.Language.prototype={"translate":function(_3){
return this.messages[_3];
}};
UI.Lang.C=new UI.Lang.Language("C",{});
UI.Lang.es=new UI.Lang.Language("es",{"The value must be a number":"El valor debe ser num\xe9rico","The field is required":"Debe ingresar un valor en este campo","The field is not valid":"El valor ingresado no es v\xe1lido","The value must contain only letters":"El valor debe contener solo letras"});
UI.Lang.setLanguage=function(_4){
if(typeof (_4)!="undefined"&&typeof (UI.Lang[_4])!="undefined"){
UI.Lang.current=UI.Lang[_4];
}else{
logWarning("UI.Lang has no translations for language "+_4);
UI.Lang.current=UI.Lang.C;
}
};
if(typeof (LANG)!="undefined"){
UI.Lang.setLanguage(LANG);
}else{
var _detectedLang=navigator.userLanguage||navigator.browserLanguage||navigator.language;
if(_detectedLang.length>=2){
UI.Lang.setLanguage(_detectedLang.substring(0,2));
}else{
logWarning("UI.Lang: Can't autodetect language. (Browser says: "+_detectedLang+")");
UI.Lang.setLanguage("C");
}
_detectedLang=null;
}
function _(_5){
return UI.Lang.current.translate(_5)||_5;
}
UI.Widget=function(_6){
bindMethods(this);
this.element=$(_6);
this.cssClass="uiwidget";
this.register();
};
UI.Widget.get=function(_7){
return $(_7)._widget;
};
var w$=UI.Widget.get;
UI.Widget.prototype={"register":function(){
if(this.element){
this.element._widget=this;
addElementClass(this.element,this.cssClass);
}
},"hide":function(){
hideElement(this.element);
},"show":function(_8){
showElement(this.element,_8);
}};
UI.TableModel=function(){
bindMethods(this);
};
UI.TableModel.prototype={"getNumCols":function(){
return 0;
},"getNumRows":function(){
return 0;
},"getCell":function(_9,_10){
return null;
},"getHeader":function(_11){
return null;
},"getFooter":function(_12){
return null;
},"getColType":function(_13){
return null;
},"hasHeader":function(){
return false;
},"hasFooter":function(){
return false;
},"getRow":function(_14){
return map(partial(this.getCell,_14),range(0,this.getNumCols()));
},"getRows":function(){
return map(this.getRow,range(0,this.getNumRows()));
},"getHeaders":function(){
return map(this.getHeader,range(0,this.getNumCols()));
},"getFooters":function(){
return map(this.getFooter,range(0,this.getNumCols()));
},"getColTypes":function(){
return map(this.getColType,range(0,this.getNumCols()));
}};
UI.ArrayTableModel=function(_15,_16,_17,_18,_19){
bindMethods(this);
this.objects=_15||[];
this.fields=_16||this._autoDetectFields();
this.headers=_18||this._autoDetectHeaders();
this.types=_17;
this.footers=_19;
};
UI.ArrayTableModel.prototype=update(new UI.TableModel(),{"getNumCols":function(){
return this.fields?this.fields.length:0;
},"getNumRows":function(){
return this.objects?this.objects.length:0;
},"getCell":function(_20,_21){
var val;
try{
val=this.objects[_20][this.fields[_21]];
if(val==null||typeof (val)=="undefined"){
val="";
}
}
catch(e){
val="";
}
return val;
},"getHeader":function(_23){
try{
return this.headers[_23];
}
catch(e){
return "";
}
},"getFooter":function(_24){
try{
return this.footers[_24];
}
catch(e){
return "";
}
},"getColType":function(_25){
try{
return this.types[_25];
}
catch(e){
return "string";
}
},"_autoDetectFields":function(){
if(this.objects&&this.objects.length>=1){
var _26=[];
for(field in this.objects[0]){
_26.push(field);
}
return _26;
}else{
return [];
}
},"_autoDetectHeaders":function(){
var _27=[];
for(var i=0;i<this.getNumCols();i++){
_27.push(this.fields[i]);
}
return _27;
},"hasHeader":function(){
return !(!this.headers);
},"hasFooter":function(){
return !(!this.footers);
},"changed":function(){
signal(this,"changed");
}});
UI.AsyncArrayTableModel=function(_29,_30,_31,_32){
bindMethods(this);
this.objects=[];
this.fields=_29;
this.headers=_31;
this.types=_30;
this.footers=_32;
};
UI.AsyncArrayTableModel.prototype=update(new UI.ArrayTableModel(),{"retrieveData":function(url,_34){
var _34=_34||"GET";
var d=loadJSONDoc(url);
d.addCallback(this._receiveData);
return d;
},"_receiveData":function(_36){
this.objects=_36;
if(!this.fields){
this._autoDetectFields();
}
if(!this.headers){
this._autoDetectHeaders();
}
this.changed();
}});
UI.HTMLTableModel=function(_37,_38){
bindMethods(this);
this._htmlTable=_37;
this._colTypes=_38;
};
UI.HTMLTableModel.prototype=update(new UI.TableModel(),{"getNumCols":function(){
try{
return this._htmlTable.tBodies[0].rows[0].cells.length;
}
catch(e){
return 0;
}
},"getNumRows":function(){
try{
return this._htmlTable.tBodies[0].rows.length;
}
catch(e){
return 0;
}
},"getCell":function(_39,_40){
try{
return this._htmlTable.tBodies[0].rows[_39].cells[_40].childNodes;
}
catch(e){
return "";
}
},"getHeader":function(_41){
try{
return this._htmlTable.tHead.rows[0].cells[_41].childNodes;
}
catch(e){
return "";
}
},"getFooter":function(_42){
try{
return this._htmlTable.tFoot.rows[0].cells[_42].childNodes;
}
catch(e){
return "";
}
},"getColType":function(_43){
try{
if(this._colTypes){
return this._colTypes[_43];
}else{
return "string";
}
}
catch(e){
return "string";
}
},"hasHeader":function(){
return !(!this._htmlTable.tHead);
},"hasFooter":function(){
return !(!this._htmlTable.tFoot);
}});
UI.ListModel=function(){
bindMethods(this);
};
UI.ListModel.prototype={"getLabel":function(_44){
return "";
},"getValue":function(_45){
return "";
},"getLength":function(){
return 0;
}};
UI.ArrayListModel=function(_46,_47,_48){
bindMethods(this);
this.objects=_46;
this.labelField=_47;
this.valueField=_48;
};
UI.ArrayListModel.prototype=update(new UI.ListModel(),{"getLabel":function(_49){
return this.labelField?this.objects[_49][this.labelField]:""+this.objects[_49];
},"getValue":function(_50){
return this.valueField?this.objects[_50][this.valueField]:this.getLabel(_50);
},"getLength":function(){
return this.objects.length;
},"changed":function(){
signal(this,"changed");
}});
UI.AsyncArrayListModel=function(_51,_52){
bindMethods(this);
this.objects=[];
this.labelField=_51;
this.valueField=_52;
};
UI.AsyncArrayListModel.prototype=update(new UI.ArrayListModel(),{"retrieveData":function(url,_53){
var _53=_53||"GET";
var d=loadJSONDoc(url);
d.addCallback(this._receiveData);
return d;
},"_receiveData":function(_54){
this.objects=_54;
this.changed();
return _54;
}});
UI.HTMLSelectListModel=function(_55){
this._options=_55.getElementsByTagName("option");
};
UI.HTMLSelectListModel.prototype=update(new UI.ListModel(),{"getLabel":function(_56){
return scrapeText(this._options[_56]);
},"getValue":function(_57){
return this._options[_57].value;
},"getLength":function(){
try{
return this._options.length;
}
catch(e){
return 0;
}
}});
UI.Window=function(_58){
bindMethods(this);
this.element=$(_58);
this.titleBar=null;
this.content=null;
this.draggableTitle=null;
var _59=this.element.getElementsByTagName("h1");
var _60=null;
if(_59.length==0){
this.setTitleBar(UI.Window.standardTitleBar("Untitled Window"));
}else{
this.setTitleBar(_59[0]);
}
var _61=getElementsByTagAndClassName("div","uicontent",this.element);
if(_61.length==0){
var div=DIV({"class":"uicontent"});
var _63=filter(function(el){
return el.className!="uititlebar";
},this.element.childNodes);
map(partial(appendChildNodes,div),_63);
this.setContent(div);
}else{
this.setContent(_61[0]);
}
this.resize(elementDimensions(this.element));
this.visible=computedStyle(this.element,"display")!="none";
this.cssClass="uiwindow";
this.register();
this.NAME=this.element.id+" (UI.Window)";
};
UI.Window.prototype=update(new UI.Widget(),{"show":function(_65){
showElement(this.element);
signal(this,"shown");
if(_65){
this.moveTo(_65);
}
},"hide":function(){
hideElement(this.element);
signal(this,"hidden");
},"close":function(){
removeElement(this.element);
this.draggableTitle.disable();
this.draggableTitle=null;
signal(this,"closed");
},"moveTo":function(_66){
setElementPosition(this.element,_66);
signal(this,"moved",_66);
},"resize":function(_67){
setElementDimensions(this.element,_67);
},"_adjustSize":function(){
setElementDimensions(this.content,{"w":this.element.clientWidth-4,"h":this.element.clientHeight-elementDimensions(this.titleBar).h-4});
},"include":function(url){
var el=DIV();
this.setContent(el);
var d=doSimpleXMLHttpRequest(url);
d.addCallback(function(req){
removeElementClass(el,"uierror");
el.innerHTML=req.responseText;
return req;
});
d.addErrback(function(req){
addElementClass(el,"uierror");
if(req){
el.innerHTML=req.responseText;
}else{
el.innerHTML=_("Error loading")+" "+url;
}
});
return d;
},"setTitleBar":function(_69){
if(this.titleBar){
removeElement(this.titleBar);
this.draggableTitle.disable();
}
addElementClass(_69,"uititlebar");
if(this.element.firstChild){
this.element.insertBefore(_69,this.element.firstChild);
}else{
this.element.appendChild(_69);
}
this.titleBar=_69;
this.draggableTitle=new UI.Draggable(this.titleBar);
this.draggableTitle.elementToMove=this.element;
},"setContent":function(_70){
if(this.content){
removeElement(this.content);
}
addElementClass(_70,"uicontent");
this.content=_70;
appendChildNodes(this.element,this.content);
setElementDimensions(this.content,{"w":this.element.clientWidth-4,"h":this.element.clientHeight-elementDimensions(this.titleBar).h-4});
}});
UI.Window._fromElement=function(_71){
var win=new UI.Window(_71);
var _73=getNodeAttribute("ui:draggable")||"true";
if(_73=="false"){
win.draggableTitle.disable();
}
};
UI.Window.standardTitleBar=function(_74){
return H1({"class":"uititlebar"},_74);
};
UI.Draggable=function(_75,_76,_77,_78){
bindMethods(this);
this.element=$(_75);
this.elementToMove=$(_75);
this.flags=arguments.length>=2?_76:UI.Draggable.DRAG_X|UI.Draggable.DRAG_Y;
this.leftLimits=_77;
this.topLimits=_78;
this._dragXStart=-1;
this._dragYStart=-1;
this._leftStart=-1;
this._topStart=-1;
this._installMouseDown();
this._disabled=false;
this.NAME=repr(_75)+" (Draggable)";
};
UI.Draggable.DRAG_X=1;
UI.Draggable.DRAG_Y=2;
UI.Draggable._oldonmousemove=document.onmousemove;
UI.Draggable._oldonmouseup=document.onmouseup;
UI.Draggable._draggable=null;
UI.Draggable.prototype={"startFromEvent":function(e){
var e=e||window.event;
var x=e.screenX;
var y=e.screenY;
this.start(x,y);
},"start":function(_82,_83){
if(this._disabled){
return;
}
if(UI.Draggable._draggable){
logError("Can't drag "+repr(this.element)+" as "+repr(UI.Draggable._draggable.element)+" is being already dragged");
return;
}
UI.Draggable._draggable=this;
this.elementToMove.style.zIndex=1;
this._dragXStart=_82;
this._dragYStart=_83;
this._leftStart=parseInt(computedStyle(this.elementToMove,"left"),10);
this._topStart=parseInt(computedStyle(this.elementToMove,"top"),10);
if((isNaN(this._leftStart)||isNaN(this._topStart))){
logger.error("Can't start the drag for "+repr(this)+" "+"Either the left or the top of the dragged element is not a number "+"left: "+this._leftStart+" top: "+this._topStart);
return;
}
signal(this,"dragStarted");
},"move":function(_84,_85){
if(this._disabled){
return;
}
if((this.flags&UI.Draggable.DRAG_X)>0){
var _86=(this._leftStart+_84-this._dragXStart);
if(this.leftLimits){
if(_86<this.leftLimits[0]){
_86=this.leftLimits[0];
}
if(_86>this.leftLimits[1]){
_86=this.leftLimits[1];
}
}
if(!isNaN(_86)){
this.elementToMove.style.left=_86+"px";
}else{
logger.error("Draggable.move: newLeft isNaN");
}
}
if((this.flags&UI.Draggable.DRAG_Y)>0){
var _87=(this._topStart+_85-this._dragYStart);
if(this.topLimits){
if(_87<this.topLimits[0]){
_87=this.topLimits[0];
}
if(_87>this.topLimits[1]){
_87=this.topLimits[1];
}
}
if(!isNaN(_87)){
this.elementToMove.style.top=_87+"px";
}else{
logger.error("Draggable.move: newTop isNaN");
}
}
signal(this,"dragging");
},"stop":function(){
var e=e||window.event;
UI.Draggable._draggable=null;
signal(this,"dragFinished");
},"_installMouseDown":function(){
var _88=this.element.onmousedown;
var _89=this;
this.element.onmousedown=function(e){
var e=e||window.event;
_89.startFromEvent(e);
if(_88){
_88.apply(this.element,arguments);
}
};
},"enable":function(){
this._disabled=false;
},"disable":function(){
this._disabled=true;
}};
document.onmousemove=function(e){
var e=e||window.event;
var x=e.screenX;
var y=e.screenY;
if(UI.Draggable._draggable){
UI.Draggable._draggable.move(x,y);
}
if(UI.Draggable._oldonmousemove){
_oldmousemove.apply(document,arguments);
}
};
document.onmouseup=function(e){
if(UI.Draggable._draggable){
UI.Draggable._draggable.stop(e);
}
if(UI.Draggable._oldonmouseup){
_oldonmouseup.apply(document,arguments);
}
};
UI.Table=function(_90,_91){
bindMethods(this);
this.element=$(_90);
this.selectedRow=-1;
this._modelRowIndexes=[];
this._bodyRowIndexes=[];
this._selectedTR=null;
this._highlightedTR=null;
this._sortCol=-1;
this._arrow=SPAN(null);
this._model=null;
this.cssClass="uitable";
this.register();
if(_91){
this.setModel(_91);
}
this.NAME=this.element.id+"(UI.Table)";
};
UI.Table._NO_ARROW="&nbsp;&nbsp;&nbsp;";
UI.Table._DOWN_ARROW="&nbsp;&nbsp;&darr;";
UI.Table._UP_ARROW="&nbsp;&nbsp;&uarr;";
UI.Table.prototype=update(new UI.Widget(),{"setModel":function(_92){
this._model=_92;
connect(_92,"changed",this,"render");
this.render();
},"model":function(){
return this._model;
},"render":function(){
if(!this._model){
logError("Can't render a table without model");
return;
}
var _93=this.getTableElement();
if(_93){
swapDOM(_93,null);
}
var _94=[];
if(this._model.hasHeader()){
_94.push(THEAD(null,TR(null,map(this._makeTH,this._model.getHeaders(),range(0,this._model.getNumCols())))));
}
if(this._model.hasFooter()){
_94.push(TFOOT(null,TR(null,map(partial(TD,null),this._model.getFooters()))));
}
var _95=TABLE(null,_94,TBODY(null,map(this._makeTR,this._model.getRows())));
this.element.appendChild(_95);
this._initIndexesMaps();
},"_initIndexesMaps":function(){
this._bodyRowIndexes=[];
this._modelRowIndexes=[];
for(var i=0;i<this._model.getNumRows();i++){
this._bodyRowIndexes.push(i);
this._modelRowIndexes.push(i);
}
},"getTableElement":function(){
return this.element.getElementsByTagName("table")[0];
},"_makeTH":function(_96,_97){
var th=TH(null,_96);
var _99=this;
th.onclick=function(e){
_99.clickHeader(_97,e||window.event);
};
return th;
},"_makeTR":function(row){
var tr=TR(null,map(this._makeTD,row,this._model.getColTypes()));
var _102=this;
tr.onclick=function(e){
_102.clickRow(_102.modelRowIndex(tr.sectionRowIndex),e||window.event);
};
tr.onmouseover=function(e){
_102.mouseOverRow(_102.modelRowIndex(tr.sectionRowIndex),e||window.event);
};
tr.onmouseout=function(e){
_102.mouseOutRow(_102.modelRowIndex(tr.sectionRowIndex),e||window.event);
};
signal(this,"rowAdded",tr);
return tr;
},"_makeTD":function(cell,type){
switch(type){
case "rawhtml":
var td=TD(null);
td.innerHTML=cell;
return td;
default:
return TD(null,cell);
}
},"clickRow":function(_106,_107){
this.selectRow(_106);
signal(this,"rowClicked",_106,_107);
},"clickHeader":function(_108,_109){
var _110=this.getTH(_108);
var _111=_110.getAttribute("_order")||"asc";
var _112=_111=="asc"?"desc":"asc";
_110.setAttribute("_order",_112);
this.sort(_108,_112=="desc");
if(_112=="asc"){
this._arrow.innerHTML=UI.Table._DOWN_ARROW;
}else{
this._arrow.innerHTML=UI.Table._UP_ARROW;
}
_110.appendChild(this._arrow);
signal(this,"headerClicked",_108,_109);
},"mouseOverRow":function(_113,_114){
this.highlightRow(_113);
signal(this,"rowMouseOver",_113,_114);
},"mouseOutRow":function(_115,_116){
this.highlightRow(-1);
signal(this,"rowMouseOut",_115,_116);
},"selectRow":function(_117){
if(this._selectedTR){
removeElementClass(this._selectedTR,"ui_active");
}
var _118=this.getTR(_117);
if(_118){
addElementClass(_118,"ui_active");
this._selectedTR=_118;
this.selectedRow=_117;
}
signal(this,"rowSelected",_117);
},"highlightRow":function(_119){
if(this._highlightedTR){
removeElementClass(this._highlightedTR,"ui_hover");
}
var _120=this.getTR(_119);
if(_120){
addElementClass(_120,"ui_hover");
this._highlightedTR=_120;
}
},"modelRowIndex":function(_121){
return this._modelRowIndexes[_121];
},"bodyRowIndex":function(_122){
return this._bodyRowIndexes[_122];
},"getTR":function(_123){
var _124=this.bodyRowIndex(_123);
if(_124>=0){
return this.getTableElement().tBodies[0].rows[_124];
}else{
return null;
}
},"getTH":function(_125){
if(_125>=0){
return this.getTableElement().tHead.rows[0].cells[_125];
}else{
return null;
}
},"_sortDate":function(a,b){
aa=scrapeText(a.cells[this.sortCol]);
bb=scrapeText(b.cells[this.sortCol]);
if(aa.length==10){
dt1=aa.substr(6,4)+aa.substr(3,2)+aa.substr(0,2);
}else{
yr=aa.substr(6,2);
if(parseInt(yr)<50){
yr="20"+yr;
}else{
yr="19"+yr;
}
dt1=yr+aa.substr(3,2)+aa.substr(0,2);
}
if(bb.length==10){
dt2=bb.substr(6,4)+bb.substr(3,2)+bb.substr(0,2);
}else{
yr=bb.substr(6,2);
if(parseInt(yr)<50){
yr="20"+yr;
}else{
yr="19"+yr;
}
dt2=yr+bb.substr(3,2)+bb.substr(0,2);
}
if(dt1==dt2){
return 0;
}
if(dt1<dt2){
return -1;
}
return 1;
},"_sortCurrency":function(a,b){
aa=scrapeText(a.cells[this.sortCol]).replace(/[^0-9.]/g,"");
bb=scrapeText(b.cells[this.sortCol]).replace(/[^0-9.]/g,"");
return parseFloat(aa)-parseFloat(bb);
},"_sortNumeric":function(a,b){
aa=parseFloat(scrapeText(a.cells[this.sortCol]));
if(isNaN(aa)){
aa=0;
}
bb=parseFloat(scrapeText(b.cells[this.sortCol]));
if(isNaN(bb)){
bb=0;
}
return aa-bb;
},"_sortString":function(a,b){
var aa=scrapeText(a.cells[this.sortCol]).toLowerCase();
var bb=scrapeText(b.cells[this.sortCol]).toLowerCase();
if(aa==bb){
return 0;
}
if(aa<bb){
return -1;
}
return 1;
},"_sortStringCaseSensitive":function(a,b){
aa=scrapeText(a.cells[this.sortCol]);
bb=scrapeText(b.cells[this.sortCol]);
if(aa==bb){
return 0;
}
if(aa<bb){
return -1;
}
return 1;
},"sort":function(_130,_131){
_130=_130||0;
_131=_131||false;
this.sortCol=_130;
var _132=this._model.getColType(_130)||"string";
var _133="_sort"+_132.charAt(0).toUpperCase()+_132.substring(1);
if(!this[_133]){
logError("UI.Table.sort: Type "+_132+" unrecognized");
return;
}
var _134=this.getTableElement();
var _135=new Array();
for(var i=0;i<_134.tBodies[0].rows.length;i++){
_135[i]=_134.tBodies[0].rows[i];
_135[i]._modelIndex=this.modelRowIndex(i);
}
_135.sort(this[_133]);
for(var i=0;i<_135.length;i++){
if(!_131){
_134.tBodies[0].appendChild(_135[i]);
}else{
_134.tBodies[0].appendChild(_135[_135.length-1-i]);
}
this._modelRowIndexes[i]=_135[i]._modelIndex;
this._bodyRowIndexes[_135[i]._modelIndex]=i;
try{
delete _135[i]._modelIndex;
}
catch(e){
_135[i]._modelIndex=null;
}
}
}});
UI.Table._fromElement=function(_136){
var _137=new UI.Table(_136.id||_136.getAttribute("id"));
var _138=_136.getAttribute("ui:model");
if(!_138){
var _139=_136.getElementsByTagName("table");
if(_139&&_139.length>0){
_137.setModel(new UI.HTMLTableModel(_139[0]));
}
return;
}else{
_137.setModel(eval("("+_138+")"));
return;
}
};
UI.Slider=function(_140,_141,_142,_143){
bindMethods(this);
this.element=$(_140);
this.minValue=_141||0;
this.maxValue=_142||100;
this.value=_141;
this.linkedInput=null;
var _144=this.element.getElementsByTagName("div");
if(!_144||_144.length==0){
this.element.appendChild(DIV(null," "));
_144=this.element.getElementsByTagName("div");
}
var _145=_144[0];
this._draggableWidth=parseInt(computedStyle(_145,"width"),10);
this._maxLeft=parseInt(computedStyle(this.element,"width"),10)-this._draggableWidth;
this.draggable=new UI.Draggable(_145,UI.Draggable.DRAG_X,[0,this._maxLeft]);
connect(this.draggable,"dragging",this,"_updateValue");
this._connectWithClicks();
this.cssClass="uislider";
this.register();
this._updateValue();
if(_143){
this.linkWithInput(_143);
_143.value=this.value;
}
this.NAME=this.element.id+"(UI.Slider)";
};
UI.Slider.prototype=update(new UI.Widget(),{"_updateValue":function(left){
var _147=this.value;
if(arguments.length==0){
left=parseInt(computedStyle(this.draggable.element,"left"),10);
}
this.value=Math.round((left/this._maxLeft)*(this.maxValue-this.minValue)+this.minValue);
if(this.value!=_147){
signal(this,"valueChanged",this.value);
if(this.linkedInput){
this.linkedInput.value=this.value;
}
}
},"_click":function(_148,_149){
var _150=elementPosition(this.element).x;
var _151=(_148-_150-this._draggableWidth/2);
this.setValue(parseFloat((_151/this._maxLeft)*(this.maxValue-this.minValue))+this.minValue);
},"setValue":function(_152){
var _153=this.value;
if(_152>this.maxValue){
_152=this.maxValue;
}
if(_152<this.minValue){
_152=this.minValue;
}
var left=Math.round(((_152-this.minValue)/(this.maxValue-this.minValue))*this._maxLeft);
this.draggable.element.style.left=left;
this.draggable.element.style.left=left+"px";
this._updateValue(left);
},"_connectWithClicks":function(){
var _154=this;
connect(this.element,"onclick",function(e){
var _155=e.mouse();
_154._click(_155.page.x,_155.page.y);
});
connect(this.draggable.element,"onclick",function(e){
e.stop();
return false;
});
},"linkWithInput":function(_156){
this.linkedInput=_156;
this.linkedInput.value=this.value;
var _157=this;
connect(_156,"onchange",function(e){
var val=parseInt(_156.value,10);
if(!isNaN(val)){
_157.setValue(val);
}
});
}});
UI.Slider._fromElement=function(_158){
var _159=getNodeAttribute(_158,"ui:minvalue")||0;
var _160=getNodeAttribute(_158,"ui:maxvalue")||0;
var _161=getNodeAttribute(_158,"ui:input");
var _162=new UI.Slider(_158,parseInt(_159,10),parseInt(_160,10));
if(_161){
_162.linkWithInput($(_161));
}
};
UI.Form=function(_163,_164,_165){
bindMethods(this);
this.element=$(_163);
this.items=_164||[];
this.validators=_165||[];
this.cssClass="uiform";
this._invalidInputs=[];
this.register();
this.NAME=this.element.id+"(UI.Form)";
var _166=_163.onsubmit;
var form=this;
_163.onsubmit=function(){
if(!form.validate()){
return false;
}
if(!_166){
return true;
}else{
return _166();
}
};
};
UI.Form.VALIDATION_PASSED="";
UI.Form.Messages={"REQUIRED":_("The field is required"),"NOT_VALID":_("The field value is not valid"),"NUMBER":_("The value must be a number"),"ALPHA":_("The value must contain only letters"),"ALPHANUM":_("The value must contain only letters and numbers"),"ALPHASPACES":_("The value must contain only letters and spaces"),"ALPHANUMSPACES":_("The value must contain only letters, numbers and spaces"),"EMAIL":_("The value must be a valid email address")};
UI.Form.prototype=update(new UI.Widget(),{"render":function(){
this.element.appendChild(TABLE(null,TBODY(null,map(function(i){
return i.render();
},this.items))));
},"validate":function(){
this._invalidInputs=[];
var _168=true;
for(var i=0;i<this.items.length;i++){
if(this.items[i].inputs){
for(var j=0;j<this.items[i].inputs.length;j++){
if(this.items[i].inputs[j]){
this.items[i].inputs[j].validate();
if(!this.items[i].inputs[j].valid){
this._invalidInputs.push(this.items[i].inputs[j].element);
_168=false;
}
}
}
}
}
for(var i=0;i<this.validators.length;i++){
var errs=this.validators[i](this.element);
var form=this;
if(errs&&errs.length){
_168=false;
forEach(errs,function(err){
var _172=err.fields;
var msg=err.message;
forEach(_172,function(_174){
form._invalidInputs.push(_174);
});
});
}
}
if(_168){
signal(this,"validationPassed");
}else{
signal(this,"validationFailed");
}
return _168;
},"submitAsync":function(url,_175,_176,_177){
if(!this.validate()){
return null;
}
signal(this,"submitted");
var _175=_175||[];
var _176=_176||[];
var _177=_177||"GET";
var url=url||this.element.action;
if(url){
var _178=formContents(this.element);
var _179=_178[0];
var _180=_178[1];
extend(_179,_175);
extend(_180,_176);
var d=doSimpleXMLHttpRequest(url,_179,_180);
signal(this,"sent",_179,_180);
return d;
}
return fail("UI.Form.submitAsync: No url given and url autodetection failed");
},"invalidInputs":function(){
return this._invalidInputs;
}});
UI.Form.Error=function(msg){
this.message=msg;
this.fields=extend([],arguments,1);
};
UI.FormItem=function(_181,_182,_183,flow){
bindMethods(this);
this.element=$(_181);
this.label=_182||"";
this.inputs=_183||[];
this.flow=flow||"horizontal";
};
UI.FormItem.prototype={"render":function(){
var _185=filter(function(el){
return el.nodeType>0;
},this.element.childNodes);
if(_185&&_185.length){
var _186={"class":"noborderspace"};
if(this.flow=="horizontal"){
this.element.appendChild(TABLE(_186,TBODY(null,TR(_186,map(partial(TD,_186),_185)))));
}else{
this.element.appendChild(TABLE(_186,TBODY(null,map(function(el){
return TR(_186,TD(_186,el));
},_185))));
}
}
return TR(null,TD({"align":"right"},LABEL(null,this.label!=""?this.label+":":"")),TD(null,this.element));
}};
UI.FormInput=function(_187,_188){
bindMethods(this);
this.element=$(_187);
this.validators=_188;
this.cssClass="uiforminput";
this.valid=true;
this.tip=null;
this.register();
this._connectEvents();
};
UI.FormInput.prototype=update(new UI.Widget(),{"validate":function(){
var _189=this.element;
this.unmarkError();
this.valid=true;
if(!this.validators){
return;
}
for(var i=0;i<this.validators.length;i++){
var msg=this.validators[i](this.element);
if(msg&&(msg!=UI.Form.VALIDATION_PASSED)){
this.markError(msg);
return false;
}
}
return true;
},"markError":function(msg){
addElementClass(this.element,"uierror");
var _190=elementPosition(this.element);
var _191=elementDimensions(this.element);
if(typeof (_190.x)!="undefined"&&typeof (_191.w)!="undefined"){
this.tip=DIV({"class":"uitip"},DIV({"class":"uiarrow"}),DIV({"class":"uimsg"},msg));
this.tip.style.left=(_190.x+_191.w)+"px";
this.tip.style.top=(_190.y)+"px";
hideElement(this.tip);
document.getElementsByTagName("body")[0].appendChild(this.tip);
connect(this.element,"onmouseover",this,"showTip");
connect(this.element,"onmouseout",this,"hideTip");
}else{
logWarning("FormInput.markError: Can't get element position and/or dimensions");
}
this.valid=false;
},"showTip":function(){
showElement(this.tip);
},"hideTip":function(){
hideElement(this.tip);
},"unmarkError":function(){
removeElementClass(this.element,"uierror");
if(this.tip){
disconnect(this.element,"onmouseover",this,"showTip");
disconnect(this.element,"onmouseout",this,"hideTip");
removeElement(this.tip);
this.tip=null;
this.element.onmouseover=null;
this.element.onmouseout=null;
}
},"_connectEvents":function(){
if(!this.element){
return;
}
var _192=this.element.onblur;
var _193=this.element.onfocus;
var _194=this;
this.element.onblur=function(){
_194.validate();
if(_192){
_192.apply(this.element,arguments);
}
};
this.element.onfocus=function(){
_194.unmarkError();
if(_193){
_193.apply(this.element,arguments);
}
};
}});
UI.SelectFormInput=function(_195,_196,_197){
bindMethods(this);
this._model=null;
this.element=$(_195);
this.cssClass="uiselectforminput";
this.register();
this.setModel(_197);
};
UI.SelectFormInput.prototype=update(new UI.FormInput(),{"setModel":function(_198){
disconnect(this.model,"changed",this,"render");
this._model=_198;
this.render();
connect(_198,"changed",this,"render");
},"model":function(){
return this._model;
},"render":function(){
replaceChildNodes(this.element,[]);
for(var i=0;i<this._model.getLength();i++){
this.element.appendChild(OPTION({"value":this._model.getValue(i)},this._model.getLabel(i)));
}
}});
UI.Form.Validators={};
UI.Form.Validators.required=function(el){
return el.value.match(/^\s*$/)?UI.Form.Messages.REQUIRED:UI.Form.VALIDATION_PASSED;
};
UI.Form.Validators.regexp=function(re,msg){
return function(el){
return el.value.match(re)?UI.Form.VALIDATION_PASSED:msg||UI.Form.Messages.NOT_VALID;
};
};
UI.Form.Validators.numeric=function(el){
var val=el.value.replace(/,/,"").replace(/\./,"");
return (isNaN(val))?UI.Form.Messages.NUMBER:UI.Form.VALIDATION_PASSED;
};
UI.Form.Validators.alpha=UI.Form.Validators.regexp(/^[A-Za-záé�óúñ]*$/,UI.Form.Messages.ALPHA);
UI.Form.Validators.alphaspaces=UI.Form.Validators.regexp(/^[A-Za-záé�óúñ\s]*$/,UI.Form.Messages.ALPHASPACES);
UI.Form.Validators.alphanum=UI.Form.Validators.regexp(/^[0-9A-Za-áé�óúñ]*$/,UI.Form.Messages.ALPHANUM);
UI.Form.Validators.alphanumspaces=UI.Form.Validators.regexp(/^[0-9A-Za-záé�óúñ\s]*$/,UI.Form.Messages.ALPHANUMSPACES);
UI.Form.Validators.email=UI.Form.Validators.regexp(/^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[A-Za-z]{2,4}$/,UI.Form.Messages.EMAIL);
UI.FormInput._getValidators=function(el){
var _200=el.getAttribute("ui:validators");
if(_200){
with(UI.Form.Validators){
_200=eval("("+_200+")");
}
}else{
_200=[];
}
return _200;
};
UI.FormInput._fromElement=function(el){
return new UI.FormInput(el,UI.FormInput._getValidators(el));
};
UI.SelectFormInput._fromElement=function(el){
var _201=el.getAttribute("ui:model");
if(_201){
_201=eval("("+_201+")");
return new UI.SelectFormInput(el,UI.FormInput._getValidators(el),_201);
}else{
_201=new UI.HTMLSelectListModel(el.cloneNode(true));
var _202=new UI.SelectFormInput(el,UI.FormInput._getValidators(el),_201);
_202.render();
return _202;
}
};
UI.FormItem._fromElement=function(el){
var _203=getNodeAttribute(el,"ui:label");
var _204=[];
if(el.tagName.toLowerCase()=="input"){
_204.push(UI.FormInput._fromElement(el));
}else{
if(el.tagName.toLowerCase()=="select"){
_204.push(UI.SelectFormInput._fromElement(el));
}
}
var _205=el.getElementsByTagName("input");
if(_205&&_205.length){
_204=_204.concat(map(UI.FormInput._fromElement,_205));
}
var _206=el.getElementsByTagName("select");
if(_206&&_206.length){
_204=_204.concat(map(function(_207){
s=UI.SelectFormInput._fromElement(_207);
},_206));
}
return new UI.FormItem(el,_203,_204);
};
UI.Form._fromElement=function(el){
var _208=getNodeAttribute(el,"ui:keeplayout");
_208=(_208&&(_208=="true"));
var _209=getNodeAttribute(el,"ui:validators");
if(_209){
with(UI.Form.Validators){
_209=eval("("+_209+")");
}
}else{
_209=[];
}
var _210=filter(function(el){
return el.nodeType==1;
},el.childNodes);
var form=new UI.Form(el,map(UI.FormItem._fromElement,_210),_209);
if(!_208){
form.render();
}
return form;
};
UI.Accordion=function(_211,_212){
bindMethods(this);
this.element=$(_211);
this.elements=filter(this._elementNode,iter(this.element.childNodes));
var _213=this._elementNode;
forEach(this.elements,function(el){
addElementClass(el,"uiaccordiontitle");
var _214=filter(_213,el.childNodes);
addElementClass(_214[0],"uiaccordiontitlebar");
_214.splice(0,1);
forEach(_214,function(_215){
addElementClass(_215,"uiaccordioncontent");
hideElement(_215);
});
});
this._installOnClicks();
this.activeElements=[];
this.multipleExpansion=_212;
this.cssClass="uiaccordion";
this.collapseAll();
this.register();
this.NAME=this.element.id+"(UI.Accordion)";
};
UI.Accordion.prototype=update(new UI.Widget(),{"setMultipleExpansion":function(_216){
this.multipleExpansion=_216;
if(!_216&&this.activeElements.length>1){
this.collapseAll();
}
},"expand":function(_217){
var _218=filter(this._elementNode,_217.childNodes);
addElementClass(_218[0],"uiexpanded");
_218.splice(0,1);
forEach(_218,showElement);
var _219=findIdentical(this.activeElements,_217);
if(_219==-1){
this.activeElements.push(_217);
}
if(!this.multipleExpansion&&this.activeElements.length>1){
this.collapse(this.activeElements[0]);
}
},"expandAll":function(){
if(!this.multipleExpansion){
logError("UI.Accordion.expandAll: Can't expand all elements if not in multipleExpansion mode");
return;
}
forEach(this.elements,this.expand);
},"collapse":function(_220){
var _221=filter(this._elementNode,_220.childNodes);
removeElementClass(_221[0],"uiexpanded");
_221.splice(0,1);
forEach(_221,hideElement);
var _222=findIdentical(this.activeElements,_220);
if(_222!=-1){
this.activeElements.splice(_222,1);
}else{
logWarning("UI.Accordion.collapse: collapsing a non-expanded element!?");
}
},"collapseAll":function(){
forEach(extend(null,this.activeElements),this.collapse);
},"_installOnClicks":function(){
var _223=this;
forEach(this._titleBars(),function(_224){
connect(_224,"onclick",function(e){
var _225=findIdentical(_223.activeElements,_224.parentNode);
if(_225==-1){
_223.expand(_224.parentNode);
}else{
_223.collapse(_224.parentNode);
}
});
});
},"_elementNode":function(el){
return el.nodeType==1;
},"_firstChildElement":function(el){
return filter(this._elementNode,el.childNodes)[0];
},"_titleBars":function(){
return map(this._firstChildElement,this.elements);
}});
UI.Accordion._fromElement=function(el){
var _226=(getNodeAttribute(el,"ui:multiple")=="true");
new UI.Accordion(el,_226);
};
addLoadEvent(function(){
var _227=getElementsByTagAndClassName("div","uislider");
map(UI.Slider._fromElement,_227);
var _228=getElementsByTagAndClassName("div","uitable");
map(UI.Table._fromElement,_228);
var _229=getElementsByTagAndClassName("form","uiform");
map(UI.Form._fromElement,_229);
var _230=getElementsByTagAndClassName("div","uiwindow");
map(UI.Window._fromElement,_230);
var _231=getElementsByTagAndClassName("div","uiaccordion");
map(UI.Accordion._fromElement,_231);
});

