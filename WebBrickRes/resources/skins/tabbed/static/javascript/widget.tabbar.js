/**
 * @author Edward Sharp
 */
if (Object.isUndefined(Proto)) { var Proto = { } }

Proto.Tabbar = Class.create();
Proto.Tabbar.prototype = {
	initialize: function() {
		var e = Prototype.emptyFunction;
		this.options = Object.extend({
			tabbar_id: 'tabbar',
			tabs_data: [
				{
					label:'controls',
					href:'/'
				},
				{
					label:'status',
					href:'status.html'
				},
				{
					label:'history',
					href:'history.html'
				},
				{
					label:'solar',
					href:'solar.html'
				}
			]
		}, arguments[0] || { });
	// end initialize
	},
	drawWithActive: function(active_tab) {
		var tr = new Element('tr');

		if (active_tab == 0) {
			tr.insert(new Element('td',{'class':'tabtermla'}));
		} else {
			tr.insert(new Element('td',{'class':'tabtermli'}));
		}

		this.options.tabs_data.each(function(tab,index) {
			var isActive = (active_tab == index);

			// Insert mid-section of tab
			if (isActive) {
				tr.insert(new Element('td',{'class':'tabmida'}).insert(new Element('a',{'href':tab['href']}).insert(tab['label'])));
			} else {
				tr.insert(new Element('td',{'class':'tabmidi'}).insert(new Element('a',{'href':tab['href']}).insert(tab['label'])));
			}

			// Unless tab is last tab, add intermediate spacer
			if (index < this.options.tabs_data.size()-1) {
				if (isActive) {
					// If tab is active, add active spacer
					tr.insert(new Element('td',{'class':'tabinterrai'}));
				} else {
					// Determine whether this tab comes before or after active tab
					if (index < active_tab) {
						// Tab before active: determine whether next tab is active or not
						if (active_tab == (index+1)) {
							// Next tab is active so use lia
							tr.insert(new Element('td',{'class':'tabinterlia'}));
						} else {
							// Next tab isn't active so use lii
							tr.insert(new Element('td',{'class':'tabinterlii'}));
						}
					} else {
						// Tab after active so use rii
						tr.insert(new Element('td',{'class':'tabinterrii'}));
					}
				}
			}
		}.bind(this))

		// Terminate tab bar
		if (active_tab == this.options.tabs_data.size() - 1) {
			tr.insert(new Element('td',{'class':'tabtermra'}));
		} else {
			tr.insert(new Element('td',{'class':'tabtermri'}));
		}
		
		$(this.options.tabbar_id).insert(new Element('table').insert(tr));
	}
}



