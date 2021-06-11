function u_addToTable(table, data)
{
    //Black magic to display in proper format
    var start_date = new Date(data['start']).toJSON().slice(0,10).split('-').reverse().join('/') + ' ' + new Date(data['start']).toLocaleTimeString();
    var end_date = new Date(data['end']).toJSON().slice(0,10).split('-').reverse().join('/') + ' ' + new Date(data['end']).toLocaleTimeString();
    table.append('<tr> <td style = "height: 100px; text-align: left;">' 
    + '<div style = "float: left;">'
    + '<b>🚪'+data["r_name"] + '</b><br> ' + "🏢 "+ data["r_location"] + '<br>'
    + '</div>' 
    + '<div style = "float: right;">'
    + 'Start: <b>' + start_date + '</b><br>'
    + 'End: <b>' + end_date + '</b><br>'
    + '</div>'
    + '</td></tr>'
    );
}

function u_rowHTML(data)
{
    var html;
    if(data["available"])
        var status_html = '✅ <span style = "color:green">Available</span>'
    else
        var status_html = '❌ <span style = "color:red">Unavailable</span>'
    html =  '<b>'+data["name"] + '</b>' + '<br>'
            + "🏢 "+ data["location"] + '<br>'
            + "Capacity: " + data["capacity"] + '<br>' 
            + status_html + '<br>'
            + '$ ' + data["price"] + ' / hour' + '<br>'
    return html;
}

function u_makeClickable()
{
    //Just hardcode the element id...
    $("#upcoming_table tbody tr").click(function(){
        if(editMode)
            return;
        var row_index = $(this).index();
        u_fillModal(row_index);
        $("#book_mgmt_modal").modal();
    });
}

function u_fillModal(index) //Populate information in the modal
{
    edit_id = index;

    var start_date = new Date(bookings[index]['start']).toJSON().slice(0,10).split('-').reverse().join('/') + ' ' + new Date(bookings[index]['start']).toLocaleTimeString();
    var end_date = new Date(bookings[index]['end']).toJSON().slice(0,10).split('-').reverse().join('/') + ' ' + new Date(bookings[index]['end']).toLocaleTimeString();

    hookMgmtFunction(index);
    hookModifyFunction(index);

    $("#book_mgmt_modal_desc").html("");
    $("#book_mgmt_modal_desc").append("Room: <b>" + bookings[index]["r_name"] + "<br>");
    $("#book_mgmt_modal_desc").append("Location: <b>" + bookings[index]["r_location"] + "</b></p>");
    $("#book_mgmt_modal_desc").append("<p>From: <b>" + start_date + "</b>");
    
    $("#book_mgmt_modal_desc").append("<p>To: <b>" + end_date + " " + "</b></p>");
    
}

function hookMgmtFunction(id)
{
    $("#cancel_s_book").off('click');
    $("#cancel_s_book").click( function () {
        console.log("Cancel booking " + id);

        //Fill the hidden form first
        $("#id_c_room_id").val(bookings[id]["id"]);

        $.ajax({
            type: 'post',
            url: 'cancel_book',
            data: $('#cancel_book_form').serialize(),
            
            success: function(result) {
                console.log(result);
                handleCancelBookSuccess();
            },
    
            fail: function ()
            {
              alert ("There was an error connecting to the server! Please retry")
            },
            error: function(result)
            {
              alert (result.responseJSON.msg);
            }
          });
    });
}

function handleCancelBookSuccess()
{
    //Close current modal and open success modal
    $("#book_mgmt_modal").modal('toggle');
    $("#cancel_book_success_modal").modal();

    //Refresh lists
    getUpcoming(); //Auto get upcoming  bookings
    $("#search_form").submit(); //Auto refresh room list
}
