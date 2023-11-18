import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import mitt from 'mitt'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'
/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
/* import specific icons */
import {
  faUserSecret,
  faBars,
  faRedoAlt,
  faSearch,
  faCompass,
} from '@fortawesome/free-solid-svg-icons'
/* add icons to the library */
library.add(faUserSecret)
library.add(faBars)
library.add(faRedoAlt)
library.add(faSearch)
library.add(faCompass)

const app = createApp(App)
const emitter = mitt()
const pinia = createPinia()

app.config.globalProperties.emitter = emitter
app.provide('emitter', emitter)
app.use(pinia)

app.component('font-awesome-icon', FontAwesomeIcon).mount('#app')
