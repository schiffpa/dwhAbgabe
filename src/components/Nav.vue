<template>
  <div class="nav">
    <a href="#" @click="drawBudget" v-bind:style= "[budget ? {background: '#ddd'} : {background: '#fff'}]">Budget</a>
    <p>
        <a href="#" @click="drawActors" v-bind:style= "[actors ? {background: '#ddd'} : {background: '#fff'}]">Schauspieler</a>
        <a href="#" @click="drawTrios" v-bind:style= "[trios ? {background: '#ddd'} : {background: '#fff'}]">Trios</a>
        <a href="#" @click="drawQuartets" v-bind:style= "[quartets ? {background: '#ddd'} : {background: '#fff'}]">Quartets</a>
    </p>
    <a href="#" @click="drawStudios" v-bind:style= "[studios ? {background: '#ddd'} : {background: '#fff'}]">Produzenten</a>
    <p></p>
    <BudgetChart chartId="myChart" v-if="budget"/>
    <StudiosChart chartId="myChart2" v-if="studios"/>
    <ActorsChart chartId="myChart3" v-if="actors"/>
    <TriosChart chartId="myChart4" v-if="trios"/>
    <QuartetsChart chartId="myChart4" v-if="quartets"/>
  </div>
</template>

<script>
import StudiosChart from './StudiosChart'
import BudgetChart from './BudgetChart'
import ActorsChart from './ActorsChart'
import TriosChart from './TriosChart'
import QuartetsChart from './QuartetsChart'

export default {

    components: {
        BudgetChart,
        StudiosChart,
        ActorsChart,
        TriosChart,
        QuartetsChart,
    },

    data() {
        return {
            budget: 0,
            studios: 0,
            actors: 0,
            trios: 0,
            quartets: 0,
        }
    },

    methods: {

        drawBudget() {
            this.budget = !this.budget
            this.studios = 0
            this.actors = 0
            this.apriori = 0
            this.quartets = 0
            this.trios = 0
        },
        
        drawStudios() {
            this.budget = 0
            this.actors = 0
            this.apriori = 0
            this.quartets = 0
            this.trios = 0
            this.studios = !this.studios
        },

        drawActors() {
            this.budget = 0
            this.studios = 0
            this.apriori = 0
            this.quartets = 0
            this.trios = 0
            this.actors = !this.actors
        },

        drawTrios() {
            this.budget = 0
            this.studios = 0
            this.actors = 0
            this.quartets = 0
            this.trios = !this.trios
        },

        drawQuartets() {
            this.budget = 0
            this.studios = 0
            this.actors = 0
            this.trios = 0
            this.quartets = !this.quartets
        }

    },
}

</script>

<style>
.nav {

    padding: 10px;
}

.nav a {

    margin: 5px;
    padding: 5px;
    border: 1px solid black;
    border-radius: 3px;
}
</style>
