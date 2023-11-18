<script setup>
import { ref, watch, inject } from 'vue'
import { storeToRefs } from 'pinia'
import { useCounterStore } from '@/stores/counter'

const emitter = inject('emitter')
const store = useCounterStore()
const { quakes, zoom } = storeToRefs(store)

async function resetNorth() {
  emitter.emit('resetNorth')
}

async function fetchData() {
  await store.fetchQuakes()
}

function openMenu() {
  document.getElementById('sidemenu').classList.add('show')
}

function closeMenu() {
  document.getElementById('sidemenu').classList.remove('show')
}

function toggleMenu() {
  var sidemenu = document.getElementById('sidemenu')
  var classlist = sidemenu.classList
  if (sidemenu.classList.contains('show')) {
    closeMenu()
  }
  else {
    openMenu()
  }
}

watch(zoom, async(current, previous) => {
  emitter.emit('setZoom', current)
})
</script>

<template>
  <div class="controls">
    <div class="innercontrols">
      <!--<font-awesome-icon class="controlbutton" :icon="['fas', 'search']" />-->
      <div class="slidercontainer">
        <input id="zoomslider" type="range" orient="vertical" step="0.125" min="0" max="22" v-model="zoom"/>
      </div>
      <font-awesome-icon class="controlbutton" v-on:click="resetNorth" :icon="['fas', 'compass']" />
      <font-awesome-icon class="controlbutton" v-on:click="fetchData" :icon="['fas', 'redo-alt']" size="xl"/>
      <font-awesome-icon class="controlbutton" v-on:click="toggleMenu" :icon="['fas', 'bars']" size="xl"/>
    </div>
  </div>
</template>

<style scoped>
.controls {
  z-index: 1;
  position: absolute;
  top: 0;
  right: 0em;
  display: flex;
  height: 73%;
}

.innercontrols {
  display: flex;
  flex-direction: column;
  align-self: flex-end;
  align-items: center;
}

.controlbutton {
  font-size: 2.5em;
  cursor: pointer;
  margin-top: 0.35em;
}

.controlbutton:active {
  transform: translateY(5%);
}

#zoomslider {
  appearance: slider-vertical;;
  -webkit-appearance: slider-vertical;;
  /*margin-right: 50%;*/
  -webkit-transform: rotate(180deg);
  transform: rotate(180deg);
  width: 5em;
}

.slidercontainer {
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  margin-top: 0.5em;
}

#zoomslider::-webkit-slider-runnable-track {
    /*width: 300px;*/
    background: #ddd;
    /*border: none;*/
    border-radius: 6px;
    cursor: pointer;
}

#zoomslider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  /*border-radius: 50%;*/
  width: 25px;
  height: 25px;
  background: var(--color-text);
  cursor: pointer;
  /*-webkit-transform: rotate(90deg);
  transform: rotate(90deg);*/
}

input[type=range]:focus::-webkit-slider-runnable-track {
    background: #ccc;
}
</style>