var x = 1;

//add attribute field
$(document).on('click', '.addService', function () {
    x++;
    var html = '<div class="row" id="attrContainer' + x + '" style="margin-top:10px;margin-right:auto;margin-bottom:10px;"><br><div class="col" ><select class="attr-select form-control" name="attr' + x + '-select" id="attr' + x + '-select"><option value="*">ALL RECORDS</option><option value="TOP (100) *">TOP 100 RECORDS</option></option></select></div><div class="col"><select class="form-control" name="attr' + x + '-comparator"><option value="none"></option><option value="gt-t' + x + '">></option><option value="lt-t' + x + '"><</option><option value="eq-t' + x + '">=</option><option value="geq-t' + x + '">>=</option><option value="leq-t' + x + '"><=</option><option value="in-t' + x + '">IN</option><option value="like-t' + x + '">LIKE</option></select></div><div class="col"><input class="form-control" type="text" name="t' + x + '-val" placeholder="Value"></div><br><div class="form-control col" id="radio' + x + '"><label for="and' + x + '">AND</label><input type="radio" id="and' + x + '"name="and-or" value="AND"><label for="or">OR</label><input type="radio" id="or' + x + '" name="and-or" value="OR"><br></div></div>';
    $(this).parent().append(html);
    console.log("added attribute field");
});
//remove attribute field
$(document).on('click', '.removeService', function () {
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
$(document).on('click', '.fetchColumns', function() {
    console.log("Received fetch event");
    var selectedTable = $("select#table-select option:checked").val();
    selectedTable = selectedTable.toString();
    console.log("Sending table selection: " + selectedTable.toString());
    $(function () {
        $.post('/query/cols', { 'table': selectedTable },
            function (data) {
                html = JSON.stringify(data);
                additionalHTML = "<option value=''></option>" + html;
                attr1HTML = "<option value='*'>ALL RECORDS</option><option value='TOP (100) *'>TOP 100 RECORDS</option>" + html;
                $(".attr-select").html(additionalHTML);
                $("#attr1-select").html(attr1HTML);
            });
    });
});

//submit query thru sql
$(document).on('click', '.submitQuerySQL', function () {
    console.log("Received SQL submit event");
    var query = $("input#sql-query").val();
    console.log("Sending query: " + query.toString());
    $(function () {
        $.post('/query/result', { 'query': query },
            function (data) {
                html = JSON.stringify(data);
                $("#outputTbl").html(html);
            });
    });
});

//submit query thru visual tool
$(document).on('click', '.submitQueryVisual', function () {
    console.log("Received visual submit event");
    var table = $("select#table-select option:checked").val();
    if(table == ""){
        table = $("select#table-select option:first").val();
    }
    var attr1 = $("select#attr1-select option:checked").val();
    var query = "SELECT " + attr1.toString() + " FROM [" + table.toString() + "]";
    var sorter = $("select#sort-select option:checked").val();
    if (sorter != null && sorter != "") {
        query = query + " ORDER BY " + String(sorter);
    }
    console.log("Sending query selection: " + query.toString());
    $(function () {
        $.post('/query/result', { 'query': query },
            function (data) {
                html = JSON.stringify(data);
                $("#outputTbl").html(html);
            });
    });
});