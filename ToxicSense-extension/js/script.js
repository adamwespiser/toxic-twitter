$(document).ready(function() {
    $("h2.ProfileHeaderCard-screenname").each(function(index) {
        injectToxicSenseHtml($(this));
    });
    $("span.DashboardProfileCard-screenname").each(function(index) {
        injectToxicSenseHtml($(this));
    });
});



function injectToxicSenseHtml(jQueryElement) {
    if (jQueryElement.find("span.toxicsense").length) {
        // Aleady injected.
        return;
    }
    var usernameLink = jQueryElement.find("a").attr("href");
    if (usernameLink) {
        var username = usernameLink.split("/").pop();
        var url = "http://toxicsense.com?user=" + username;
        var iconLink = chrome.extension.getURL("img/icon.png");
        var htmlToInject = "<span class='toxicsense'><a target='_blank' href='" + url + "'><img src='" + iconLink + "'  title='Analyze this user with ToxicSense' /></a></span>";
        jQueryElement.append(htmlToInject);
    }
}