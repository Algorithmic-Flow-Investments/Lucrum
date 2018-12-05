<template>
	<div :class="{'segment': true, 'active': active}" :style="addStyle" @click.self="activate">
		<div class="colour" :style="{background: (target.internal) ? '#789BFF' : (amount < 0) ? 'rgb(255, 104, 89)' : 'rgb(255, 220, 120)'}"></div>
		<div class="content left">
			<mdc-text typo='headline6' tag="span" adjust-margin>{{target.name | truncate(18, '...')}}</mdc-text>
			<mdc-text typo='subtitle2' tag="span" adjust-margin>{{formatDate}}</mdc-text>
		</div>
		<div class="content right" :style="rightAddStyle">
			<div class="text">
				<mdc-icon v-if="target.internal" icon="compare_arrows" class="pre-right" style="font-size: 14px"></mdc-icon>
				<mdc-text v-else-if="amount < 0"  typo='headline4' tag="span" class="pre-right" adjust-margin>-</mdc-text>
				<mdc-text typo='headline4' tag="span" adjust-margin style="float:left">£</mdc-text>
				<mdc-text typo='headline4' tag="span" adjust-margin>{{numberWithCommas(Math.abs(amount))}}</mdc-text>
			</div>
			<mdc-icon v-if="!active" icon="chevron_right" style="color: #AEAEB1;line-height: 48px;vertical-align: top;"></mdc-icon>
		</div>
		<div class="extra" v-show="active">
			<mdc-text typo='headline6' tag="span" class="raw" :style="rawStyle" adjust-margin>{{extra.raw}}</mdc-text>
			<mdc-text typo='headline6' tag="span" class="target" adjust-margin @click.stop="activateTarget">{{(!target.exists) ? 'Set Target' : target.name}}
				<mdc-icon v-if="!target.exists" icon="add_circle" style="color: #AEAEB1;line-height: 28px;vertical-align: top;font-size: 16px;"></mdc-icon>
				<mdc-icon v-else icon="edit" style="color: #AEAEB1;line-height: 28px;vertical-align: top;font-size: 16px;opacity: 0.1;"></mdc-icon></mdc-text>

			<mdc-text typo='headline6' tag="span" class="method" adjust-margin @click.stop="activateMethod">{{(extra.method == null) ? 'Set Method' : extra.method.name}}
				<mdc-icon v-if="extra.method == null" icon="add_circle" style="color: #AEAEB1;line-height: 28px;vertical-align: top;font-size: 16px;"></mdc-icon>
				<mdc-icon v-else icon="edit" style="color: #AEAEB1;line-height: 28px;vertical-align: top;font-size: 16px;opacity: 0.1;"></mdc-icon></mdc-text>
		</div>
	</div>
</template>

<script>
	import moment from 'moment'
	import axios from "axios";
	import EditTarget from "@/components/EditTarget";
	import Vue from "vue";


	import { EventBus } from '../event-bus.js';

	export default {
		name: 'TransactionSegment',
		props: ['amount', 'target', 'tags', 'date', 'tid'],
	  	components: {EditTarget},
		data () {
			return {
				active: false,
			  	extra: {
				  raw: '',
				  method: null
				},
			  editTarget: false
			}
		},
		methods: {
			numberWithCommas (x) {
				return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
			},
			fetchData() {
				axios.get(window.APIROOT + "api/transaction/" + this.tid).then(response => {
				  this.extra = response.data;
				  //this.target = this.extra.target;
				  setTimeout(() => {
					if (this.active && this.$route.params.edit == 'target'){
					  this.activateTarget()
					}
				  }, 250)
				});
			},
			activate(){
				this.active = !this.active
				if (this.active){
					this.fetchData()
				  	this.$router.push({params: {transactionId: this.tid}})
				}
				else {
				  this.$router.push({params: {transactionId: null}})
				}
			},
		  	activateTarget(){
			  this.$router.push({params: {edit: 'target'}})
			  EventBus.$on('edit/close', () => {
			    this.fetchData()
			  })
			},
		  activateMethod(){
			this.$router.push({params: {edit: 'method'}})
			EventBus.$on('edit/close', () => {
			  this.fetchData()
			})
		  },
		},
		computed: {
			addStyle(){
				if (this.active){
					return {'transform': 'translateY(' + -(this.$el.offsetTop - this.$parent.$el.offsetTop - this.$parent.$parent.$el.scrollTop) +'px)',
						'height': this.$parent.$parent.$el.offsetHeight + 'px'}
				}
				return {}
			},
		  rightAddStyle(){
			  if (this.active){
			    let style = window.getComputedStyle(this.$el.getElementsByClassName('right')[0])
				//return {'padding-right': '100%'}
			    //return {'padding-right': 'calc(50% - ' + parseInt(style.width) / 2 + 'px' + ')'}
			  }
			  return {}
		  },
		  rawStyle() {
			if (this.active) {
			  let ts = parseInt(window.getComputedStyle(this.$el.getElementsByClassName('raw')[0]).width) / (this.extra.raw.length * 2.2)  + 'vw'
			  return {'font-size': ts}
			}
		  },
		  formatDate() {
			  return moment(this.date).format('ddd, D MMM YYYY')
		  }
		},
		mounted() {
		  setTimeout(() => {
			if(this.$route.params.transactionId == this.tid){
			  this.activate()
			}
		  }, 250)
		}
	}
