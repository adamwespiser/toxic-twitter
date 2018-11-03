function visualizeUserTweets(data) {
    // TODO: Replace content below with d3 implementation.

    var jsonResponse = JSON.stringify(data, undefined, 2);
    jsonResponse = jsonResponse.replace(/(?:\r\n|\r|\n)/g, '<br>');
    $('#jsonResult').html(jsonResponse);
}

function visualizeTopicTweets(data) {
    var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S").parse;

    var dataset = data.map(function(obj){
        var rObj = {
          'date': parseDate(obj.timestamp),
          'tweet': obj.text,
          'user': obj.user,
          'toxicity': obj.toxicity
        }
        return rObj;
      });

    svgHeight = 327
    svgWidth = 900
    var margin = {top: 60, right: 100, bottom: 40, left: 100},

    width = svgWidth - margin.left - margin.right,
    height = svgHeight - margin.top - margin.bottom;

    // Set the ranges
    var x = d3.time.scale()
      .domain(d3.extent(dataset,
            function(d) { return d.date; }))
      .range([0, width]);
    var y = d3.scale.linear()
      .domain([0,1])
      .range([height, 0]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
      .orient("bottom").ticks(5);

    var yAxis = d3.svg.axis().scale(y)
      .orient("left").ticks(5);

    // NOTE: this is a pretty ugly external linkage...
    // but we need to clear the text before we make the plot
    $("#jsonResult").empty()


    // Create the svg element to put our plot on
    var svg = d3.select("#jsonResult")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    var tooltip = d3.select("#jsonResult").append("div")
                  .attr("class", "tooltip")
                  .style("opacity", 0);

    // Not sure this is 100% working:
    // The "text" here is going to the bottom of the page,
    // which works fine for now, but we may want to change this
    // to a new "target"
    var tipMouseover = function(d) {
        var html  = "@" + d.user + "<br/>" + d.date + "<br/>" + d.tweet ;
        tooltip.html(html)
            .style("left", (d3.event.pageX)) // move this to target
            .style("top", (d3.event.pageY))  // move this to target
            .transition()
            .duration(200)
            .style("opacity", .9) // started as 0!

        };
    // tooltip mouseout event handler
    var tipMouseout = function(d) {
         tooltip.transition()
         .duration(300)
         .style("opacity", 0);
    };

    // Add the scatterplot
    svg.selectAll("dot")
        .data(dataset)
      .enter().append("circle")
        .attr("r", 3.5)
        .attr("cx", function(d) { return x((d.date)); })
        .attr("cy", function(d) { return y(d.toxicity); })
        .on("mouseover", tipMouseover)
        .on("mouseout", tipMouseout);

    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    // Make the Y Axis Labels
    svg.append("text")
      .attr("x",-50)
      .attr("y",-10)
      .text("Toxic");

    svg.append("text")
      .attr("x",-50)
      .attr("y",height + 35)
      .text("Benign");

    // Make the X Axis Label
    svg.append("text")
      .attr("x",width - 30)
      .attr("y",height + 35)
      .text("Year");

    // Make the plot title
    title = "Tweet Toxicity vs. Time";
    svg.append("text")
      .attr("x", (width/2))
      .attr("y", -20)
      .style("text-anchor", "middle")
      .style("font-weight", "bold")
      .style("font-size", "16px")
      .text(title);

}
