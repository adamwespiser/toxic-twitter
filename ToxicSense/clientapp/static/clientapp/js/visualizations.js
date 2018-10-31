function visualizeUserTweets(data) {
    // TODO: Replace content below with d3 implementation.

    var jsonResponse = JSON.stringify(data, undefined, 2);
    jsonResponse = jsonResponse.replace(/(?:\r\n|\r|\n)/g, '<br>');
    $('#jsonResult').html(jsonResponse);
}

function visualizeTopicTweets(data) {
    // TODO: Replace content below with d3 implementation.

    var jsonResponse = JSON.stringify(data, undefined, 2);
    jsonResponse = jsonResponse.replace(/(?:\r\n|\r|\n)/g, '<br>');
    $('#jsonResult').html(jsonResponse);
}