<script setup>
import moment from 'moment'
import mapboxgl from 'mapbox-gl'
import { storeToRefs } from 'pinia'
import { useCounterStore } from '@/stores/counter'
import { ref, watch, onMounted, inject } from 'vue'
//import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'
//import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css'

let popups = []
let map = ref(null)
let loaded = ref(false)
const store = useCounterStore()
const emitter = inject('emitter')
const { quakes, zoom } = storeToRefs(store)

const props = defineProps({
	mapStyle: {
		required: false,
		default: 'mapbox://styles/mapbox/satellite-streets-v12'
	}
})

function loadMap() {
	mapboxgl.accessToken = 'pk.eyJ1IjoibG9naWxlaWZzIiwiYSI6ImNrbTk4bzRwazFmanIycWtuaXdnbnZ0ZTAifQ.eJjqmhjSLkP5eCXQGto8tA'
	map = new mapboxgl.Map({
		container: 'map', // container ID
		// Choose from Mapbox's core styles, or make your own style with Mapbox Studio
		style: props.mapStyle,
		//center: [-68.137343, 45.137451], // starting position
		//center: [-20.786, 64.431],
		center: [-22.165323169098766, 63.92804361154887],
		zoom: zoom.value, // starting zoom
		attributionControl: false,
	})

	/*const geocoder = new MapboxGeocoder({
		accessToken: mapboxgl.accessToken,
		mapboxgl: mapboxgl
	})
	map.addControl(geocoder)*/
}

async function fetchData() {
	await store.fetchQuakes()
}

function removeLayers() {
	var heatLayerExists = false
	var pointLayerExists = false
	var labelLayerExists = false
	if (map.getLayer('heat')) {
		map.removeLayer('heat')
		heatLayerExists = true
	}
	if (map.getLayer('point')) {
		map.removeLayer('point')
		pointLayerExists = true
	}
	if (map.getLayer('labels')) {
		map.removeLayer('labels')
		labelLayerExists = true
	}
	return heatLayerExists || pointLayerExists || labelLayerExists
}

function removeSource() {
	if (map.getSource('quakes')) {
		map.removeSource('quakes')
		return true
	}
	return false
}

function addSource() {
	console.log('addSource')
	//console.log(quakes.value)
	map.addSource('quakes', {
		'type': 'geojson',
		data: quakes.value
	});
}

function addHeatMap() {
	if (map.getLayer('heat')) { map.removeLayer('heat') }
	map.addLayer({
		'id': 'heat',
		'type': 'heatmap',
		'source': 'quakes',
		'maxzoom': 9,
		'paint': {
			// Increase the heatmap weight based on frequency and property magnitude
			'heatmap-weight': [
				'interpolate',
				['linear'],
				['get', 'mag'],
				0,
				0,
				6,
				1
			],
			// Increase the heatmap color weight weight by zoom level
			// heatmap-intensity is a multiplier on top of heatmap-weight
			'heatmap-intensity': [
				'interpolate',
				['linear'],
				['zoom'],
				0,
				1,
				9,
				3
			],
			// Color ramp for heatmap.  Domain is 0 (low) to 1 (high).
			// Begin color ramp at 0-stop with a 0-transparancy color
			// to create a blur-like effect.
			'heatmap-color': [
				'interpolate',
				['linear'],
				['heatmap-density'],
				0,
				'rgba(33,102,172,0)',
				0.2,
				'rgb(103,169,207)',
				0.4,
				'rgb(209,229,240)',
				0.6,
				'rgb(253,219,199)',
				0.8,
				'rgb(239,138,98)',
				1,
				//'rgb(178,24,43)'
				//'rgb(252, 100, 0)'
				'rgb(250, 86, 6)'
			],
			// Adjust the heatmap radius by zoom level
			'heatmap-radius': [
				'interpolate',
				['linear'],
				['zoom'],
				0,
				2,
				9,
				20
			],
			// Transition from heatmap to circle layer by zoom level
			'heatmap-opacity': [
				'interpolate',
				['linear'],
				['zoom'],
				7,
				1,
				9,
				0
			]
		}
	});
}

