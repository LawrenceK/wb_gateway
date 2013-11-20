/*
 * @author Edward Sharp, Andy Harris added the curs_* functions for usability
 */

function curs_wait(obj,evt) {
    if (evt.preventDefault) evt.preventDefault();
    document.body.style.cursor = "wait" ;
    obj.style.cursor = "wait" ;
    document.observe('mouseout', curs_pointer.bind(obj));			    
}

function curs_pointer(obj) {
    document.body.style.cursor = "pointer" ;
    this.style.cursor = "pointer" ;
    document.stopObserving('mouseup');
}

function curs_clicked() {
    var box = document.getElementById("waitingBox") ;
    box.style.visibility = "visible";
    box.style.zIndex = "99";    
}


if (Object.isUndefined(Proto)) { var Proto = { } }

Proto.Spinner = Class.create();
Proto.Spinner.prototype = {
	initialize: function() {
		var e = function(new_value) {return new_value};
		this.options = Object.extend({
			spinner_container_id: 'spinner',
			live: false,
			initial_value: 15,
			min_value: 0,
			max_value: 100,
			large_increment: 10,
			small_increment: 1,
			onChange: e,
			onIncrement: e,
			onDecrement: e,
			format_value: e,
			refreshTime: 30,
			repeatPause: 0.5,
			repeatDelay: 0.1,
			sendDelay: 3
		}, arguments[0] || { });
		this.timer_id = null;
		this.changed = false;
		this.value = this.options.initial_value;
		this.value_div = $(this.options.spinner_container_id).down('.spinner_value');
		this.up_a = $(this.options.spinner_container_id).down('.spinner_up');
		this.down_a = $(this.options.spinner_container_id).down('.spinner_down');
		
        this.getValue(this);
		this.refreshValue();
		this.up_a.observe('mousedown', this._incValDown.bind(this));
		
		this.down_a.observe('mousedown', this._decValDown.bind(this));
		
		this.stop_periodical_inc = true;
		this.stop_periodical_dec = true;
	},
	doSend: function(obj) {
        if (obj.changed) {
            var url = "/sendevent/"+obj.options.spinner_container_id+"/manual/set?type=http://id.webbrick.co.uk/events/zones/manual"+"&val="+obj.value ;
            doTimedXMLHttpRequest(url,pollerTimeout) ;
            obj.changed = false ;
        }
    // end doSend
	},
	refreshValue: function() {
		this.value_div.update(this.options.format_value(this.value));

		window.clearTimeout(this.timer_id);
		if (this.options.live)
		    {
		    // only send if this is live data
		    this.timer_id = this.doSend.delay(this.options.sendDelay,this);
		    }

		window.clearTimeout(this.refresh_id);
		this.refresh_id = this.getValue.delay(this.options.refreshTime,this);
		
	// end refreshValue	
	},
	_incVal: function() {
		this.value += this.options.small_increment;
		if (this.value > this.options.max_value) {
			this.value = this.options.max_value;
		}
		this.value = this.options.onIncrement(this.value);
		this.value = this.options.onChange(this.value);
		this.refreshValue();
	// end _incVal
	},
	_decVal: function() {
		this.value -= this.options.small_increment;
		if (this.value < this.options.min_value) {
			this.value = this.options.min_value;
		}
		this.value = this.options.onDecrement(this.value);
		this.value = this.options.onChange(this.value);
		this.refreshValue();		
	// end _decVal	
	},
	_incValDown: function() {
		this.changed = true;
		this._incVal();
        document.observe('mouseup', this._incValUp.bind(this));
		this.stop_periodical_inc = false;
		var delayedRepeat = function() {
			new PeriodicalExecuter(function(pe) {
				if (this.stop_periodical_inc) {
					pe.stop();
				} else {
					this._incVal();
				}
			}.bind(this), this.options.repeatDelay);
		}.bind(this);
		delayedRepeat.delay(this.options.repeatPause);
	},
	_incValUp: function() {
		this.stop_periodical_inc = true;
		document.stopObserving('mouseup');
	},
	_decValDown: function() {
		this.changed = true;
		this._decVal();
        document.observe('mouseup', this._decValUp.bind(this));
		this.stop_periodical_dec = false;
		var delayedRepeat = function() {
			new PeriodicalExecuter(function(pe) {
				if (this.stop_periodical_dec) {
					pe.stop();
				} else {
					this._decVal();
				}
			}.bind(this), this.options.repeatDelay);
		}.bind(this);
		delayedRepeat.delay(this.options.repeatPause);
	},
	_decValUp: function() {
		this.stop_periodical_dec = true;
		document.stopObserving('mouseup');
	},
	setValue_orig: function(new_value) {
		if (new_value >= this.options.min_value && new_value <= this.options.max_value) {
			this.value = new_value;
			this.refreshValue();
			return true;
		}
		return false;
	// end setValue_orig	
	},
	
	setValue: function(obj,req) {
	    var response = req.responseXML.documentElement ;
        var new_value = getElementFloatByTagName(response, "val");
        if ( new_value != null )
            {
			obj.value = new_value;
			obj.refreshValue();
			return true;
			}
		else
		    {
		    return false;
		    }
	// end setValue	
	},
	getValue: function(obj) {
	    if (!obj.changed && obj.options.live) {
            var req = "/eventstate/"+obj.options.spinner_container_id+"/state?attr=targetsetpoint" ;
            var def = doTimedXMLHttpRequest(req, pollerTimeout) ;
            def.addBoth(obj.setValue, obj) ;
            return obj.value;
            }
	// end getValue
	}
};
