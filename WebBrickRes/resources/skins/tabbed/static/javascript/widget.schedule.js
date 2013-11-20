/**
 * @author Edward Sharp, Modifed Andy Harris added ';' in places and 'px' for top and left styles
 */

if (Object.isUndefined(Proto)) { var Proto = { } }

function doSend(zname,index,smod,day,t) {
    var days=['-M-----','--T----','---W---','----t--','-----F-','------s','S------','-------'] ;
    /*
     *  Two parts, one for the schedule and one for the device value.
     */
    var url = "/sendevent/schedule/"+zname+"/"+index+"/"+zname+"?type=http://id.webbrick.co.uk/events/config/set"+"&val="+t ;
    //alert ("First Sending"+url) ;
    doTimedXMLHttpRequest(url,pollerTimeout) ;
    url = "/sendevent/schedule/"+zname+"/"+index+"?type=http://id.webbrick.co.uk/events/config/set"+"&time="+formatTime(smod)+":00&day="+days[day] ;
    //alert ("Second Sending"+url) ;
    doTimedXMLHttpRequest(url,pollerTimeout) ;
}

function sendChanges(lObj) {
    /*
     *  Walk through list object to see if there are any changes
     *  we expect a global called schedule
     */
    //alert ("schedule3.t:"+schedule[3].t+"schedule3.smod:"+schedule[3].smod) ;
	for (var i = 0; i < lObj.length; i++) {
		    if (lObj[i]['index']!=-1) {
		        // previous data exists, compare to the point of difference then write and clear all others
		        if (lObj[i]['index'] != schedule[i].index) {
		                //alert("Found deleted value");
                        for (i=i; i < lObj.length; i++) {
                            //write the rest of the values out
                            //alert("Writing:"+ i +":" + lObj[i]['smod'] + ":" + lObj[i]['day'] + ":" + lObj[i]['t']);
	            	        doSend(sname,i,lObj[i]['smod'],lObj[i]['day'],lObj[i]['t']) ;
                            }
                    // write a blank in this position
                    //alert("removing:"+i);
		            doSend(sname,i,0,7,0) ; // 0-6 days 7 is no days
                    break;        		             
		            }
		        if (lObj[i]['smod'] != schedule[i].smod || lObj[i]['day'] != schedule[i].day || lObj[i]['t'] != schedule[i].t) {
		            // changed value
                    //alert("Writing Change :"+ i +":" + lObj[i]['smod'] + ":" + lObj[i]['day'] + ":" + lObj[i]['t']);
                    doSend(sname,i,lObj[i]['smod'],lObj[i]['day'],lObj[i]['t']) ;
		            }
		        }
		    else {
		        // new data, write at index [i]
		        //alert ("New:"+lObj[i]['smod']+":"+lObj[i]['day']+":"+lObj[i]['t']+": Index:"+i) ;
		        doSend(sname,i,lObj[i]['smod'],lObj[i]['day'],lObj[i]['t']) ;
		        
		        
		        }
		    
		    }
     
    }


function formatTime(mod) {
		var minutes = mod % 60;
		var hours = (mod - minutes) / 60;
		var hour_disp = (hours < 10) ? (hours == 0 ? '00' : '0' + hours) : hours;
		var min_disp = (minutes < 10) ? (minutes == 0 ? '00' : '0' + minutes) : minutes;
		return hour_disp + ":" + min_disp;
	}


