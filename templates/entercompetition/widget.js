document.getElementById('bmc_wrapper').innerHTML = '<div id="bmc_widget">{{form|safe}}</div>';

function jsonp(url, callback, name, query)
{                
    if (url.indexOf("?") > -1)
        url += "&jsonp=";
    else
        url += "?jsonp=";
    url += name + "&";
    if (query)
        //url += encodeURIComponent(query) + "&";   
        url += query + "&";
    url += new Date().getTime().toString(); // prevent caching        
    
    var script = document.createElement("script");        
    script.setAttribute("src",url);
    script.setAttribute("type","text/javascript");                
    document.body.appendChild(script);
}

function apply(competition_url) {
    var query = "";
    var form = document.getElementById("bmc_form");
    for (var i=0; i < form.length; i ++) {
        if (i > 0) 
	    query += "&";
        query += "" + form.elements[i].name + "=" + form.elements[i].value;
    }
    
    jsonp("/apply/" + competition_url, "{{callback_function}}", "enter_competition", query);
    
    return false; //cancel form submission
}

function {{callback_function}}(data) {
    var widget = document.getElementById("bmc_widget");
    widget.innerHTML = data.message;
}