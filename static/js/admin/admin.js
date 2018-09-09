/**
 * Created by prathyushsp on 16/10/16.
 */

var admin_socket = '';
var cpuData = [];
var ramData = [];
var updateInterval = 1000;
var i = 0;
var j = 0;


$(document).ready(function () {
    admin_socket = io.connect();
    admin_socket.on('connect', function () {
        admin_socket.emit('admin_status', {init: 'Admin Connected'});
    });
    admin_socket.emit('status');
    admin_socket.on('status_response', function (res) {
        $('#active_threads').text(res.thread_usage);
        $('#disk_space').text(res.disk_usage.used);
        $('#disk_space_util').text(res.disk_usage.used_p);
        $('#ram_space').text(res.ram_usage.used);
        $('#ram_space_util').text(res.ram_usage.used_p);
        $('#cpu_usage').text(res.cpu_usage.used);
        $('#free_cpu').text(res.cpu_usage.free);
        cpuData.push([i++, parseFloat(res.cpu_usage.used)]);
        ramData.push([j++, parseInt(res.ram_usage.used_p)]);
        setTimeout(function () {
            admin_socket.emit('status');
        }, 2000);
    });

    function getCpuData() {
        if (cpuData.length > 5)
            cpuData = cpuData.slice(1);
        return cpuData;
    }

    function getRamData() {
        if (ramData.length > 5)
            ramData = ramData.slice(1);
        return ramData;
    }

    $("#updateInterval").val(updateInterval).change(function () {
        var v = $(this).val();
        if (v && !isNaN(+v)) {
            updateInterval = +v;
            if (updateInterval < 1) {
                updateInterval = 1;
            } else if (updateInterval > 2000) {
                updateInterval = 2000;
            }
            $(this).val("" + updateInterval);
        }
    });

    var cpuPlot = $.plot("#cpu_plot", [getCpuData()], {
        series: {
            shadowSize: 0	// Drawing is faster without shadows
        },
        yaxis: {
            min: 0,
            max: 100
        },
        xaxis: {
            show: true
        }
    });

    var ramPlot = $.plot("#ram_plot", [getRamData()], {
        series: {
            shadowSize: 0	// Drawing is faster without shadows
        },
        yaxis: {
            min: 0,
            max: 100
        },
        xaxis: {
            show: true
        }
    });

    function update() {
        cpuPlot.setData([getCpuData()]);
        ramPlot.setData([getRamData()]);
        cpuPlot.setupGrid();
        ramPlot.setupGrid();
        cpuPlot.draw();
        ramPlot.draw();
        setTimeout(update, updateInterval);
    }

    update();
});