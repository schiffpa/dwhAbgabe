<template>
  <div class="chartContainer">
    <YearSelector @year="setYearFrom"/>
    <YearSelector @year="setYearTo"/>
    <PageSelector @page="setPage"/>
    <p></p>
    <canvas :id="chartId"></canvas>
  </div>
</template>

<script>
import YearSelector from './YearSelector'
import PageSelector from './PageSelector'
import Chart from 'chart.js'
import { movies, studios } from './Utils.js'

var cvs
var ctx
var charts = {}

var from = 2020
var to = 2020
var page = 1

export default {

    props: ['chartId'],

    components: {
        YearSelector,
        PageSelector,
    },

    mounted() {

        cvs = document.getElementById(this.chartId)
        ctx = cvs.getContext('2d')

        var data = movies(from, to)

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
                            return data.datasets[0].labels[i] + '\n' + data.labels[i];
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
                        return chart.data.datasets[0].labels[i] || 'Studio' + '\n' + chart.data.labels[i];
                    }
                }
            }
            chart.update()

        },

        renderMovies() {
            this.renderChart(movies(from, to))
        },

        renderStudios() {
            this.renderChart(studios(page))
        },

        setYearFrom(year) {
            from = year
            this.renderMovies()
        },

        setYearTo(year) {
            to = year
            this.renderMovies()
        },

        setPage(p) {
            page = p
            this.renderStudios()

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
