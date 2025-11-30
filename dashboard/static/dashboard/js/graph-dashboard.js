document.addEventListener('DOMContentLoaded', function () {
    const chartElement = document.querySelector("#statusChart");
    const activeCount = parseInt(chartElement.dataset.active);
    const inactiveCount = parseInt(chartElement.dataset.inactive);

    var statusChart = new ApexCharts(chartElement, {
        chart: {
            type: 'donut',
            height: 300,
            fontFamily: 'inherit',
        },
        series: [activeCount, inactiveCount],
        labels: ['Active', 'Inactive'],
        colors: ['#0055ff', '#ff3e1d'],
        legend: { position: 'bottom' },
        plotOptions: {
            pie: {
                donut: {
                    size: '65%',
                    labels: {
                        show: true,
                        value: {
                            formatter: val => val + '%'
                        }
                    }
                }
            }
        }
    });

    statusChart.render();
});
