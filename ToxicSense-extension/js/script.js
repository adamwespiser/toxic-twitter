const BASE_URL = "http://www.toxicsense.com"; // In production this should be http://toxicsense.com
const TIMEOUT = 2000;

var topicScoreMap = {};
var chosenTopic = null;
var chosenUser = null;


$(document).ready(function () {
    startPolling();
});

function refresh() {
    refreshEverything();
    setTimeout(refresh, TIMEOUT);
}

var refreshEverything = function() {
    $("h2.ProfileHeaderCard-screenname").each(function (index) {
        injectToxicSenseHtmlUser($(this));
    });
    $("span.DashboardProfileCard-screenname").each(function (index) {
        injectToxicSenseHtmlUser($(this));
    });
    $("h1.SearchNavigation-titleText").each(function (index) {
        injectToxicSenseHtmlTopic($(this));
    });
};

var startPolling = function() {
    setTimeout(refresh, TIMEOUT);   
};

function injectToxicSenseHtmlTopic(jQueryElement) {
    if (jQueryElement.find("span.toxicsense").length) {
        // Aleady injected.
        return;
    }
    var score = "";
    var topic = jQueryElement.clone().children().remove().end().text().trim();
    if (chosenTopic == topic) {
        return;
    }
    chosenTopic = topic;
    if (topic) {
        if (topicScoreMap[topic]) {
            // User was already analyzed.
            score = topicScoreMap[topic];
        } else {
            $.get(BASE_URL + '/analyze', {topic:topic}).done(function(response) {
                score = handleUserData(response);
                setTopicScore(topic, score);
            });
        }
        var url = BASE_URL + "?topic=" + encodeURIComponent(topic);
        var iconLink = chrome.extension.getURL("img/icon.png");
        var htmlToInject = `
<span class='toxicsense toxicsense-topic'>
    <a target='_blank' href='${url}' title='ToxicSense Score. Click here to learn more.'>
        <span>
            <img src='${iconLink}' title='Analyze this topic with ToxicSense' />
            <span id='toxicSense-score-topic' class='score'></span>
        </span>
    </a>
</span>`;
        jQueryElement.append(htmlToInject);

        if (score) {
            setTopicScore(username, score);
        }
    }
}

function setTopicScore(topic, score) {
    // Cache for future use.
    topicScoreMap[topic] = score;
    var newScore = 100 - score;
    $("#toxicSense-score-topic").html(newScore + "%");
    if (newScore >= 10) {
        $("#toxicSense-score-topic").addClass("toxic");
    }
}

var userScoreMap = {};

function injectToxicSenseHtmlUser(jQueryElement) {
    if (jQueryElement.find("span.toxicsense").length) {
        // Aleady injected.
        return;
    }
    var score = "";
    var usernameLink = jQueryElement.find("a").attr("href");
    if (usernameLink) {
        var username = usernameLink.split("/").pop();
        if (chosenUser == username) {
            return;
        }
        chosenUser = username;
        if (userScoreMap[username]) {
            // User was already analyzed.
            score = userScoreMap[username];
        } else {
            $.get(BASE_URL + '/analyzeuser', {user:username}).done(function(response) {
                score = handleUserData(response);
                setUserScore(username, score);
            });
        }
        var url = BASE_URL + "?user=" + encodeURIComponent(username);
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
            setUserScore(username, score);
        }
    }
}

function handleUserData(data) {
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
    var score = 100 - Math.round(100 * (totalTweets - toxicTweets) / totalTweets);

    return score;
}

function setUserScore(username, score) {
    // Cache for future use.
    userScoreMap[username] = score;

    $("#toxicSense-score-" + username).html(score + "%");
    if (score >= 10) {
        $("#toxicSense-score-" + username).addClass("toxic");
    }
}