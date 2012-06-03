$(document).ready(function() {
	pieChart();
	$('#button').click(pieChart);
	$('#beets').on('change', 'input', pieChart);
    });

var clr = [];
var j = 0;

function pieChart(i) {
	$("#holder").empty();
	var r = Raphael("holder");
    r.customAttributes.segment = function (x, y, r, a1, a2) {
		j += 1
		if (a1 == 0) {
			j = 0;
		}

        var color = $('#input'+(j+1) ).attr('color');

        var flag = (a2 - a1) > 180,
        a1 = (a1 % 360) * Math.PI / 180;
        a2 = (a2 % 360) * Math.PI / 180;

        return {
            path: [["M", x, y], ["l", r * Math.cos(a1), r * Math.sin(a1)], ["A", r, r, 0, + flag, 1, x + r * Math.cos(a2), y + r * Math.sin(a2)], ["z"]],
            fill: "hsb(" + color + ", .75, .8)"
        };
    };

    function animate(ms) {
        var start = 0,
            val;
        for (i = 0; i < ii; i++) {
            val = 360 / total * data[i];
            paths[i].animate({segment: [200, 200, 150, start, start += val]}, 200);
            paths[i].angle = start - val / 2;
        }
    }

    var data = [];
		var inputs = $('#beets').find('.amount').length;
			for (var i = 0; i < inputs; i++) {
                data.push( parseFloat( $('#input'+(i+1) ).val() ))
                $('#input'+(i+1) ).attr('color', 1-((i+1)/10)) ;

			}
    var paths = r.set(),
        total,
        start,
        bg = r.circle(200, 200, 0).attr({stroke: "#fff", "stroke-width": 4});
    data = data.sort(function (a, b) { return b - a;});

    total = 0;
    for (var i = 0, ii = data.length; i < ii; i++) {
        total += data[i];
    }
    start = 0;
    for (i = 0; i < ii; i++) {
        var val = 360 / total * data[i];
        (function (i, val) {
            paths.push(r.path().attr({segment: [200, 200, 1, start, start + val], stroke: "#fff"}).click(function () {
                pieChart();
            }));
        })(i, val);
        start += val;
    }
    bg.animate({r: 151}, 1000, "bounce");
    animate(1000);
	updateColors();
};

/**
 * Find the color blocks and update the colors
 */
function updateColors(){
	var c = $("#beets .colorbox"),
		inputs = $("#beets .amount");

	inputs.each(function(i, ele){
		var hue = 360 * $(ele).attr("color"),
			box = $(c.get(i));
		console.log(hue);

		box.css("background-color", "hsl("+hue+", 75%, 80%)");
	});
}
