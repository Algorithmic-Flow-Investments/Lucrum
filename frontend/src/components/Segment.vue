<template>
	<div class="segment" :class="{ active }">
		<div class="normal" @click="activate()">
			<div class="colour" :class="colour"></div>
			<div class="content">
				<div class="left">
					<div class="main">{{ title }}</div>
					<div class="sub">{{ subtitle }}</div>
				</div>
				<div class="right">
					<span class="sign">
						<span v-if="amount < 0 && !internal">-</span>
						<span v-else class="nosign">-</span>
					</span>
					<span class="currency money">
						£
					</span>
					<span class="amount money">
						{{ Math.abs(amount) | numberWithCommas }}
					</span>
				</div>
			</div>
		</div>
		<div v-if="active" class="extra">
			<slot></slot>
		</div>
	</div>
</template>

<script>
export default {
	name: "Segment",
	props: {
		colour: String,
		amount: Number,
		title: String,
		subtitle: String,
		internal: {
			type: Boolean,
			default: false
		}
	},
	data() {
		return {
			active: false
		};
	},
	filters: {
		numberWithCommas(x) {
			return x
				.toFixed(2)
				.toString()
				.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		}
	},
	methods: {
		activate() {
			if (this.$slots.default) {
				this.active = !this.active;
				if (this.active) {
					this.$emit("activate");
				} else {
					this.$emit("deactivate");
				}
			}
		}
	}
};
</script>

<style scoped lang="scss">
@import "../assets/colours";

$duration: 0.4s;

.segment {
	padding-bottom: 10px;
	padding-top: 10px;
	height: calc(50px + 10px + 10px);
	transition: height, transform;
	will-change: height;
	transition-duration: $duration;
	z-index: 0;
	background: rgb(55, 55, 64);
	position: relative;
}

.segment:not(:last-child) {
	border-bottom: 1px solid #32333d;
}

.segment:last-child {
	padding-bottom: 0;
}

.colour {
	width: 5px;
	height: 50px;
	display: inline-block;
	top: 10px;
	position: absolute;
	transition: width, height, top, margin-left;
	transition-duration: $duration;
}

.content {
	display: inline-block;
	width: calc(100% - 5px - 5px - 10px);
	height: 50px;
	vertical-align: top;
	line-height: normal;
	color: $text-strong;
	margin-left: 10px;
	margin-right: 5px;
	transition: opacity calc(#{$duration} / 2) calc(#{$duration} / 2), width calc(#{$duration} * 0.45) calc(#{$duration} * 0.55);
}

.left {
	display: inline-block;
	width: 65%;
	transition: opacity 0.2s $duration, width 0s $duration;
}

.right {
	display: inline-block;
	vertical-align: top;
	width: 30%;
	min-width: 180px;
	max-width: 230px;
	font-size: 32px;
	float: right;
	right: 0;
	transition: right, transform;
	transition-duration: $duration;
	position: relative;
}

.amount {
	float: right;
	line-height: 50px;
}

.currency {
	line-height: 50px;
}

.nosign {
	visibility: hidden;
}

.main {
	font-size: 24px;
	height: 30px;
	line-height: 30px;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
	width: 100%;
}

.sub {
	font-size: 18px;
	color: $text;
	height: 20px;
	line-height: 20px;
	width: 100%;
}

/* Active */

.active.segment {
	height: calc(50px + 10px + 10px + 150px);
	z-index: 10;
}

.active .left {
	opacity: 0;
	width: 0;
	transition: opacity 0s;
}

.active .right {
	right: 50%;
	transform: translateX(50%) scale(1.8);
	min-width: 0;
	width: auto;
}

.active .colour {
	width: 90%;
	height: 5px;
	display: block;
	top: 58px;
	transition-property: width, height, top, margin-left;
	transition-duration: $duration;
	margin-left: 5%;
}

.extra {
	margin-top: 5px;
}
</style>