Proto.Scheduler = Class.create();
Proto.Scheduler.prototype = {
	initialize: function() {
		var e = Prototype.emptyFunction;
		this.options = Object.extend({
			editor_id: 'scheduler',
			dow_abbrs: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday'],
			window_data: [],
			gradient: {coolpoint:20,hotpoint:40},
			gradient_cold: [89, 126, 226],
			gradient_hot: [189, 0, 21],
			day_ruler_size: 550
		}, arguments[0] || { });
		
		this.updateSlotData();
		this.createUndoData();
		
		this.cur_slot = Object.clone(this.options.window_data[0]);
		this.sel_window_id = null;
		this.changed_since_commit = false;

	// end initialize
	},
	createUndoData: function() {
		this.undo_window_data = [];
		this.options.window_data.each(function(wd) {
			this.undo_window_data.push(Object.clone(wd));
		}.bind(this));
		
	// end createUndoData
	},
	restoreUndoData: function() {
		this.options.window_data = [];
		this.undo_window_data.each(function(wd) {
			this.options.window_data.push(Object.clone(wd));
		}.bind(this));
		
	// end restoreUndoData
	},
	sortWindowData: function() {
			var sort_func = function (a,b) {
				var val_a = a['day'] * 1440 + a['smod'];
				var val_b = b['day'] * 1440 + b['smod'];
				return (val_b < val_a) - (val_a < val_b);
			// end asc()	
			}
			
			this.options.window_data.sort(sort_func);
	// end sortWindowData
	},
	updateSlotData: function() {
		this.sortWindowData();
		var cur_win_id = 1;
		this.slot_data = [];
		cur_t = this.options.window_data[0]['t'];
		
		for (var day_index = 0; day_index <= 6; day_index++) {
			var day_slots = [];
			var slot = {'smod':0,'t':cur_t,'window_id':cur_win_id-1};
			
			while ((this.options.window_data[cur_win_id] != null) && (this.options.window_data[cur_win_id]['day'] == day_index)) {
				var cur_window = this.options.window_data[cur_win_id];
				slot['emod'] = cur_window['smod'];
				day_slots.push(slot);
				var slot = {'smod':cur_window['smod'],'window_id':cur_win_id,'t':cur_window['t']};
				cur_t = cur_window['t'];
				cur_win_id++;
			}
			slot['emod'] = 1440;
			day_slots.push(slot);
			this.slot_data.push(day_slots);
		}

	// end updateSlotData
	},
	formatTime: function(mod) {
		var minutes = mod % 60;
		var hours = (mod - minutes) / 60;
		var hour_disp = (hours < 10) ? (hours == 0 ? '00' : '0' + hours) : hours;
		var min_disp = (minutes < 10) ? (minutes == 0 ? '00' : '0' + minutes) : minutes;
		return hour_disp + ":" + min_disp;
	// end formatTime	
	},
	formatTemp: function(t) {
		return parseInt(t) + '.' + Math.round(t % 1 * 10)
	// end formatTemp	
	},
	createDayRuler: function () {
		var ruler_div = new Element('div', {'class':'twTimeRuler'});
		for (var mod = 0; mod <= 1450; mod += 180) {
				ruler_div.insert(new Element('div', {'class':'twTimeRulerLabel'})
					.insert(this.formatTime(mod))
					.setStyle({'left':this._modToXval(mod) + 'px'})
					);
		}		
		return ruler_div;
	// end createDayRuler()	
	},
	_modToXval: function(mod) {
		return parseInt((mod / 1440) * this.options.day_ruler_size);
	// end _modToXval()	
	},
	createDaySlots: function (day_index) {
		var day_div = new Element('div', {'class':'twDayDiv','id':'day_'+day_index})
							.setStyle({'width':this.options.day_ruler_size + 'px'});

		return day_div;
	// end createDaySlots()	
	},
	clearDaySlots: function (day_index) {
		$('day_'+day_index).update();
	// end clearDaySlots()
	},
	displayDaySlot: function (id, day_index, tw) {
		var smod = tw['smod'];
		var emod = tw['emod'];
		var window_id = tw['window_id'];
		var t = tw['t'];
		
		// Set variables for calculating bg color
		var cp = this.options.gradient['coolpoint'];
		var hp = this.options.gradient['hotpoint'];
		
		var bgcolarray = [0,0,0];
		var chot = this.options.gradient_hot;
		var ccold = this.options.gradient_cold;
		
		// Use linear interpolation to calculate RGB value based on hot and cold points
		bgcolarray.each(function(val,index) {
			bgcolarray[index] = parseInt((Math.max(Math.min(t,hp)-cp,0))/(hp-cp)*(chot[index]-ccold[index]) + ccold[index]);
		}.bind(this));
		
		var bgcol = 'rgb(' + bgcolarray[0] + ',' + bgcolarray[1] + ',' + bgcolarray[2] + ')';
		
		day_div = $('day_'+day_index);
		slot_div = new Element('div', {'class':'twTimeSlot', 'id':'slot_' + day_index + '_' + id})
			.insert(new Element('div',{'class':'twSlotT'}).insert(this.formatTemp(t)))
			.insert(new Element('div',{'class':'twSlotStartTime'}).insert(this.formatTime(smod)))
			.insert(new Element('div',{'class':'twSchedEnd'}))
			.setStyle({'left':this._modToXval(smod) + 'px'})
			.setStyle({'width':this._modToXval(emod-smod) + 'px'})
			.setStyle({'backgroundColor':bgcol})
			.observe('click', function(e) {
				var cmod = parseInt((Event.pointerX(e) - $('day_0').cumulativeOffset()[0]) / this.options.day_ruler_size * (24*60));
				var dow_height = ($('day_6').cumulativeOffset()[1] - $('day_0').cumulativeOffset()[1]) / 6;
				var cdow = parseInt((Event.pointerY(e) - $('day_0').cumulativeOffset()[1]) / dow_height );
				this._clickSlot(window_id, cmod, cdow);
				Event.stop(e);
				}.bind(this));
		if (false) {
			slot_div.addClassName('twSlotSel')
				.setStyle({'left':this._modToXval(smod) - 6 + 'px'})
		}			
		day_div.insert(slot_div);
	// end displayDaySlot()	
	},
	_clickSlot: function (window_id, cmod, cdow) {
		// if (this.changed_since_commit) {
		// 	alert("Click 'done' or 'cancel'");
		// 	return;
		// }
		
		if (this.sel_window_id == null) {
			// See if the click was near the start of the slot that observed the event
			if (cdow == this.options.window_data[window_id]['day'] && Math.abs(cmod - this.options.window_data[window_id]['smod']) < 30) {
				this.cur_slot = this.options.window_data[window_id];
				this.sel_window_id = window_id;
				this.createUndoData();
				this.refreshAllDaySlots();
				document.fire('scheduler:timeslot_selected');
				return;
			} 
			// If this isn't the last slot, see if the click was near the start of the next slot
			if (window_id < this.options.window_data.size() - 1) {
				if (cdow == this.options.window_data[window_id+1]['day'] && Math.abs(cmod - this.options.window_data[window_id+1]['smod']) < 15) {
					this.cur_slot = this.options.window_data[window_id+1];
					this.sel_window_id = window_id + 1;
					this.createUndoData();
					this.refreshAllDaySlots();
					document.fire('scheduler:timeslot_selected');
					return;
				}
			}
			
			// Not clicked near a start or end so just update cursor
			this.setDOW(cdow);
			// Quantize to 15 mins
			this.setSMod(parseInt(cmod/15)*15);
		
		} else {
			this.setDOW(cdow);
			// Quantize to 15 mins
			this.setSMod(parseInt(cmod/15)*15);
		}
		
	// end _clickSlot	
	},
	refreshDaySlots: function (day_index) {
		this.clearDaySlots(day_index);
		day_div = $('day_'+day_index);
		this.slot_data[day_index].each(function(tw, index) {
			this.displayDaySlot(index,day_index,tw);
		// each tw	
		}.bind(this));		
	// end refreshDaySlots()	
	},
	createBody: function () {
		var tbody = new Element('tbody');
		var tr = new Element('tr');
		//tr.insert(new Element('td'));
		tr.insert(new Element('td').insert(this.createDayRuler()));
		tbody.insert(tr);
		
		this.options.dow_abbrs.each(function(abbr,index){
			var tr = new Element('tr', {'class':'twDay'});
			tr.insert(new Element('td', {'class':'twDayLabel'}).insert(abbr));
			tr.insert(new Element('td').insert(this.createDaySlots(index)));
			tbody.insert(tr);
		// end dow_abbrs.each			
		}.bind(this));
		
		return tbody;
	// end createBody	
	},
	drawControl: function () {
		var table = new Element('table');
		table.insert(this.createBody());
		$(this.options.editor_id).update(new Element('div',{'id':'twCursor'}));
		$(this.options.editor_id).insert(table);
		
		this.refreshAllDaySlots();
	// end drawControl()	
	},
	updateCursor: function() {
		var day = this.cur_slot['day'];
		var smod = this.cur_slot['smod'];
		var origin = $('day_' + day).positionedOffset();
		$('twCursor').setStyle({'top':origin[1]-3+'px'});
		$('twCursor').setStyle({'left':origin[0] + this._modToXval(smod)-3+'px'});

		$('twCursor').addClassName('cursor');
		if (this.sel_window_id == null) {
			$('twCursor').removeClassName('selected')
		} else {
			$('twCursor').addClassName('selected')
		}
	// end updateCursor
	},
	addSlot: function () {
		var day_index = this.cur_slot['day'];
		var smod = this.cur_slot['smod'];
		var t = this.cur_slot['t'];
		
		var skipnew = false;
		this.options.window_data.each(function(tw) {
			if (smod == tw['smod'] && day_index == tw['day']) {
				skipnew = true;
			}
		// end tw.each	
		})
		
		if (!skipnew) {
			this.options.window_data.push({
				'day':day_index,
				'smod': smod,
				't': t,
				'index': -1
			});
			
			this.sel_window_id = this.options.window_data.size() - 1;
			this.cur_slot = this.options.window_data[this.sel_window_id];
		}
		
		this.refreshAllDaySlots();
		
		document.fire('scheduler:window_data_updated');
		
	// end addSlot()	
	},
	removeSlot: function () {
		var new_tws = new Array();
		this.options.window_data.each(function(tw, index) {
			if (index != this.sel_window_id) {
				new_tws.push(tw);
			}
		// end window_data.each	
		}.bind(this));
		
		this.options.window_data = new_tws;		
		this.clearSelSlot();
		this.refreshAllDaySlots();
		
		document.fire('scheduler:window_data_updated');
		
	// end removeSlot()	
	},
	getWindowData: function () {
		return Object.toJSON(this.options.window_data);
	// end getWindowData()
	},
	refreshAllDaySlots: function () {
		this.updateSlotData();
		
		this.options.dow_abbrs.each(function(abbr,index){
			this.refreshDaySlots(index);
		// end dow_abbrs.each			
		}.bind(this));		
		
		this.updateCursor();
	// end refreshAllDaySlots	
	},
	_modClash: function(smod, day) {
		var clash = false;
		
		this.options.window_data.each(function(slot,id) {
			if (smod == slot['smod'] && day == slot['day']) {
				clash = true;
			}
		}.bind(this))
		
		return clash;
	// end _modClash
	},
	setSMod: function (new_value) {
		// Prevent user from changing window 0
		if (this.sel_window_id == 0) {
			return 0;
		}
		
		// Prevent user from setting start point to min 0 on day 0
		if (this.sel_window_id > 0 && new_value == 0 && this.cur_slot['day'] == 0) {
			return 15;
		}
		
		if (this._modClash(new_value,this.cur_slot['day']) && this.sel_window_id != null) {
			return this.cur_slot['smod'];
		}
		
		this.cur_slot['smod'] = new_value;
		if (this.sel_window_id != null) {
			this.changed_since_commit = true;
		}
		
		document.fire('scheduler:timeslot_updated');
		this.refreshAllDaySlots();
		
		return new_value;		
	// end setSMod
	},
	setDOW: function (new_value) {
		// Prevent user from changing window 0
		if (this.sel_window_id == 0) {
			return 0;
		}

		if (new_value == 0 && this.cur_slot['smod'] == 0 && this.sel_window_id > 0) {
			return this.cur_slot['day'];
		}
		
        if (this._modClash(this.cur_slot['smod'],new_value)  && this.sel_window_id > 0) {			return this.cur_slot['day'];
		}		
		
		this.cur_slot['day'] = new_value;
		if (this.sel_window_id != null) {
			this.changed_since_commit = true;
		}

		document.fire('scheduler:timeslot_updated');		
		this.refreshAllDaySlots();

		return new_value;
	// end setEMod
	},
	setT: function (new_value) {
		this.cur_slot['t'] = new_value;
		if (this.sel_window_id != null) {
			this.changed_since_commit = true;
		}

		document.fire('scheduler:timeslot_updated');		
		this.refreshAllDaySlots();
		
	// end setT
	},
	delSlot: function () {
		if (this.sel_window_id == null) return;
		
		if (this.sel_window_id == 0) return;
		
		this.changed_since_commit = true;
		this.removeSlot();
		this.clearSelSlot();
		this.commitChanges();
	// end delSlot	
	},
	clearSelSlot: function() {
		if (this.sel_window_id == null) return;

		this.cur_slot = Object.clone(this.cur_slot);
		this.sel_window_id = null;
	// end clearSelSlot
	},
	newSlot: function() {
		this.addSlot();

		this.changed_since_commit = true;
		this.refreshAllDaySlots();
	// end newSlot	
	},
	commitChanges: function() {
		this.changed_since_commit = false;
		this.createUndoData();
		this.clearSelSlot();
		this.refreshAllDaySlots();
	/* 
	 * now write out any changes to sendevent	
	 */
	    sendChanges(this.options.window_data);
	    
	// end commitChanges	
	},
	undoChanges: function() {
		this.changed_since_commit = false;
		this.restoreUndoData();
		this.clearSelSlot();
		this.refreshAllDaySlots();
		
		document.fire('scheduler:timeslot_updated');		
	},
	unsavedChanges: function() {
		return this.changed_since_commit;
	// end unsavedChanges	
	}
};