function addPoints() {
	if (map.getLayer('point')) { map.removeLayer('point') }
	map.addLayer({
		"id": "point",
		"type": "circle",
		"source": "quakes",
		"minzoom": 7,
		"paint": {
			// Size circle radius by earthquake magnitude and zoom level
			"circle-radius": [
				"interpolate",
				["linear"],
				["zoom"],
				7, [
					"interpolate",
					["linear"],
					["get", "mag"],
					1, 1,
					6, 4
				],
				16, [
					"interpolate",
					["linear"],
					["get", "mag"],
					1, 5,
					6, 50
				]
			],
			// Color circle by earthquake magnitude
			"circle-color": [
				"interpolate",
				["linear"],
				["get", "mag"],
				0, "rgba(255, 255, 255, 0)",
				0.5, "rgb(103,169,207)",
				1, "rgb(209,229,240)",
				//2, "rgb(253,219,199)",
				2, 'rgb(252, 232, 121)',
				//3, "rgb(239,138,98)",
				3, "rgb(255, 224, 0)",
				4, 'rgb(250, 86, 6)',
				5, "rgb(178,24,43)"
			],
			"circle-stroke-color": "white",
			"circle-stroke-width": 1,
			// Transition from heatmap to circle layer by zoom level
			"circle-opacity": [
				"interpolate",
				["linear"],
				["zoom"],
				7, 0,
				8, 1
			]
		}
	})
}

function addLabels() {
	if (map.getLayer('labels')) { map.removeLayer('labels') }
	map.addLayer({
		'id': 'labels',
		'type': 'symbol',
		'minzoom': 10,
		'source': 'quakes',
		'layout': {
			'text-field': [
				'concat',
				['to-string', ['get', 'mag']],
				''
			],
			'text-font': [
				'Open Sans Bold',
				'Arial Unicode MS Bold'
			],
			'text-size': 8
		},
		'paint': {
			'text-color': 'rgba(0,0,0,0.5)'
		}
	})
}

function openQuakePopup(quake) {
	//console.log('openQuakePopup', quake)
	//var coordinates = quake.coordinates
	var magnitude = quake.mag
	var depth = quake.depth
	var time = new Date(quake.time)
	var html = "<p><strong>Magnitude: </strong>" + magnitude + "</p>"
	html = html +"<p><strong>Date: </strong>" + moment(time).format('DD.MM.YYYY') + "</p>"
	html = html + "<p><strong>Time: </strong>" + moment(time).format('HH:mm:ss') + "</p>"
	html = html + "<p><strong>Depth: </strong>" + depth + "km</p>"

	// Ensure that if the map is zoomed out such that multiple
	// copies of the feature are visible, the popup appears
	// over the copy being pointed to.
	//while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
	//  coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
	//}

	let popup = new mapboxgl
		.Popup({closeOnClick: false})
		.setLngLat([quake.lon, quake.lat])
		.setHTML(html)
		.addTo(map)
	popups.push(popup)
}

async function initialize() {
	await fetchData()
}

emitter.on('openQuake', (quake) => {
	openQuakePopup(quake)
})

emitter.on('setZoom', (zoomLevel) => {
	map.setZoom(zoomLevel)
})

emitter.on('resetNorth', () => {
	map.resetNorthPitch({duration: 500})
})

watch(quakes, async (current, previous) => {
	var layersRemoved = removeLayers()
	var sourceRemoved = removeSource()
	var timeout = 0
	if (layersRemoved) { timeout = 500 }
	setTimeout(() => {
		addSource()
		addHeatMap()
		addPoints()
		addLabels()
	}, timeout)
})

onMounted(() => {
	loadMap()

	map.on('load', () => {
		console.log('map loaded')
		initialize()
		loaded = true
		map.getCanvas().style.cursor = 'default'
	})

	map.on('click', 'point', function (e) {
		e.clickOnLayer = true
		var quake = {"id": e.features[0].id, ...e.features[0].properties}
		openQuakePopup(quake)
	})

	map.on('click', (e) => {
		if (e.clickOnLayer) {
			// click on some layer - handle elsewhere
			return
		}
		console.log('map click')
		//popups.map((popup) => popup.remove())
	})

	// Change the cursor to a pointer when the mouse is over an earthquake point
	map.on('mouseenter', 'point', function () {
		map.getCanvas().style.cursor = 'pointer'
	})

	// Change it back to default when it leaves
	map.on('mouseleave', 'point', function () {
		map.getCanvas().style.cursor = 'default'
	})

	// This doesn't work well on mobile
	/*map.on('zoom', (e) => {
		zoom.value = map.getZoom()
	})*/

	map.on('zoomend', (e) => {
		zoom.value = map.getZoom()
	})
})
</script>

<template>
	<div id="map"></div>
</template>

<style scoped>
#map {
	position: absolute;
	left: 0;
	top: 0;
	bottom: 0;
	width: 100%;
}
</style>