//counter for current number of attribute fields
var x = 1;

//add attribute field
$(document).on('click', '.addService', function () {
    //when adding attribute field, increment counter
    x++;
    //new attribute field contains and/or radio, col selector, comparator, and value fields
    var html = '<div class="row" id="attrContainer' + x + '" style="margin-top:10px;margin-bottom:10px;"><div class="col" id="radio' + (x - 1) + '"><select class="form-control" id="ANDOR' + (x - 1) + '"><option value=""></option><option value="AND">AND</option><option value="OR">OR</option></select></div><div class="col"><select class="attr-select form-control" name="attr' + x + '-select" id="attr' + x + '-select"></select></div><div class="col"><select class="form-control" name="attr' + x + '-comparator" id="attr' + x + '-comparator"><option value=""></option><option value=">">></option><option value="<"><</option><option value="=">=</option><option value=">=">>=</option><option value="=<"><=</option><option value="NOT">NOT</option><option value="LIKE">LIKE</option><option value="SOME">SOME</option></select></div><div class="col"><input class="form-control" type="text" name="t' + x + '-val" id="t' + x + '-val" placeholder="Value"></div>';
    $(this).parent().append(html);
    console.log("User added attribute field");
});
//remove attribute field
$(document).on('click', '.removeService', function () {
    //x > 1 signals that there are attribute containers left that can be removed
    if (x > 1) {
        var refID = "#attrContainer" + x.toString();
        $(refID).remove();
        x--;
        console.log("User removed attribute field");
    }
    else {
        console.log("Not allowed: minimum number of attribute fields reached (1)");
    }
});

//fetch columns on click
$(document).on('click', '.fetchColumns', function () {
    console.log("Browser received column fetch event");
    //fetch table name
    var selectedTable = $("select#table-select option:checked").val();
    selectedTable = selectedTable.toString();
    console.log("Sending table selection to server: " + selectedTable.toString());
    $(function () {
        //post request to /querys/cols for dbAccess to handle
        $.post('/query/cols', { 'table': selectedTable },
            function (data) {
                //unpack response from dbAccess from json to string
                html = JSON.stringify(data);
                //html for attribute containers
                additionalHTML = "<option value=''></option>" + html;
                //html for selecting which attributes to view
                viewHTML = "<option value='*'>ALL RECORDS</option><option value='TOP (100) *'>TOP 100 RECORDS</option>" + html;
                $(".attr-select").html(additionalHTML);
                $("#view-select").html(viewHTML);
            });
    });
});

//submit query thru sql
$(document).on('click', '.submitQuerySQL', function () {
    console.log("Browser received SQL submit event");
    //fetch sql query from input field
    var query = $("input#sql-query").val();
    console.log("Sending query to server: " + query.toString());
    $(function () {
        //post to /query/result to get table string
        $.post('/query/result', { 'query': query },
            function (data) {
                //translate json object containing table string
                html = JSON.stringify(data);
                $("#outputTbl").html(html);
            });
    });
});

//submit query thru visual tool
$(document).on('click', '.submitQueryVisual', function () {
    console.log("Browser received visual submit event");
    //fetch table name
    var table = $("select#table-select option:checked").val();
    //default behavior if someone were to just click 'submit' straightaway
    if (table == "") {
        table = $("select#table-select option:first").val();
    }
    //get view filters (which columns to show)
    var view1 = $("select#view-select option:checked").val();
    //build half of query without qualifiers
    var query = "SELECT " + String(view1) + " FROM [" + String(table) + "]";
    //fetch values of qualifiers
    //execute if there are multiple qualifiers
    if (x > 1) {
        query = query + " WHERE ";
        //for however many fields there are, iterate through fields, fetch values, and add to query string
        for (var i = 0; i <= x; i++) {
            //column field id
            var colString = "select#attr" + (i) + "-select option:checked";
            var compCol = $(colString).val();
            //comparator field id
            var compString = "select#attr" + (i) + "-comparator option:checked";
            var comparator = $(compString).val();
            //value field id
            var valString = "input#t" + (i) + "-val";
            var compVal = $(valString).val();
            //and/or field id; if i == x, then this will be "", you can't append an and/or at the end of the statement
            var radioString = "select#ANDOR" + (i);
            var radioVal = $(radioString).val();
            //checks to make sure that all fields are filled out before adding the string
            if ((comparator != null && comparator != "") || (compCol != null && compCol != "") || (compVal != null && compVal != "")) {
                //if there are more attribute fields, append the AND/OR statement
                if (i != x) {
                    query = query + String(compCol) + " " + String(comparator) + " " + String(compVal) + " " + String(radioVal) + " ";
                } 
                //otherwise (if you're at the last attribute field) don't append AND/OR
                else {
                    query = query + String(compCol) + " " + String(comparator) + " " + String(compVal) + " ";
                }
            }
        }
    }
    //execute if there are no extra fields
    else {
        //same logic as above
        var colString = "select#attr1-select option:checked";
        if ($(colString).val() != "") {
            query = query + " WHERE ";
            var compCol = $(colString).val();
            var comparator = $("select#attr1-comparator option:checked").val();
            var compVal = $("input#t1-val").val();
            if ((comparator != null && comparator != "") || (compCol != null && compCol != "") || (compVal != null && compVal != "")) {
                query = query + String(compCol) + " " + String(comparator) + " " + String(compVal);
            }
        }
    }
    //check if sorting preference is set
    var sorter = $("select#sort-select option:checked").val();
    if (sorter != null && sorter != "") {
        query = query + " ORDER BY " + String(sorter);
    }
    //send query to views -> dbAccess
    console.log("Sending query selection to server: " + query.toString());
    $(function () {
        //placeholder text to show that the server is awaiting a query
        $("#outputTbl").text("Client awaiting query result: " + query.toString() + " ...");
        //post to /query/result to get table string
        $.post('/query/result', { 'query': query },
            function (data) {
                //translate json object containing table string
                html = JSON.stringify(data);
                $("#outputTbl").html(html);
            });
    });
});