import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex)
import * as requests from "@/helpers/requests";
import Target from "@/Models/Target";
import Method from "@/Models/Method";
import Account from "@/Models/Account";
import Tag from "@/Models/Tag";
import Category from "@/Models/Category";

export default new Vuex.Store({
	state: {
		targets: [],
		methods: [],
		accounts: [],
		tags: [],
		categories: []
	},
	mutations: {
		updateTargets(state, data) {
			state.targets = data
		},
		updateMethods(state, data) {
			state.methods = data
		},
		updateAccounts(state, data) {
			state.accounts = data
		},
		updateTags(state, data) {
			state.tags = data
		},
		updateCategories(state, data) {
			state.categories = data
		}
	},
	actions: {
		fetch_targets({ commit }) {
			return new Promise(function(resolve, reject) {
				requests.get("targets/list").then(targets => {
					commit('updateTargets', targets.map(t => new Target(t)))
					console.log("Vuex> Fetched targets")
					resolve()
				})
			})
		},
		fetch_methods({ commit }) {
			return new Promise(function(resolve, reject) {
				requests.get("methods/list").then(methods => {
					commit('updateMethods', methods.map(m => new Method(m)))
					resolve()
				})
			})
		},
		fetch_accounts({ commit }) {
			return new Promise(function(resolve, reject) {
				requests.get("accounts/list").then(accounts => {
					commit('updateAccounts', accounts.map(m => new Account(m)))
					resolve()
				})
			})
		},
		fetch_tags({ commit }) {
			let store = this.state
			return new Promise(function(resolve, reject) {
				requests.get("tags/list").then(tags => {
					commit('updateTags', tags.map(t => new Tag(t)))
					store.tags.forEach(tag => tag.category = tag.getCategory())
					resolve()
				})
			})
		},
		fetch_categories({ commit }) {
			let store = this.state
			return new Promise(function(resolve, reject) {
				requests.get("categories/list").then(categories => {
					commit('updateCategories', categories.map(c => new Category(c)))
					store.tags.forEach(tag => tag.category = tag.getCategory())
					resolve()
				})
			})
		}
	}
})
