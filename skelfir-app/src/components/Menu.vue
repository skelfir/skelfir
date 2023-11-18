<script setup>
function closeMenu() {
  document.getElementById('sidemenu').classList.remove('show')
}
</script>

<template>
  <div id="sidemenu" class="slide-in from-left">
    <!--<div class="slide-in-content">-->
      <a href="javascript:void(0)" class="closebtn" v-on:click="closeMenu">&times;</a>
      <a href="#">Map style</a>
      <a href="#">Notification settings</a>
      <a href="#">Magnitude and depth filter</a>
      <a href="#">List view or chart view</a>
      <a href="#">Contact</a>
    <!--</div>-->
  </div>
</template>

<style scoped>
#sidemenu {
  top: 0;
  left: 0;
  position: fixed;
  height: 100vh;
  padding-top: 60px;
  transition: 0.5s;
  background-color: #111;
  opacity: 90%;
  max-width: 70vw;
}

.slide-in {
  z-index: 2;
  position: absolute;
  overflow: hidden;
  transition: transform .5s ease;
}

.slide-in.from-left {
  left: 0;
}

.slide-in-content {
  /*padding: 5px 20px;*/
  /*background: #eee;*/
  transition: transform .5s ease;
}

.slide-in.from-left {
  transform: translateX(-100%);
  -webkit-transform: translateX(-100%);
}

.slide-in.show {
  translate: translateX(0);
  -webkit-transform: translateX(0);
}

.slide-in.from-left .slide-in-content {
  transform: translateX(-100%);
  -webkit-transform: translateX(-100%);
}

.slide-in.show .slide-in-content {
  translate: translateX(0);
  -webkit-transform: translateX(0);
}

body {
  font-family: "Lato", sans-serif;
}

#sidemenu a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 25px;
  color: #818181;
  display: block;
  transition: 0.3s;
}

#sidemenu a:hover {
  color: #f1f1f1;
}

#sidemenu .closebtn {
  position: absolute;
  top: 0;
  right: 25px;
  font-size: 36px;
  margin-left: 50px;
}

@media screen and (max-height: 450px) {
  #sidemenu {padding-top: 15px;}
  #sidemenu a {font-size: 18px;}
}
</style>
