import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const quakes = ref(null)
  const zoom = ref(8)

  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  async function fetchQuakes() {
    console.log('fetching quakes')
    fetch('https://skelfir.com/quakes', {method: 'GET'})
    .then(response => {
      console.log(`response status: ${response.status}`)
      if (response.status >= 200 && response.status <= 299) {
        return response.json()
      } else {
        throw Error(response.status)
      }
    })
    .then(data => {
      console.log('data recieved: ', data)
      this.quakes = data
      //map.removeLayer('earthquakes-heat')
      //map.removeLayer('earthquakes-point')
      //map.removeLayer('earthquake-labels')
      //addSource()
      //addLayers()
      //setChart()
      //window.history.pushState('page2', 'Skelfir', window.location.href);
      //return this.quakes
    })
  }

  return { count, doubleCount, increment, fetchQuakes, quakes, zoom }
})
