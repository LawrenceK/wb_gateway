// $Id:$

// Returns True if string ends with the provided character
String.prototype.endsWith = function(c)
    {
    return ( c == this.charAt(this.length-1));
    }