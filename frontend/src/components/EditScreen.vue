<template>
	<div :class="{'fullpage': true, 'active': active}">
		<span @click="close()"><i class="material-icons mdc-button__icon back">arrow_back</i></span>
		<edit-target @close="close()" v-if="editTarget"></edit-target>
		<select-target @close="close()" @new="newTarget()" v-if="selectTarget"></select-target>

		<edit-method @close="close()" v-if="editMethod"></edit-method>
		<select-method @close="close()" @new="newMethod()" v-if="selectMethod"></select-method>
	</div>
</template>

<script>
	import EditTarget from "@/components/EditTarget";
	import SelectTarget from "@/components/SelectTarget";
	import EditMethod from "@/components/EditMethod";
	import SelectMethod from "@/components/SelectMethod";
	import { EventBus } from '../event-bus.js';
	import axios from "axios";


	export default {
		name: 'EditScreen',
		data() {
			return {
				active: false,
				editTarget: false,
				selectTarget: false,
				editMethod: false,
				selectMethod: false
			}
		},
		components: {
			EditTarget,
			SelectTarget,
			EditMethod,
			SelectMethod
		},
		watch:{
			'$route' (to, from) {
				this.check()
			}
		},
		methods: {
			close() {
				this.active = false
				this.$router.push({params: {edit: null}})
				EventBus.$emit('edit/close')
			},
			reset() {
				this.selectTarget = false
				this.editTarget = false
				this.selectMethod = false
				this.editMethod = false
			},
			newTarget(){
				this.selectTarget = false
				this.editTarget = true
			},
			newMethod(){
				this.selectMethod = false
				this.editMethod = true
			},
			check(){
				if (this.$route.params.edit){
					this.active = true
					if (this.$route.params.transactionId){
						this.reset()
						axios.get(window.APIROOT + "api/transaction/" + this.$route.params.transactionId).then(response => {
							if (this.$route.params.edit === 'target'){
								if (response.data.target.id === -1) {
									this.selectTarget = true
								}
								else {
									this.editTarget = true
								}
							}
							else if (this.$route.params.edit === 'method') {
								if (response.data.method) {
								  	this.editMethod = true
								}
								else {
								  	this.selectMethod = true
								}
							}
						})
					}
				}
			}
		},
		mounted() {
		  setTimeout(this.check(), 250)
		}
	}
</script>

<style scoped>
.fullpage {
	height: 100vh;
	width: 100vw;
	position: fixed;
	top: 0;
	background: #1eb980;
	z-index: 20;
	transition: left;
	transition-duration: 0.5s;
	left: 100vw;
}

.active {
	left: 0;
}

.back {
	color: rgb(55, 55, 64);
	font-size: 24px;
	padding: 15px;
}
</style>
