/**
 * @author Edward Sharp
 */
if (Object.isUndefined(Proto)) { var Proto = { } }

Proto.Tempslider = Class.create();
Proto.Tempslider.prototype = {
	initialize: function() {
		var e = function(new_value) {return new_value};
		this.options = Object.extend({
			container_id: 'tslider',
			initial_value: 15,
			min_value: 0,
			max_value: 100,
			onChange: e
		}, arguments[0] || { });
		this.value = this.options.initial_value;
		this.slide = $(this.options.container_id).down('.temp_bar');
		
		$(this.options.container_id).insert(new Element('div',{'id':'tsCursor'}));
		
		this.drawScale();
		
		this.slide.observe('click', function(e) {
			var cfraction = (Event.pointerY(e) - this.slide.getHeight()) / this.slide.getHeight();
			var ctemp = (1-cfraction) * (this.options.max_value - this.options.min_value) + this.options.min_value;
			ctemp = parseInt(ctemp*2)/2;
			this.options.onChange(ctemp);
			Event.stop(e);
			}.bind(this));
		
		this.refreshValue();
	},
	drawScale: function() {
		$(this.options.container_id)
			.insert(new Element('div',{'class':'tsLabel'})
				.setStyle({
					top:'-22px', 
					left:'3px',
					fontSize:'16px'})
				.update('&deg;C'));
		
		var max_val = this.options.max_value;
		var min_val = this.options.min_value;
		
		var approx_increment = (max_val - min_val) / 5;
		var increment = approx_increment - approx_increment % 5;
		
		if (increment == 0) {
			increment = 5;
		}

		if (min_val % 5 > 0) {
			min_val = min_val - min_val % 5 + 5;
		}
		
		for (var cur_temp = min_val; cur_temp <= this.options.max_value + 4; cur_temp += increment) {
			var display_temp = cur_temp;
			$(this.options.container_id)
				.insert(new Element('div',{'class':'tsLabel'})
					.setStyle({
						top:this._tempToYval(display_temp)-8+'px', 
						left:'-30px',
						fontSize:'16px'})
					.update(parseInt(display_temp)));
		}
	// end drawScale	
	},
	refreshValue: function() {
		this.updateCursor()
	// end refreshValue	
	},
	_tempToYval: function(temp) {
		return this.slide.getHeight() - parseInt(((temp - this.options.min_value) / (this.options.max_value - this.options.min_value)) * this.slide.getHeight());
	// end _modToXval()	
	},
	updateCursor: function() {
		var origin = this.slide.positionedOffset();
		
		$('tsCursor').setStyle({'left':origin[1]-3+'px'});
		$('tsCursor').setStyle({'top':origin[0] + this._tempToYval(this.value)-3+'px'});
	// end updateCursor
	},
	setValue: function(new_value) {
		if (new_value >= this.options.min_value && new_value <= this.options.max_value) {
			this.value = new_value;
			this.refreshValue();
			return true;
		}
		return false;
	// end setValue	
	},
	getValue: function() {
		return this.value;
	// end getValue
	}
};
