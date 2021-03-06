.. rst-class:: covid19hd text-center

COVID-19 statistics in Heidelberg and Rhein-Neckar-Kreis
========================================================

.. container:: lead

    Last updated on: |last-updated|

    Data source: https://lrarnk.maps.arcgis.com/apps/opsdashboard/index.html#/ee14457029f4480ca0f7e16a4bae0929

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
    function AvgQueue(interval) {
        this.queue = [];
        this.interval = 7;
    }
    AvgQueue.prototype.push_and_calc_average = function (val) {
        var avg = 0;
        this.queue.push(val);
        while (this.queue.length > this.interval) {
            this.queue.shift();
        }
        if (this.queue.length == this.interval) {
            for (var i=0; i<this.queue.length; i++) {
                avg += this.queue[i];
            }
            avg /= this.queue.length;
        } else {
            avg = null;
        }
        return avg;
    }
    function plot_stats(json) {
        // af: Quarantined, ni: Daily new, gn: Recovered, vst: Deaths, ges: Total, F7d: 7-day incidence
        var districts = ['hd', 'rnk'];
        var rawdata = json['features'];
        var data_cumul = {};
        var data_dailynew = {};
        var avg_queues = {};
        var headers_cumul = ['Total', 'Recovered', 'Deaths', 'Quarantined'];
        var headers_dailynew = ['Daily new', 'Daily new 7-day average'];
        var colors_cumul = ['red', 'green', 'black', 'orange'];
        var colors_dailynew = ['orange', 'red'];
        var config = {
            responsive: true
        };
        var layout = {
            height: 800
        };
        var d = new Date(0);
        rawdata.sort(function (a, b) { return a['attributes']['date'] - b['attributes']['date'] });
        for (var i=0; i<districts.length; i++) {
            data_cumul[districts[i]] = [];
            data_dailynew[districts[i]] = [];
            avg_queues[districts[i]] = new AvgQueue(7);
            for (var j=0; j<headers_cumul.length; j++) {
                data_cumul[districts[i]].push(
                    {
                        x: [],
                        y: [],
                        name: headers_cumul[j],
                        line: {
                            color: colors_cumul[j]
                        }
                    }
                );
            }
            for (var j=0; j<headers_dailynew.length; j++) {
                data_dailynew[districts[i]].push(
                    {
                        x: [],
                        y: [],
                        name: headers_dailynew[j],
                        line: {
                            color: colors_dailynew[j]
                        }
                    }
                );
            }
            for (var j=0; j<rawdata.length; j++) {
                e = rawdata[j]['attributes'];
                e['date'] = new Date(e['date']).toISOString().substring(0, 10);
                rawdata[j]['attributes']['date'] = e['date'];
                data_dailynew[districts[i]][0]['x'].push(e['date']);
                data_dailynew[districts[i]][0]['y'].push(e['ni_' + districts[i]]);
                data_dailynew[districts[i]][1]['x'].push(e['date']);
                data_dailynew[districts[i]][1]['y'].push(avg_queues[districts[i]].push_and_calc_average(e['ni_' + districts[i]]));
                data_cumul[districts[i]][0]['x'].push(e['date']);
                data_cumul[districts[i]][0]['y'].push(e['ges_' + districts[i]]);
                data_cumul[districts[i]][1]['x'].push(e['date']);
                data_cumul[districts[i]][1]['y'].push(e['gn_' + districts[i]]);
                data_cumul[districts[i]][2]['x'].push(e['date']);
                data_cumul[districts[i]][2]['y'].push(e['vst_' + districts[i]]);
                data_cumul[districts[i]][3]['x'].push(e['date']);
                data_cumul[districts[i]][3]['y'].push(e['af_' + districts[i]]);
            }
            $('.plot-' + districts[i] + '-dailynew').html("");
            $('.plot-' + districts[i] + '-cumul').html("");
            $("#seven-day-incidence-" + districts[i]).html(rawdata[rawdata.length - 1]['attributes']['F7d_' + districts[i]]);
            Plotly.newPlot($('.plot-' + districts[i] + '-dailynew')[0], data_dailynew[districts[i]], layout, config);
            Plotly.newPlot($('.plot-' + districts[i] + '-cumul')[0], data_cumul[districts[i]], layout, config);
        }
        $("#last-updated").html(rawdata[rawdata.length - 1]['attributes']['date']);
    }
    $.getJSON("https://services7.arcgis.com/0Uc5jDlEgdLosloE/arcgis/rest/services/" +
               "dbdata_hd_rnk03/FeatureServer/0/query?where=date%3CCURRENT_TIMESTAMP" +
               "&objectIds=&time=&resultType=none&outFields=date%2Caf_hd%2Caf_rnk%2Cni_hd" +
               "%2Cni_rnk%2Cgn_hd%2Cgn_rnk%2Cvst_hd%2Cvst_rnk%2Cges_hd%2Cges_rnk%2CF7d_hd" +
               "%2CF7d_rnk&f=pjson", function(rawdata) {
        plot_stats(rawdata);
    });
    </script>
