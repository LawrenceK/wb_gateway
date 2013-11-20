// $Id: Event.js 2360 2008-06-06 16:00:16Z webbrick $
//
// Define an object type for basic events, and associated functions.
//

// Construct a basic event.
function Event(evtype, source, payload) {
    // Initialize a new event object
    // Use blank string consistently for undefined fields
    this._evtype  = evtype  || "";
    this._source  = source  || "";
    if (payload === undefined) {
        this._payload = null ;
    } else {
        this._payload = payload ;
    }
}

new Event() ;   // Force prototype into existence

Event.prototype.eq = function(other) {
    return ( (this._evtype  == other._evtype)  &&
             (this._source  == other._source)  &&
             (this._payload == other._payload) );
}

Event.prototype.toString = function() {
    return "Event(evtype=\""+this._evtype+"\", source=\""+this._source+"\")";
}

Event.prototype.getType = function() {
    return this._evtype;
}

Event.prototype.getSource = function() {
    return this._source;
}

Event.prototype.getPayload = function() {
    return this._payload;
}

function makeEvent(evtype,source,payload) {
    // Construct a new event object from the supplied values
    if (!evtype) evtype = EventUri.DefaultType;
    return new Event(evtype,source,payload);
}

// End.
