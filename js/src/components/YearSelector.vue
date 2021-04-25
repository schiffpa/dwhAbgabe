<template>
    <select class="select" @click="update()">
        <option v-for="year in years" :key="year">
          {{ year }}
        </option>
    </select>
</template>

<script>
export default {

    props: ["yr"],

    mounted() {
        this.$el.value = this.yr 
    },
    
    methods: {
        update() {
            this.selected = this.$el.options[this.$el.selectedIndex].value
            this.$emit('year', this.selected)
        },
        getYears() {
            console.log('salam')
        }
    },

    data() {
        return { years: ["2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000","1999","1998","1997","1996","1995","1994","1993","1992","1991","1990","1989","1988","1987","1986","1985","1984","1983","1982","1981","1980","1979","1977","1976","1975","1974","1973","1972","1971","1970","1966","1964","1963","1962","1961","1959","1956","1955","1953","1951","1950","1942","1941","1940","1939","1937"] }
    }
}
</script>

<style>
</style>
