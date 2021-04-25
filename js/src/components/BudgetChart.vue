<template>
  <div class="chartContainer">
    <p></p>
    <YearSelector @year="setYearFrom" v-bind:yr="this.from"/>
    <YearSelector @year="setYearTo" v-bind:yr="this.to"/>
    <p></p>
    <canvas :id="chartId"></canvas>
  </div>
</template>

<script>
import YearSelector from './YearSelector'
import Chart from 'chart.js'
import Vue from 'vue'
import { movies } from './Utils.js'

var cvs
var ctx
var charts = {}

export default {

    props: ['chartId'],

    components: {
        YearSelector,
    },

    mounted() {

        cvs = document.getElementById(this.chartId)
        ctx = cvs.getContext('2d')

        var data = movies(this.from, this.to)

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
                        return chart.data.datasets[0].labels[i] + '\n' + chart.data.labels[i];
                    }
                }
            }
            chart.update()

        },

        renderMovies() {
            this.renderChart(movies(this.from, this.to))
        },

        setYearFrom(year) {
            this.from = year
            this.renderMovies()
        },

        setYearTo(year) {
            this.to = year
            this.renderMovies()
        },
    },

    data() {
        return {
            from: 2020,
            to: 2020
        }
    }
}

</script>

<style>
.chartContainer {
  width: 67%;
  margin: auto;
}
</style>
