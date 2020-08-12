//counter for current number of attribute fields
var x = 1;

//add attribute field
$(document).on('click', '.addService', function () {
    //when adding attribute field, increment counter
    x++;
    var html = '<div class="row" id="attrContainer' + x + '" style="margin-top:10px;margin-right:auto;margin-bottom:10px;"><br><div class="col" ><select class="attr-select form-control" name="attr' + x + '-select" id="attr' + x + '-select"><option value="*">ALL RECORDS</option><option value="TOP (100) *">TOP 100 RECORDS</option></option></select></div><div class="col"><select class="form-control" name="attr' + x + '-comparator" id="attr' + x + '-comparator"><option value=""></option><option value=">">></option><option value="<"><</option><option value="=">=</option><option value=">=">>=</option><option value="=<"><=</option><option value="IN">IN</option><option value="LIKE">LIKE</option></select></div><div class="col"><input class="form-control" type="text" name="t' + x + '-val" id="t' + x + '-val" placeholder="Value"></div><br><div class="form-control col" id="radio' + x + '"><label for="and' + x + '">AND</label><input type="radio" id="and' + x + '"name="and-or" value="AND"><label for="or">OR</label><input type="radio" id="or' + x + '" name="and-or" value="OR"><br></div></div>';
    $(this).parent().append(html);
    console.log("added attribute field");
});
//remove attribute field
$(document).on('click', '.removeService', function () {
    //x > 1 signals that there are attribute containers left that can be removed
    if (x > 1) {
        var refID = "#attrContainer" + x.toString();
        $(refID).remove();
        x--;
        console.log("removed attribute field");
    }
    else {
        console.log("cannot remove any more attribute fields");
    }
});

//fetch columns on click
$(document).on('click', '.fetchColumns', function () {
    console.log("Received fetch event");
    //fetch table name
    var selectedTable = $("select#table-select option:checked").val();
    selectedTable = selectedTable.toString();
    console.log("Sending table selection: " + selectedTable.toString());
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
    console.log("Received SQL submit event");
    //fetch sql query from input field
    var query = $("input#sql-query").val();
    console.log("Sending query: " + query.toString());
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
    console.log("Received visual submit event");
    //fetch table name
    var table = $("select#table-select option:checked").val();
    //default behavior if someone were to just click 'submit' straightaway
    if (table == "") {
        table = $("select#table-select option:first").val();
    }
    //get view filters
    var view1 = $("select#view-select option:checked").val();
    //build half of query without qualifiers
    var query = "SELECT " + String(view1) + " FROM [" + String(table) + "]";
    //fetch values of qualifiers
    //maybe contain this in a for loop from 1 to x?
    var compCol = $("select#attr1-select option:checked").val();
    var comparator = $("select#attr1-comparator option:checked").val();
    var compVal = $("input#t1-val").val();
    //to-do: add radio
    if ((comparator != null && comparator != "") || (compCol != null && compCol != "") || (compVal != null && compVal != "")) {
        query = query + " WHERE " + String(compCol) + String(comparator) + String(compVal);
    }
    //check if sorting preference is set
    var sorter = $("select#sort-select option:checked").val();
    if (sorter != null && sorter != "") {
        query = query + " ORDER BY " + String(sorter);
    }
    console.log("Sending query selection: " + query.toString());
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