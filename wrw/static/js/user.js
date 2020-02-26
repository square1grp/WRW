$(document).ready(function () {
    $("#menu-btn").click(function () {
        $("#menu").toggle()
    });
    
    $("a#redirect_to_symptom").click(function (e) {
        e.preventDefault();

        symptom_id = $("select.symptom").val();
        window.location.href = "/symptom/" + symptom_id.toString();
    });
});

$(document).ready(function () {
    $("div.plotly-graph-div").on("plotly_hover", function (e, data) {
        if (data.points.length == 0)
            return false;

        var point = data.points[0];
        var pn = point.pointNumber,
            tn = point.curveNumber,
            sizes = point.data.marker.size,
            line_colors = point.data.marker.line.color;

        var color = line_colors[pn];
        color = color.replace("0)", "1)");
        line_colors[pn] = color
        var update = { "marker": { size: sizes, opacity: 1, "line": { color: line_colors, width: 12 } } };
        Plotly.restyle($(this).attr("id"), update, [tn]);
    }).on("plotly_unhover", function (e, data) {
        if (data.points.length == 0)
            return false;

        var point = data.points[0];
        var pn = point.pointNumber,
            tn = point.curveNumber,
            sizes = point.data.marker.size,
            line_colors = point.data.marker.line.color;

        var color = line_colors[pn];
        color = color.replace("1)", "0)");
        line_colors[pn] = color
        var update = { "marker": { size: sizes, opacity: 1, "line": { color: line_colors, width: 12 } } };
        Plotly.restyle($(this).attr("id"), update, [tn]);
    });
});