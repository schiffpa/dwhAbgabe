<template>
    <select class="select" @change="update()">
        <option v-for="group in groups" :key="group">
          {{ group }}
        </option>
    </select>
</template>

<script>
export default {

    mounted() {
        this.$el.selectedIndex = 1
    },
    
    methods: {
        update() {
            this.selected = this.$el.options[this.$el.selectedIndex].value
            this.$emit('group', this.selected)
        }
    },

    data() {
        return { groups: [10, 50, 100, 500, 1000] }
    }
}
</script>

<style>
</style>
