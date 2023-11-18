<script setup>
import { ref, onMounted } from 'vue'
import * as notifier from '@/notifier'
import Map from './components/Map.vue'
import Menu from './components/Menu.vue'
import Chart from './components/Chart.vue'
import Controls from './components/Controls.vue'
import Popups from './components/Popups.vue'
//import { storeToRefs } from 'pinia'
//import { useCounterStore } from '@/stores/counter'

//const store = useCounterStore()
//const { quakes } = storeToRefs(store)

notifier.initialize()

let socket = new WebSocket("wss://www.seismicportal.eu/standing_order/websocket");
socket.onopen = function() {
  console.log('connected')
}

socket.onmessage = function(e) {
  console.log('socket onmessage')
  console.log(e)
  var msg = JSON.parse(e.data)
  console.log('new earthquake: ', msg)
}

socket.onclose = function() {
  console.log('disconnected')
}
</script>

<template>
  <main>
    <!--<Popups></Popups>-->
    <Map></Map>
    <Menu></Menu>
    <!--<div id="sidemenu2" v-on:click="toggleMenu" class="slide-in from-left" >
      <div class="slide-in-content">
        <ul>
          <li>Lorem</li>
          <li>Ipsum</li>
          <li>Dolor</li>
        </ul>
      </div>
    </div>-->
    <Controls></Controls>
    <Chart></Chart>
  </main>
</template>

<style scoped>
.slide-in {
  z-index: 2;
  position: absolute;
  overflow: hidden;
}

.slide-in.from-left {
  left: 0;
}

.slide-in-content {
  padding: 5px 20px;
  background: #eee;
  transition: transform .5s ease;
}

.slide-in.from-left .slide-in-content {
  transform: translateX(-100%);
  -webkit-transform: translateX(-100%);
}

.slide-in.show .slide-in-content {
  translate: translateX(0);
  -webkit-transform: translateX(0);
}

header {
  line-height: 1.5;
}

.quake-chart {
  position: absolute;
  background-color: blue;
  left: 0;
  bottom: 0;
  width: 100%;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
