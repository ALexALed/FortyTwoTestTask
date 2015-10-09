$(document).ready(function () {

    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // page requests
    if ($("#requestsContainer").length) {

        function sendViews(requests) {
            $.ajax({
                method: "post",
                url: "/requests/requestsData/",
                data: {'data':JSON.stringify(requests)}
            });
        }

        function fillData(data) {
            var compiledRow = _.template("<tr class=<%=bold_class%>><td><%=http_request%></td>" +
                "<td><%=remote_addr%></td>" +
                "<td><%=date_time%></td> " +
                "</tr>");
            var rows = '';
            data['requestsData'].forEach(function (item) {
                var row = compiledRow({
                    http_request: item['http_request'],
                    remote_addr: item['remote_addr'],
                    date_time: item['date_time'],
                    bold_class: item['viewed'] == false ? 'bold-font' : ''
                });
                rows += row;
            });

            $('#requestsContainer').html(rows);
            $('#requestsHeader').text('(' + data['requestsNew'] + ') Requests');
        }


        function fillRequests() {

            $.ajax({
                method: "get",
                url: "/requests/requestsData"
            }).done(function (data) {
                fillData(data);
                sendViews(data['requestsData']);
            });
        }

        fillRequests();
        setInterval(fillRequests, 10000); //10 sec delay

    }
});