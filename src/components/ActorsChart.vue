<template>
  <div class="chartContainer">
    <PageSelector @page="setPage"/>
    <p></p>
    <canvas :id="chartId"></canvas>
  </div>
</template>

<script>
import PageSelector from './PageSelector'
import Chart from 'chart.js'
import { actors } from './Utils.js'

var cvs
var ctx
var charts = {}

var page = 1

export default {

    props: ['chartId'],

    components: {
        PageSelector,
    },

    mounted() {

        cvs = document.getElementById(this.chartId)
        ctx = cvs.getContext('2d')

        var data = actors(page)

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
                            return data.labels[i];
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
                        return chart.data.labels[i];
                    }
                }
            }
            chart.update()
        },

        setPage(p) {
            page = p
            this.renderChart(actors(page))
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
