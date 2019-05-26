<template>
	<div class="segment" :class="{ active: active }" :style="addStyle" @click.self="activate">
		<div
			class="colour"
			:style="{
				background: target.internal ? '#789BFF' : transaction.amount < 0 ? 'rgb(255, 104, 89)' : 'rgb(255, 220, 120)'
			}"
			@click="activate"
		></div>
		<div class="content left" @click="activate">
			<mdc-text typo="headline6" tag="span" adjust-margin>{{ name | truncate(truncateLength, "...") }} </mdc-text>
			<mdc-text typo="subtitle2" tag="span" adjust-margin>{{ formatDate }} </mdc-text>
		</div>
		<div class="content right" :style="rightAddStyle" @click="activate">
			<mdc-icon class="sign" icon="compare_arrows" v-if="target.internal"></mdc-icon>
			<mdc-text v-else-if="transaction.amount < 0" typo="headline4" tag="span" class="sign" adjust-margin>- </mdc-text>
			<div class="text">

				<mdc-text typo="headline4" tag="span" adjust-margin style="float:left">£ </mdc-text>
				<mdc-text typo="headline4" tag="span" adjust-margin>{{ numberWithCommas(Math.abs(transaction.amount)) }} </mdc-text>
			</div>
			<mdc-icon v-if="!active" icon="chevron_right" style="color: #AEAEB1;line-height: 48px;vertical-align: top;"></mdc-icon>
		</div>
		<div class="extra" v-show="active">
			<mdc-text typo="headline6" tag="span" class="raw" :style="rawStyle" adjust-margin>{{ transaction.raw }} </mdc-text>
			<mdc-text typo="headline6" tag="span" class="target" adjust-margin @click.stop="activateTarget"
				>{{ !transaction.target ? "Set Target" : target.name }}
				<mdc-icon v-if="!transaction.target" icon="add_circle" style="color: #AEAEB1;line-height: 28px;vertical-align: top;font-size: 16px;"></mdc-icon>
				<mdc-icon v-else icon="edit" style="color: #AEAEB1;line-height: 28px;vertical-align: top;font-size: 16px;opacity: 0.1;"></mdc-icon>
			</mdc-text>

			<mdc-text typo="headline6" tag="span" class="method" adjust-margin>
				{{ !transaction.method ? "Unknown Method" : transaction.method.name }}
			</mdc-text>

			<div class="tags">
				<div v-for="tag in transaction.tags" :key="tag.name">{{ tag.name }}</div>
			</div>
			<mdc-icon icon="add_circle" style="color: #AEAEB1;vertical-align: top;font-size: 64px;cursor: pointer"></mdc-icon>
			<button @click="$emit('link', transaction.id)">Link transactions</button>
		</div>
		<edit-target v-if="editTarget" @close="editTarget = false" @update="$emit('update'); fetchData()" :id="target.id" :predicted="transaction.raw" :parent="transaction.id" @click.stop></edit-target>
		<button v-if="link !== null" @click="link_transaction()">LINK</button>
	</div>
</template>

<script>
import moment from "moment/moment";
import axios from "axios/index";
import EditTarget from "@/components/transactions/EditTarget";

