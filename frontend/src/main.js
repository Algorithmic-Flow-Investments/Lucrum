// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import VueMDCAdapter from "vue-mdc-adapter";
import "./theme.scss";
import App from "./App";
import router from "./router";
import VueSimpleSVG from "vue-simple-svg";
import PortalVue from 'portal-vue'

Vue.use(PortalVue)

Vue.config.productionTip = false;

Vue.use(VueMDCAdapter);

Vue.use(VueSimpleSVG);

var filter = function(text, length, clamp){
	clamp = clamp || '...';
	var node = document.createElement('div');
	node.innerHTML = text;
	var content = node.textContent;
	return content.length > length ? content.slice(0, length) + clamp : content;
};

Vue.filter('truncate', filter);

window.APIROOT = "http://127.0.0.1:5000/"

/* eslint-disable no-new */
new Vue({
	el: "#app",
	router,
	template: "<App/>",
	components: { App }
});