</script>

<style scoped>

	.colour {
		width: 5px;
		height: 48px;
		display: inline-block;
		top: 0;
		position: relative;
		transition: height, top;
		transition-duration: .2s;
	}

	.content {
		display: inline-block;
		height: 48px;
		vertical-align: top;
	}

	.pre-right {
		float:left;
		padding-right:5px;
		line-height: 48px;
		color: white;
	}

	.right {
		float: right;
		text-align: right;
		transition: top, right, transform, padding;
		transition-duration: .2s;
		right: 0;
		position: relative;
	}

	.left {
		-webkit-transform-origin-x: 0;
		font-size: 16px;
		transition: top, padding, opacity;
		transition-duration: .2s;
		top: 0;
		position: relative;
	}

	.text {
		width: 180px;
		display: inline-block;
		font-size: 16px;
		transition: font-size;
		transition-duration: .2s;
	}

	.active .left {
		top: 100px;
		left: -999px;
		position: relative;
		opacity: 0;
		transition-duration: 0s;
	}

	.active .right {
		right: 50%;
		position: relative;
		transform: translateX(50%);
	}

	.active .right .text {
		font-size: 150% !important;
	}

	.active .colour {
		width: 90%;
		height: 5px;
		display: block;
		top: 48px;
		position: relative;
		transition-property: width, height, top, margin-left;
		transition-duration: .2s;
		margin-left: 5%;
	}

	.raw {
		width: 100%
	}

	.target {
		font-size: 1.5em !important;
	}

	.extra {
		padding: 1% 5% 1% 5%;
		font-size: 80%;
	}

	.editDialog {

	}

	.segment {
		padding-bottom: 10px;
		padding-top: 10px;
		border-bottom: 1px solid #32333D;
		height: 52px;
		transition: height, transform;
		transition-duration: .2s;
		z-index: 0;
		background: rgb(55, 55, 64);
	}

	.segment.active {
		z-index: 10;
	}

	.mdc-typography--headline6 {
		font-family: 'Roboto Condensed';
		font-size: 1.25em;
		color: white;
		display: block;
		letter-spacing: 0.04em;
		line-height: 26px;
	}

	.mdc-typography--headline4 {
		font-family: 'Eczar';
		color: white;
		letter-spacing: 0.05em;
		line-height: 48px;
		font-size: 212.5%
	}

	.mdc-typography--subtitle2 {
		font-family: 'Roboto Condensed';
		font-size: 0.875em;
		color: #AEAEB1;
		letter-spacing: 0.05em;
		line-height: 24px;
	}



	@media (max-width: 1640px) and (min-width: 1480px) {
		.text {
			font-size: 14px;
			width: 150px;
		}
		.left {
			font-size: 14px;
		}
	}

	@media (max-width: 1480px) and (min-width: 1350px) {
		.text {
			font-size: 12px;
			width: 130px;
		}
		.left {
			font-size: 12px;
		}
	}

	@media (max-width: 1350px) and (min-width: 1100px) {
		.text {
			font-size: 10px;
			width: fit-content;
		}
		.left {
			font-size: 10px;
		}
	}

	@media (max-width: 1100px) and (min-width: 1000px) {
		.text {
			font-size: 8px;
			width: fit-content;
		}
		.left {
			font-size: 9px;
		}
	}

	@media (max-width: 1000px) and (min-width: 839px) {
		.text {
			font-size: 6px;
			width: fit-content;
		}
		.left {
			font-size: 8px;
		}
	}

	/* Tablet */

	@media (max-width: 660px) and (min-width: 590px) {
		.text {
			font-size: 14px;
			width: 150px;
		}
		.left {
			font-size: 14px;
		}
	}

	@media (max-width: 590px) and (min-width: 540px) {
		.text {
			font-size: 12px;
			width: 130px;
		}
		.left {
			font-size: 12px;
		}
	}

	@media (max-width: 540px) and (min-width: 479px) {
		.text {
			font-size: 10px;
			width: fit-content;
		}
		.left {
			font-size: 12px;
		}
	}

	/* Phone */

	@media (max-width: 479px) and (min-width: 320px) {
		.text {
			font-size: 12px;
			width: fit-content;
		}
		.left {
			font-size: 12px;
		}
	}

	@media (max-width: 320px) {
		.text {
			font-size: 8px;
			width: fit-content;
		}
		.left {
			font-size: 10px
		}
	}


</style>
