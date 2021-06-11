var _date;
var _time;
var _duration;
var editMode;
var edit_id;

function hookModifyFunction(index)
{
    $("#modify_s_book").off('click');
    $("#modify_s_book").click( function () {
        console.log("Modify booking " + index);

        modifyCriteria(index);
        $("#book_mgmt_modal").modal('toggle');
        showModifyTable(index);
        toggleEditMode();

        //Fill the hidden form first
        $("#id_c_room_id").val(bookings[index]["id"]);

        //Call the first step
        $.ajax({
            type: 'post',
            url: 'modify_first',
            data: $('#cancel_book_form').serialize(),
            
            success: function(result) {
                console.log(result);
                getUpcoming(); //Refresh the upcoming list to remove the target
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

        $("#search_form").submit(); //Auto refresh room list
    });
}

function modifyCriteria(index)
{
    //Save old criteria first
    _date = $("#id_date").val();
    _time = $("#id_start_time").val();
    _dur = $("#id_duration").val();
    
    //Replace criteria with modify target
    var replace_date = new Date(bookings[index]['start']).toJSON().slice(0,10).split('-').reverse().join('/');
    $("#id_date").val(replace_date);
    $("#id_start_time").val(new Date(bookings[index]['start']).toLocaleTimeString('en-GB'));
    $("#id_duration").val(1);
    $("#id_room_name").val(bookings[index]["r_name"]);
}

function restoreCriteria()
{
    $("#id_date").val(_date);
    $("#id_start_time").val(_time);
    $("#id_duration").val(_dur);
    $("#id_room_name").val("");
    $("#search_form").submit(); //Auto refresh room list
}

function showModifyTable(index)
{
        var row = $("tr", $("#upcoming_table tbody")).eq(index).clone();
        row.addClass('row-highlight');
        $("#modify_table tbody").html("");
        row.appendTo($("#modify_table tbody"));
}

function toggleEditMode()
{
    if(!editMode)
    {
        $("#book_header").text("Modify your booking: ");
        $("#book_modal_header").text("Modify Booking");
        $("#book_modal_p").text("Please review your change:");
        $("#modify_actions").show();
    }
    else
    {
        restoreCriteria();
        $("#modify_table tbody").html("");
        $("#modify_actions").hide();
        $("#book_header").text("Book a room:");
        $("#book_modal_header").text("Confirm Room Booking");
        $("#book_modal_p").text("Please review your booking information:");
    }
    editMode = !editMode;
}

function cancelModify()
{
    $.ajax({
        type: 'post',
        url: 'modify_cancel',
        
        success: function(result) {
            console.log(result);
            getUpcoming(); //Refresh the upcoming list to restore the target
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
    toggleEditMode();
}

function modifyNewBookHandle()
{
    toggleEditMode();
}