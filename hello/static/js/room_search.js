function addToTable(table, data)
{
    if(data["img"] != "")
        var img_url = "/media/" + data["img"];
    else
        var img_url = "/media/rooms/default.jpg";
    var img_html = '<img src = ' + img_url + ' style = "max-height: 200px; float: left; margin-right: 100px">';
    table.append('<tr> <td style = "height: 217px; ">' 
    + img_html 
    + '<div style = "float: right;">'
    + rowHTML(data)
    + '</td></tr>'
    );
}

function rowHTML(data)
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

function makeClickable()
{
    //Just hardcode the element id...
    $("#results_table tbody tr").click(function(){
        var row_index = $(this).index();
        handleBookRoom(row_index);
    });
}

function handleBookRoom(index) //Populate information in the modal
{
    if(!rooms[index]["available"])
    {
        alert("This room is occupied");
        return;
    }
    var date =  $("#id_date").val();
    var start_time = $("#id_start_time").val();
    var duration = parseInt($("#id_duration").val());
    var end_time = calcEndTime(start_time, duration);
    var price = rooms[index]["price"] * duration;
    hookBookFunction(rooms[index]["id"],date,start_time,duration,price);

    $("#bookmodal_desc").html("");
    $("#bookmodal_desc").append("Room: <b>" + rooms[index]["name"] + "<br>");
    $("#bookmodal_desc").append("Location: <b>" + rooms[index]["location"] + "</b><br>");
    $("#bookmodal_desc").append("Capacity: <b>" + rooms[index]["capacity"] + " person(s)</b></p>");
    $("#bookmodal_desc").append("<p>From: <b>" + date + " " + start_time + "</b>");
    
    $("#bookmodal_desc").append("<p>To: <b>" + date + " " 
                + end_time + "</b></p>");
    $("#bookmodal_price_total").text(price);

    $("#book_modal").modal();

    calcPromoPrice();
}

function hookBookFunction(id, date, start_time, duration, price)
{
    $("#accept_book").off('click');
    $("#accept_book").click( function () {
        if(bookings.length >= 3 && !editMode)
        {
            alert("You can only have a maximum of 3 bookings");
            return;
        }
        console.log("Book data: " + id + ' ' + date + ' ' + start_time + ' ' +  duration + ' ' + price);

        //Fill the hidden form first
        $("#id_b_room_id").val(id);
        $("#id_b_date").val(date);
        $("#id_b_start_time").val(start_time);
        $("#id_b_duration").val(duration);
        $("#id_b_price").val(price);

        $.ajax({
            type: 'post',
            url: 'book_room',
            data: $('#book_form').serialize(),
            
            success: function(result) {
                console.log(result);
                handleBookSuccess();
                if(editMode)
                    modifyNewBookHandle();
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

function handleBookSuccess()
{
    //Close current modal and open success modal
    $("#book_modal").modal('toggle');
    $("#book_success_modal").modal();

    //Refresh lists
    getUpcoming(); //Auto get upcoming  bookings
    $("#search_form").submit(); //Auto refresh room list
}

function calcEndTime(start, duration)
{
    var new_hour = parseInt(start.substring(0,2)) + duration;
    var new_string = new_hour + ":" + start.slice(3,5);
    return new_string;
}

function handleCheckbox()
{
    $("#search_filter_available").change( function () {
        toggleFilterVisiblity();
    });
}

function toggleFilterVisiblity()
{
    if (!$("#search_filter_available").is(':checked')){
        $("#results_table tbody tr").each( function(index, row) {
            $(row).show();
        });
    }
    else{
        $("#results_table tbody tr").each( function(index, row) {
            if(!rooms[index]["available"])
                $(row).hide();
        });
    }
}