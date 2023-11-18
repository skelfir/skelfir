<script setup>
import 'chartjs-adapter-moment'
import Chart from 'chart.js/auto'
import { storeToRefs } from 'pinia'
import zoomPlugin from 'chartjs-plugin-zoom'
import { ref, watch, onMounted, inject } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const emitter = inject('emitter')
const { quakes } = storeToRefs(store)

function getChart() {
	return Chart.getChart("chart")
}

function destroyChart() {
	let quakeChart = Chart.getChart("chart")
	console.log('quakeChart exists')
	console.log(quakeChart)
	quakeChart.destroy()
}

function loadChart() {
	//console.log(quakes.value)
	console.log('loadChart')
	//var data = quakes.value.features.map((item) => { return item })
	var data = quakes.value.features.map((quake) => {
		return {
			'x': quake.properties['time'],
			'y': quake.properties['mag'],
			'lat': quake.properties['lat'],
			'lon': quake.properties['lon'],
			'depth': quake.properties['depth']
		}
	})
	//console.log('data: ', data[0])
	//console.log('data: ', data[data.length-1])
	Chart.register(zoomPlugin)
	new Chart("chart", {
		type: "scatter",
		data: {
			datasets: [{
				pointRadius: 4,
				//pointBackgroundColor: "rgba(255,0,0,1)",
				//data: quakes.value.features.map(function (d) {return d;})
				data: data,
			}]
		},
		options: {
			elements: {
				point: {
					backgroundColor: 'rgba(255, 0, 0, 1)',
					borderColor: 'rgba(0, 0, 0, 1)',
					borderWidth: 1,
				},
			},
			onClick: (e, points) => {
				if (points.length > 0) {
					console.log(points)
					var index = points[0].index
					var quake = quakes.value.features[index].properties
					emitter.emit('openQuake', quake)
				}
			},
			onHover: (e, points) => {
				if (points.length > 0 ) {
					e.chart.canvas.style.cursor = 'pointer'
				}
				else {
					e.chart.canvas.style.cursor = 'default'
				}
			},
			plugins: {
				legend: {
					display: false
				},
				zoom: {
					zoom: {
						wheel: {
							enabled: true,
						},
						pinch: {
							enabled: true
						},
						mode: 'y',
						limits: {
							y: {min: 0, max: 2},
						},
					}
				}
			},
			maintainAspectRatio: false,
			scales: {
				x: {
					type: 'time',
					position: 'bottom',
					time: {
						unit: 'hour',
						displayFormats: {
							day: 'MMM DD',
							hour: 'HH:mm',
						}
					},
					ticks: {
						major: {
							enabled: true
						}
					},
				},
				y: {
					suggestedMin: 0,
					suggestedMax: 6,
					ticks: {
						stepSize: 2,
					},
				},
			}
		},
	})
}

//onMounted(() => {
//	loadChart()
//})

watch(quakes, async (current, previous) => {
	//console.log('watch')
	//console.log(current)
	//console.log(`quakes: ${quakes}`)
	let chart = getChart()
	console.log(chart)
	if (chart) {
		destroyChart()
		console.log('chart exists')
	}
	loadChart()
})
</script>

<template>
	<div id="chart-container">
		<canvas id='chart'></canvas>
		<a href="">Reset zoom</a>
		<button>Reset</button>
	</div>
</template>

<style scoped>
#chart {
	width: 100%;
	-webkit-tap-highlight-color: rgba(0, 0, 0, 0);
	-moz-tap-highlight-color: rgba(0, 0, 0, 0);
}

#chart-container {
	position: absolute;
	left: 0;
	bottom: 0;
	width: 100%;
	height: 25%;
}

button {
	position: absolute;
  left: 0vw;
  bottom: 1.5vh;
}
</style>
