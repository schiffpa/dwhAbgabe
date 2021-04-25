<template>
  <div class="chartContainer">
    <p></p>
    <canvas :id="chartId"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js'
import { trios } from './Utils.js'

var cvs
var ctx
var charts = {}

export default {

    props: ['chartId'],

    mounted() {

        cvs = document.getElementById(this.chartId)
        ctx = cvs.getContext('2d')

        var data = trios()

        charts[this.chartId] = new Chart(ctx, {
            type: 'line',
            data,
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                          autoSkip: true,
                        }
                    }]
                },
                tooltips: {
                    callbacks: {
                        title: function (tooltipItems) {
                            let i = tooltipItems[0].index
                            if (i > data.datasets[0].data.length) return
                            return data.datasets[0].labels[i];
                        }
                    }
                }
            }
        })
    },

    methods: {

        renderChart(data) {

            var chart = charts[this.chartId]
            chart.data = data
            chart.options.tooltips = {
                callbacks: {
                    title: function (tooltipItems) {
                        let i = tooltipItems[0].index
                        if (i > chart.data.datasets[0].data.length) return
                            return chart.data.datasets[0].labels[i];
                    }
                }
            }
            chart.update()
        },
    }
}

</script>

<style>
.chartContainer {
  width: 67%;
  margin: auto;
}
</style>
