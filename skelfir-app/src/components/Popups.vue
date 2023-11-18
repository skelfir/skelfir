<script setup>
</script>

<template>
  <div class="bubblecontainer">
	  <div class="bubble">
	    <p>New earthquake!</p>
	  </div>
	</div>
</template>

<style scoped>
.bubblecontainer {
  /*top: 5%;
  position: absolute;
  width: 20%;
  height: 20%;*/

  z-index: 2;
  position: fixed;
  top: 5%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.bubble {
  background-color: blue;
}
</style>