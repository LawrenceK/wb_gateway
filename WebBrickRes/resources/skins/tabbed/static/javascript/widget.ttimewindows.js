/**
 * @author Edward Sharp
 */
if (Object.isUndefined(Proto)) { var Proto = { } }

Proto.TTimewindows = Class.create();
Proto.TTimewindows.prototype = {
	initialize: function() {
		var e = Prototype.emptyFunction;
		this.options = Object.extend({
			editor_id: 'scheduler',
			dow_abbrs: ['monday', 'tuesday', 'weds', 'thurs', 'friday','sat','sun'],
			window_data: [[],[],[],[],[],[],[]],
			initial_slot: {'smod':9*60, 'emod':17*60, 't':21.0, 'sel':false},
			day_ruler_size: 550
		}, arguments[0] || { });
		
		this.sel_day_index = null;
		this.sel_slot = this.options.initial_slot;
		this.sel_slot_id = {};

		var done = false;
		this.options.window_data.each(function(day_data,index) {
			if (day_data.size() > 0 && !done) {
				this.sel_day_index = index;
				this.sel_slot = day_data[0];
				day_data[0]['sel'] = true;
				this.sel_slot_id = {'day_index':index,'id':0};
				done = true;
			}
		}.bind(this))

	// end initialize
	},
	formatTime: function(mod) {
		var minutes = mod % 60;
		var hours = (mod - minutes) / 60;
		var hour_disp = (hours < 10) ? (hours == 0 ? '00' : '0' + hours) : hours;
		var min_disp = (minutes < 10) ? (minutes == 0 ? '00' : '0' + minutes) : minutes;
		return hour_disp + ":" + min_disp;
	// end formatTime	
	},
	createDayRuler: function () {
		var ruler_div = new Element('div', {'class':'twTimeRuler'});
		for (var mod = 0; mod <= 1410; mod += 180) {
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
							.setStyle({'width':this.options.day_ruler_size + 'px'})
							.observe('click', function(e) {
								this.clearSelSlot();
								this.sel_day_index = day_index;
								this.refreshAllDaySlots();
							}.bind(this));

		return day_div;
	// end createDaySlots()	
	},
	clearDaySlots: function (day_index) {
		$('day_'+day_index).update();
	// end clearDaySlots()
	},
	displayDaySlot: function (id, day_index, smod, emod, selected) {
		day_div = $('day_'+day_index);
		slot_div = new Element('div', {'class':'twTimeSlot', 'id':'slot_' + day_index + '_' + id})
			.insert(new Element('div',{'class':'twSlotStartTime'}).insert(this.formatTime(smod)))
			.insert(new Element('div',{'class':'twSlotEndTime'}).insert(this.formatTime(emod)))
			.setStyle({'left':this._modToXval(smod) + 'px'})
			.setStyle({'width':this._modToXval(emod-smod) + 'px'})
			.observe('click', function(e) {
				this._clickSlot(day_index,id);
				Event.stop(e);
				}.bind(this));
		if (selected) {
			slot_div.addClassName('twSlotSel')
				.setStyle({'left':this._modToXval(smod) - 6 + 'px'})
		}
		day_div.insert(slot_div);
	// end displayDaySlot()	
	},
	_clickSlot: function (day_index, id) {
		this.sel_day_index = day_index;

		this.options.window_data.each(function(wd, d_id) {
			wd.each(function(slot, s_id) {
				if((d_id == day_index) && (s_id == id)) {
					slot.sel = true;
					this.sel_slot = slot;
					this.sel_slot_id = {'day_index':d_id, 'id':s_id};
				} else {
					slot.sel = false;
				}
			}.bind(this))
			this.refreshDaySlots(d_id);
		}.bind(this))
		
		document.fire('scheduler:timeslot_selected');
		
	// end _clickSlot	
	},
	refreshDaySlots: function (day_index) {
		this.clearDaySlots(day_index);
		day_div = $('day_'+day_index);
		this.options.window_data[day_index].each(function(tw, index) {
			this.displayDaySlot(index,day_index,tw['smod'],tw['emod'],tw['sel']);
		// each tw	
		}.bind(this));		
		if (this.sel_day_index == day_index) {
			day_div.addClassName('twSelDay');
		} else {
			day_div.removeClassName('twSelDay');
		}
	// end refreshDaySlots()	
	},
	createBody: function () {
		var tbody = new Element('tbody');
		var tr = new Element('tr');
		tr.insert(new Element('td'));
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
		$(this.options.editor_id).update(table);
		
		this.refreshAllDaySlots();
	// end drawControl()	
	},
	addSlot: function (day_index, smod, emod, sel, t) {
		if (smod >= emod) {
			return false;
		}
		var new_tws = new Array();
		var skipnew = false;
		this.options.window_data[day_index].each(function(tw) {
			var skip = false;
			// new slot is entirely within old tw
			if ((tw['smod'] < smod && smod < tw['emod']) && (tw['smod'] < emod && emod < tw['emod'])) {
				skipnew = true;
			}
			// tw is entirely within new slot
			if ((smod <= tw['smod'] && tw['smod'] <= emod) && (smod <= tw['emod'] && tw['emod'] <= emod) ) {
				skip = true;
			}
			// tw ends within new slot, buts starts before
			if (smod <= tw['emod'] && tw['emod'] <= emod && tw['smod'] < smod) {
				skip = true;
				smod = tw['smod'];
			}
			// tw starts within new slot, buts ends after
			if (smod <= tw['smod'] && tw['smod'] <= emod && tw['emod'] > emod) {
				skip = true;
				emod = tw['emod'];
			}
			if (!skip) {
				new_tws.push(tw);
			}
		// end tw.each	
		})
		
		if (!skipnew) {
			new_tws.push({
				'smod': smod,
				'emod': emod,
				'sel': sel,
				't': t
			});
		}
		this.options.window_data[day_index] = new_tws;		
		
		this.refreshDaySlots(day_index);
		
		document.fire('scheduler:window_data_updated');
		
	// end addSlot()	
	},
	removeSlot: function (day_index, id) {
		var new_tws = new Array();
		this.options.window_data[day_index].each(function(tw, index) {
			if (index != id) {
				new_tws.push(tw);
			}
		// end window_data.each	
		})
		
		this.options.window_data[day_index] = new_tws;		
		this.refreshDaySlots(day_index);
		
		document.fire('scheduler:window_data_updated');
		
	// end removeSlot()	
	},
	getWindowData: function () {
		return Object.toJSON(this.options.window_data);
	// end getWindowData()
	},
	refreshAllDaySlots: function () {
		this.options.dow_abbrs.each(function(abbr,index){
			this.refreshDaySlots(index);
		// end dow_abbrs.each			
		}.bind(this));		
	// end refreshAllDaySlots	
	},
	_modInExistingWindow: function(mod, day_index) {
		var miew = false;
		
		this.options.window_data[day_index].each(function(slot,id) {
			if (mod >= slot['smod'] && mod <= slot['emod'] && id != this.sel_slot_id['id']) {
				miew = true;
			}
		}.bind(this))
		
		return miew;
	// end _modInExistingWindow
	},
	setSMod: function (new_value) {
		if (new_value >= this.sel_slot['emod'] || (this._modInExistingWindow(new_value,this.sel_day_index) && this.sel_slot_id['id'] != null)) {
			return this.sel_slot['smod'];
		}
		
		this.sel_slot['smod'] = new_value;
		
		document.fire('scheduler:timeslot_updated');
		if (this.sel_slot_id['id'] != null)
			this.refreshDaySlots(this.sel_slot_id['day_index']);
		return new_value;		
	// end setSMod
	},
	setEMod: function (new_value) {
		if (new_value <= this.sel_slot['smod'] || (this._modInExistingWindow(new_value,this.sel_day_index) && this.sel_slot_id['id'] != null)) {
			return this.sel_slot['emod'];
		}

		this.sel_slot['emod'] = new_value;

		document.fire('scheduler:timeslot_updated');		
		if (this.sel_slot_id['id'] != null)
			this.refreshDaySlots(this.sel_slot_id['day_index']);
		return new_value;
	// end setEMod
	},
	setT: function (new_value) {
		this.sel_slot['t'] = new_value;

		if (this.sel_slot_id['id'] != null)
			this.refreshDaySlots(this.sel_slot_id['day_index']);
		document.fire('scheduler:timeslot_updated');		
	// end setT
	},
	delSlot: function () {
		if (this.sel_slot_id['id'] == null) return;
		
		this.removeSlot(this.sel_slot_id['day_index'], this.sel_slot_id['id']);
		this.clearSelSlot();
	// end delSlot	
	},
	clearSelSlot: function() {
		if (this.sel_slot_id['id'] == null) return;

		this.sel_slot['sel'] = false;
		this.sel_slot = Object.clone(this.sel_slot);
		this.sel_slot_id = {};
	// end clearSelSlot
	},
	newSlot: function() {
		if (this.sel_slot_id['id'] != null || this.sel_day_index == null) return;
		
		this.addSlot(this.sel_day_index, this.sel_slot['smod'], this.sel_slot['emod'], false, this.sel_slot['t'])
		this.refreshAllDaySlots();
	// end newSlot	
	}
};