export default {
	name: "TransactionSegment",
	props: ["data", 'link'],
	components: { EditTarget },
	data() {
		return {
			active: false,
			editTarget: false,
			editMethod: false,
			transaction: this.data
		};
	},
	methods: {
		numberWithCommas(x) {
			return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		},
		fetchData() {
			axios.get(window.APIROOT + "api/transaction/" + this.transaction.id).then(response => {
				this.transaction = response.data;
			});
		},
		activate() {
			this.active = !this.active;
			if (this.active) {
				this.fetchData();
				this.$router.push({ params: { transactionId: this.transaction.id } });
			} else {
				this.$router.push({ params: { transactionId: null } });
			}
		},
		activateTarget() {
			this.editTarget = true;
			/*this.$router.push({params: {edit: 'target'}})
				  EventBus.$on('edit/close', () => {
					this.fetchData()
				  })*/
		},
		activateMethod() {
			this.editMethod = true
		},
		link_transaction() {
			axios.post(window.APIROOT + `api/transaction/${this.transaction.id}`, { parent: this.link }).then(response => {

			})
		}
	},
	computed: {
		truncateLength() {
			return this.$parent.$data.textTruncateLength;
		},
		name() {
			if (this.transaction.target){
				if (this.transaction.target.internal){
					if (this.transaction.amount < 0){
						return this.transaction.account.name + " -> " + this.transaction.target.name
					}
					else {
						return this.transaction.target.name + " -> " + this.transaction.account.name
					}

				}
				return this.transaction.target.name
			}
			return this.transaction.raw
		},
		target() {
			if (this.transaction.target){
				return this.transaction.target
			}
			else {
				return {
					internal: false,
					id: -1
				}
			}
		},
		addStyle() {
			if (this.active) {
				return {}; //{'height': this.$parent.$parent.$el.offsetHeight + 'px'}{'transform': 'translateY(' + -(this.$el.offsetTop - this.$parent.$el.offsetTop - this.$parent.$parent.$el.scrollTop) +'px)',
			}
			return {};
		},
		rightAddStyle() {
			if (this.active) {
				let style = window.getComputedStyle(this.$el.getElementsByClassName("right")[0]);
				//return {'padding-right': '100%'}
				//return {'padding-right': 'calc(50% - ' + parseInt(style.width) / 2 + 'px' + ')'}
			}
			return {};
		},
		rawStyle() {
			if (this.active) {
				//let ts = parseInt(window.getComputedStyle(this.$el.getElementsByClassName('raw')[0]).width) / (this.extra.raw.length * 2.2)  + 'vw'
				//return {'font-size': ts}
				return {};
			}
		},
		formatDate() {
			return moment(this.transaction.date).format("ddd, D MMM YYYY");
		}
	},
	mounted() {
		setTimeout(() => {
			if (this.$route.params.transactionId == this.transaction.id) {
				this.activate();
			}
		}, 250);
	}
};
</script>

<style scoped>
.colour {
	width: 5px;
	height: 48px;
	display: inline-block;
	top: 0;
	position: relative;
	transition: height, top;
	transition-duration: 0.2s;
}

.content {
	display: inline-block;
	height: 48px;
	vertical-align: top;
}

.sign {
	line-height: 48px;
	color: white;
}

.right {
	float: right;
	text-align: right;
	transition: top, right, transform, padding;
	transition-duration: 0.2s;
	right: 0;
	position: relative;
}

.left {
	-webkit-transform-origin-x: 0;
	transition: top, padding, opacity;
	transition-duration: 0.2s;
	top: 0;
	position: relative;
}

.text {
	width: 10em;
	display: inline-block;
	transition: font-size;
	transition-duration: 0.2s;
}

.segment.active {
	height: 300px;
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
	font-size: 1.5em;
	width: fit-content;
}

.active .colour {
	width: 90%;
	height: 5px;
	display: block;
	top: 48px;
	position: relative;
	transition-property: width, height, top, margin-left;
	transition-duration: 0.2s;
	margin-left: 5%;
}

.raw {
	width: 100%;
}

.target {
	font-size: 1.5em !important;
	cursor: pointer;
}

.extra {
	padding: 1% 5% 1% 5%;
	font-size: 80%;
}

.segment {
	padding-bottom: 10px;
	padding-top: 10px;
	border-bottom: 1px solid #32333d;
	height: 52px;
	transition: height, transform;
	will-change: height;
	transition-duration: 0.2s;
	z-index: 0;
	background: rgb(55, 55, 64);
}

.segment.active {
	z-index: 10;
}

.mdc-typography--headline6 {
	font-family: "Roboto Condensed";
	font-size: 1em;
	color: white;
	display: block;
	letter-spacing: 0.04em;
	line-height: 26px;
}

.mdc-typography--headline4 {
	font-family: "Eczar";
	color: white;
	letter-spacing: 0.05em;
	line-height: 48px;
	font-size: 212.5%;
}

.mdc-typography--subtitle2 {
	font-family: "Roboto Condensed";
	font-size: 0.875em;
	color: #aeaeb1;
	letter-spacing: 0.05em;
	line-height: 24px;
}

.segment {
	font-size: 16px;
}

@media screen and (min-width: 320px) {
	.segment {
		font-size: calc(12px + 4 * ((100vw - 320px) / 1600));
	}
}

@media screen and (min-width: 1920px) {
	.segment {
		font-size: 16px;
	}
}

/*@media (max-width: 1640px) and (min-width: 1480px) {
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
		}*/

/* Tablet */

/*@media (max-width: 660px) and (min-width: 590px) {
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
		}*/

/* Phone */

/*@media (max-width: 479px) and (min-width: 320px) {
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
		} */
</style>
