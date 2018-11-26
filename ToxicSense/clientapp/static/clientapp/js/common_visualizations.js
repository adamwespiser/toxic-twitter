var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S").parse;

function colorTweetByToxicity(toxicity) {
    if (toxicity > 0.6) {
        return "red";
    }
    if (toxicity > 0.2) {
        return "limegreen";
    }
    return "green";
}

function visualizeToxicityVsTime(data, elementId) {
    var dataset = data.map(function (obj) {
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
    var margin = { top: 40, right: 100, bottom: 40, left: 100 },
        width = svgWidth - margin.left - margin.right,
        height = svgHeight - margin.top - margin.bottom;

    // Set the ranges
    var x = d3.time.scale()
        .domain(d3.extent(dataset,
            function (d) { return d.date; }))
        .range([0, width]);
    var y = d3.scale.linear()
        .domain([0, 1])
        .range([height, 0]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(5);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

    // NOTE: this is a pretty ugly external linkage...
    // but we need to clear the text before we make the plot
    $(elementId).empty()

    // Create the svg element to put our plot on
    var svg = d3.select(elementId)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    var tooltip = d3.select(elementId).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // Not sure this is 100% working:
    // The "text" here is going to the bottom of the page,
    // which works fine for now, but we may want to change this
    // to a new "target"
    var tipMouseover = function (d) {
        var html = "@" + d.user + "<br/>" + d.date + "<br/>" + d.tweet;
        tooltip.html(html)
            .style("left", (d3.event.pageX)) // move this to target
            .style("top", (d3.event.pageY))  // move this to target
            .transition()
            .duration(200)
            .style("opacity", .9) // started as 0!

    };
    // tooltip mouseout event handler
    var tipMouseout = function (d) {
        tooltip.transition()
            .duration(300)
            .style("opacity", 0);
    };

    // Add the scatterplot
    svg.selectAll("dot")
        .data(dataset)
        .enter().append("circle")
        .attr("r", 3.5)
        .attr("cx", function (d) { return x((d.date)); })
        .attr("cy", function (d) { return y(d.toxicity); })
        .attr("fill", function (d) {
            return colorTweetByToxicity(d.toxicity);
        })
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
        .attr("x", -50)
        .attr("y", -10)
        .attr("font-family", "sans-serif")
        .style("font-weight", "normal")
        .text("Toxic");

    svg.append("text")
        .attr("x", -50)
        .attr("y", height + 35)
        .attr("font-family", "sans-serif")
        .style("font-weight", "normal")
        .text("Non-Toxic");

    // Make the X Axis Label
    svg.append("text")
        .attr("x", width - 30)
        .attr("y", height + 35)
        .attr("font-family", "sans-serif")
        .style("font-weight", "normal")
        .text("Time");

    // Make the plot title
    title = "Tweet Toxicity vs. Time";
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", -20)
        .style("text-anchor", "middle")
        .style("font-weight", "normal")
        .attr("font-family", "sans-serif")
        .style("font-size", "16px")
        .text(title);


    // Make the legend
    const legendData = [["Toxic Message", "red", "circle"], ["Non-Toxic message", "green", "circle"]];

    var legend = svg.append('g')
        .attr("class", "legend1")
        .attr("height", 0)
        .attr("width", 0)
        .attr('transform', 'translate(' + (width - margin.right) + ',' + -30 + ')')

    // Create the legend object
    var legendRect = legend
        .selectAll('g')
        .data(legendData);

    // Set up the right translate for each point in the legend
    var legendRectE = legendRect.enter()
        .append("g")
        .attr("transform", function (d, i) {
            return 'translate(0, ' + (i * 13) + ')';
        });

    // make the legend "circles"
    legendRectE
        .append('circle')
        .attr('r', 3.5)
        .attr("opacity", 1)
        .style("fill", function (d) { return d[1]; });


    // Set the legend label
    legendRectE
        .append("text")
        .attr("x", 10)
        .attr("y", 5)
        .attr("font-size", "12px")
        .attr("font-weight", "normal")
        .attr("font-family", "sans-serif")
        .text(function (d) {
            return d[0];
        });

    // put a rect around the legend
    // TODO figure out a way to bind this to legendRectE
    svg.append("rect")
        .attr("height", 25)
        .attr("width", 140)
        .attr("x", width - margin.right - 10)
        .attr("y", -35)
        .attr("stroke", "black")
        .attr("fill", "none")
        .attr("stroke-width", 1)
}
