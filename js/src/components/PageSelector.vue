<template>
    <select class="select" @change="update()">
        <option v-for="page in pages" :key="page">
          {{ page }}
        </option>
    </select>
</template>

<script>
export default {

    mounted() {
        this.$el.selectedIndex = 0
    },
    
    methods: {
        update() {
            this.selected = this.$el.options[this.$el.selectedIndex].value
            this.$emit('page', this.selected)
        }
    },

    data() {
        return { pages: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] }
    }
}
</script>

<style>
</style>
