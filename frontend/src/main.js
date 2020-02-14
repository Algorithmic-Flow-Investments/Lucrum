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

import VueResizeText from 'vue-resize-text';

Vue.use(VueResizeText)

import store from '@/store'


Vue.mixin({
	computed: {
		l_targets() {
			return this.$store.state.targets
		},
		l_methods() {
			return this.$store.state.methods
		},
		l_accounts() {
			return this.$store.state.accounts
		},
		l_tags() {
			return this.$store.state.tags
		},
		l_categories() {
			return this.$store.state.categories
		}
	},
	methods: {

	}
})


/* eslint-disable no-new */
export default new Vue({
	el: "#app",
	router,
	template: "<App/>",
	components: { App },
	store,
	data() {
		return {
			testshared: 'a'
		}
	},
	create() {
		return undefined;
	}
});
