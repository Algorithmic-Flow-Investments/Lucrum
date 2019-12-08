// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App";
import router from "./router";

Vue.config.productionTip = false;

import Buefy from "buefy";

import "../node_modules/@fortawesome/fontawesome-free/css/all.css";

Vue.use(Buefy, {
	defaultIconPack: "fas"
});

import { Laue } from 'laue';

Vue.use(Laue);

/* eslint-disable no-new */
export default new Vue({
	el: "#app",
	router,
	template: "<App/>",
	components: { App }
});
