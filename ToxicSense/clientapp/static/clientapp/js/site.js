$(document).ready(function() {
    $('#loading').hide();
});

$('#topicsearch').click(analyze);
$('#topic').on('keypress', function(e) {
    if (e.keyCode == 13) {
        analyze();
    }
});

function analyze() {
    var topic = $('#topic').val();
    if (!topic.trim() || topic.length < 2) {
        return;
    }

    $('#topicsearch').attr("disabled", "disabled");
    $('#loading').show();
    $.get('/analyze', {topic:topic})
     .done(function(response) {
        $('#topicsearch').removeAttr("disabled");
        $('#loading').hide();
        var jsonResponse = JSON.stringify(response, undefined, 2);
        jsonResponse = jsonResponse.replace(/(?:\r\n|\r|\n)/g, '<br>');
        $('#jsonResult').html(jsonResponse);
     });
}