var drawGraph = function (links, domElementToAppend) {
    if (links.length <= 2) {
        console.log("Not enough links");
        return;
    }
    var nodes = {};
    links.forEach(function (link) {
        var sourceType, targetType;
        if (link.lt == "mention") {
            sourceType = "user";
            targetType = "mention-user";
        } else if (link.lt == "create") {
            sourceType = "user";
            targetType = "hashtag";
        } else {
            sourceType = "mention-user";
            targetType = "hashtag";
        }
        link.source = nodes[link.source] ||
            (
                nodes[link.source] = {
                    name: link.source,
                    lt: sourceType
                }
            );
        link.target = nodes[link.target] ||
            (
                nodes[link.target] = {
                    name: link.target,
                    lt: targetType
                }
            );
    });
    var chart = d3.select(domElementToAppend);
    var targetWidth = chart.node().getBoundingClientRect().width;
    var width = targetWidth,
        height = 700;

    var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([width, height])
        .gravity(0.07)
        .linkDistance(150)
        .friction(0.5)
        .charge(-250)
        .on("tick", tick)
        .start();
    var svg = d3.select(domElementToAppend).append("svg")
        .attr("width", width)
        .attr("height", height);
    
    svg.append("rect")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("fill", "#efefef");

    svg.append("svg:defs").selectAll("marker")
        .data(["end"])
        .enter().append("svg:marker")
        .attr("id", String)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", -1.5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("svg:path")
        .attr("d", "M0,-5L10,0L0,5");

    var path = svg.append("svg:g").selectAll("path")
        .data(force.links())
        .enter().append("svg:path")
        .attr("class", function (d) { return "link " + d.type; })
        .style("stroke", function (d) {
            return d.lt == "create" ? "blue" : d.lt == "mention" ? "red" : "green";
        });

    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter().append("g")
        .attr("class", "node")
        .call(force.drag);

    node.append("circle")
        .attr("r", function (d) { return 3 + (d.weight * 0.5); })
        .attr("class", function (d) { return "dag-circle node-" + d.lt; });

    node.on("dblclick", function (d) {
        d.fixed = !d.fixed;
        var fixedClassName = "node-" + d.lt + "-fixed";
        var movableClassName = "node-" + d.lt;
        if (d.fixed) {
            d3.select(this).select("circle")
                .attr("class", fixedClassName);
        } else {
            d3.select(this).select("circle")
                .attr("class", movableClassName);
        }
    });

    node.append("text")
        .attr("dx", "1em")
        .attr("dy", "0.3em")
        .style("font-size", function (d) {
            return d.weight > 10 ? "13px" : "10px";
        })
        .style("font-weight", function (d) {
            return d.weight > 10 ? "bold" : "";
        })
        .attr("class", "dag-text")
        .text(function (d) {
            if (d.weight > 1) {
                return d.name;
            } else {
                return "";
            }
        });

    function tick() {
        path.attr("d", function (d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" +
                d.source.x + "," +
                d.source.y + "A" +
                dr + "," + dr + " 0 0,1 " +
                d.target.x + "," +
                d.target.y;
        });
        node.attr(
            "transform",
            function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            }
        );
    };

    var tipNode = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            return "<div><span style='color:white'>" + d.name + "</span></div>";
        });

    var tipPath = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            return "<div><span style='color:white'>" + d.tweet + "</span></div>";
        });

    svg.call(tipPath);
    svg.call(tipNode);

    d3.selectAll(domElementToAppend + " circle")
        .on('mouseover', tipNode.show).on('mouseout', tipNode.hide);

    d3.selectAll(domElementToAppend + " path")
        .on('mouseover', tipPath.show).on('mouseout', tipPath.hide);
}
