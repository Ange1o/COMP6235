$(document).ready(function () {
    GetAll();
});


    alert("111")
    $.ajax({
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        url: 'user/GetAll',
        success: function (data) {
            var newHtml = "";
            $.each(data, function (index, value) {
                newHtml += "<tr><td>" + value.data+ "</td><td>" + value.trend + "</td></tr>";
            });
            $('#fList').append(newHtml);
        },
        error: function (data) {
            alert('Error in getting result');
        }
    });
