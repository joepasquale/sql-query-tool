var x = 1;
//add attribute field
$(document).on('click', '.addService', function () {
    x++;
    var html = '<div class="row" id="attrContainer' + x + '" style="margin-top:10px;margin-right:auto;margin-bottom:10px;"><br><div class="col" ><select class="form-control" name="attr' + x + '-select"><option value="attr1-t' + x + '">Attribute 1</option><option value="attr2-t' + x + '">Attribute 2</option><option value="attr3-t' + x + '">Attribute 3</option><option value="attr4-t' + x + '">Attribute 4</option><option value="attr5-t' + x + '">Attribute 5</option></select></div><div class="col"><select class="form-control" name="attr' + x + '-comparator"><option value="none"></option><option value="gt-t' + x + '">></option><option value="lt-t' + x + '"><</option><option value="eq-t' + x + '">=</option><option value="geq-t' + x + '">>=</option><option value="leq-t' + x + '"><=</option><option value="in-t' + x + '">IN</option><option value="like-t' + x + '">LIKE</option></select></div><div class="col"><input class="form-control" type="text" name="t' + x + '-val" placeholder="Value"></div><br><div class="form-control col" id="radio' + x + '"><label for="and' + x + '">AND</label><input type="radio" id="and' + x + '"name="and-or" value="AND"><label for="or">OR</label><input type="radio" id="or' + x + '" name="and-or" value="OR"><br></div></div>';
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
//fetch columns
$(document).on('click', '.fetchColumns', function () {
    console.log("on");
    var selectedTable = $("select#table-select option:checked").val();
    selectedTable = selectedTable.toString();
    console.log(selectedTable == null);
    $.post('/query/fetch-columns', {'table':selectedTable});
});

//temp
$(document).on('click', '.submitQuery', function () {
    console.log("sent query");
});