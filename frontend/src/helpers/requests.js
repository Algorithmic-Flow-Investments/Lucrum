export const api = "http://0.0.0.0:5000/api/v2/"; // The API address
var axios = require("axios")

import Vue from 'vue';
export const EventBus = new Vue();

import {default as MainVue} from '@/main'
/*
Simply wrappers for common HTTP requests. At the moment, this just ensures that all
errors will be printed to the console, however eventually this can be updated
to notify the user, or us, of any network or server errors
 */

export function get(endpoint, options) {
	let opts = options || {};
	return new Promise(function(resolve, reject) {
		axios
			.get(api + endpoint, opts)
			.then(response => {
				resolve(response.data);
			})
			.catch(error => {
				console.log(error.response);
				reject(error);
			});
	});
}

export function post(endpoint, data, options) {
	let opts = options || {};
	EventBus.$emit('sending')
	return new Promise(function(resolve, reject) {
		axios
			.post(api + endpoint, data, opts)
			.then(response => {
				EventBus.$emit('sent');
				resolve(response.data);
			})
			.catch(error => {
				EventBus.$emit('sent');
				console.log("ERROR:", error);
				MainVue.$notification.open({
					duration: 5000,
					message: error.toString(),
					position: 'is-top-right',
					type: 'is-danger',
					hasIcon: true
				})
				reject(error);
			});
	});
}

export function del(endpoint) {
	EventBus.$emit('deleting')
	return new Promise(function(resolve, reject) {
		axios
			.delete(api + endpoint)
			.then(response => {
				EventBus.$emit('deleted')
				resolve(response.data);
			})
			.catch(error => {
				EventBus.$emit('deleted')
				console.log(error.response);
				reject(error);
			});
	});
}

export function patch(endpoint, data) {
	return new Promise(function(resolve, reject) {
		axios
			.patch(api + endpoint, data)
			.then(response => {
				resolve(response.data);
			})
			.catch(error => {
				console.log(error.response);
				reject(error);
			});
	});
}
