.. rst-class:: covid19hd text-center

COVID-19 statistics in Heidelberg and Rhein-Neckar-Kreis
========================================================

.. container:: lead

    Last updated on: |last-updated|

    Data source: https://www.rhein-neckar-kreis.de/start/landratsamt/coronavirus+fallzahlen.html

|

Heidelberg
----------

.. container:: lead

    (7-day incidence: |seven-day-incidence-hd|)

|

Daily new
^^^^^^^^^

.. container:: plot-hd-dailynew

    Loading...

|

Cumulative
^^^^^^^^^^

.. container:: plot-hd-cumul

    Loading...

|

Rhein-Neckar-Kreis
------------------

.. container:: lead

    (7-day incidence: |seven-day-incidence-rnk|)

|

Daily new
^^^^^^^^^

.. container:: plot-rnk-dailynew

    Loading...

|

Cumulative
^^^^^^^^^^

.. container:: plot-rnk-cumul

    Loading...


.. |last-updated| raw:: html

   <span id="last-updated">Loading...</span>

.. |seven-day-incidence-hd| raw:: html

   <span id="seven-day-incidence-hd">Loading...</span>

.. |seven-day-incidence-rnk| raw:: html

   <span id="seven-day-incidence-rnk">Loading...</span>

.. raw:: html

    <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
    <script>
    function plot_stats(divid, rawdata) {
        var date = rawdata.columns;
        var data_cumul = [];
        var data_dailynew = [];
        var config = {
            responsive: true
        };
        var colors = ['red', 'green', 'black', 'orange', null, 'orange', 'red'];
        for (var i = 0; i < rawdata.index.length; i++) {
            if (i == 4) {
                $("#seven-day-incidence-" + divid).html(rawdata.data[i][rawdata.data[i].length - 1]);
                continue;
            }
            var column = {
                x: date,
                y: [],
                name: rawdata.index[i],
                line: {
                    color: colors[i]
                }
            };
            for (var j = 0; j < rawdata.data[i].length; j++) {
                column.y.push(rawdata.data[i][j]);
            }
            if (i < 4) {
                data_cumul.push(column);
            } else {
                data_dailynew.push(column);
            }
        }
        var layout = {
            height: 800
        };
        $('.plot-' + divid + '-dailynew').html("");
        $('.plot-' + divid + '-cumul').html("");
        Plotly.newPlot($('.plot-' + divid + '-dailynew')[0], data_dailynew, layout, config);
        Plotly.newPlot($('.plot-' + divid + '-cumul')[0], data_cumul, layout, config);
    }
    $.getJSON("_static/hd_stats.json", function(rawdata) {
        plot_stats('hd', rawdata);
        $("#last-updated").html(rawdata.columns[rawdata.columns.length - 1]);
    });
    $.getJSON("_static/rnk_stats.json", function(rawdata) {
        plot_stats('rnk', rawdata);
    });
    </script>