var baseUrl = "http://localhost:8000"; // In production this should be http://toxicsense.com

$(document).ready(function() {
    $("h2.ProfileHeaderCard-screenname").each(function(index) {
        injectToxicSenseHtml($(this));
    });
    $("span.DashboardProfileCard-screenname").each(function(index) {
        injectToxicSenseHtml($(this));
    });
});

var userScoreMap = {};

function injectToxicSenseHtml(jQueryElement) {
    if (jQueryElement.find("span.toxicsense").length) {
        // Aleady injected.
        return;
    }
    var score = "";
    var usernameLink = jQueryElement.find("a").attr("href");
    if (usernameLink) {
        var username = usernameLink.split("/").pop();
        if (userScoreMap[username]) {
            // User was already analyzed.
            score = userScoreMap[username];
        } else {
            $.get(baseUrl + '/analyzeuser', {user:username}).done(function(response) { handleUserData(username, response); });
        }
        var url = baseUrl + "?user=" + username;
        var iconLink = chrome.extension.getURL("img/icon.png");
        var htmlToInject = `
<span class='toxicsense'>
    <a target='_blank' href='${url}' title='ToxicSense Score. Click here to learn more.'>
        <span>
            <img src='${iconLink}'  title='Analyze this user with ToxicSense' />
            <span id='toxicSense-score-${username}' class='score'></span>
        </span>
    </a>
</span>`;
        jQueryElement.append(htmlToInject);

        if (score) {
            setScore(username, score);
        }
    }
}

function handleUserData(username, data) {
    var dataset = data.map(function(obj){
        var rObj = {
          'date': obj.timestamp,
          'tweet': obj.text,
          'user': obj.user,
          'toxicity': obj.toxicity
        }
        return rObj;
      });

    // Calculate the ToxicSense Score as the numerical percentage
    // between 0 and 100, as...
    // number of toxic tweets / all tweets * 100
    var totalTweets = dataset.length;
    var toxicThreshold = 0.6;
    var toxicTweets = dataset.filter(x => x.toxicity > toxicThreshold).length;
    var score = Math.round(100 * (totalTweets - toxicTweets) / totalTweets);
    setScore(username, score);

    // Cache for future use.
    userScoreMap[username] = score;
}

function setScore(username, score) {
    $("#toxicSense-score-" + username).html(score);
    if (score < 70) {
        $("#toxicSense-score-" + username).addClass("toxic");
    }
}