<template>
	<div class="segment">
		<div class="colour" :style="{ background: colour }"></div>
		<div class="content left">
			<mdc-text typo="headline6" tag="span" adjust-margin>{{ title }}</mdc-text>
			<mdc-text typo="subtitle2" tag="span" adjust-margin>{{ subtitle }}</mdc-text>
		</div>

		<div class="content right">
			<div class="text">
				<mdc-text typo="headline4" tag="span" adjust-margin style="float:left">£</mdc-text>
				<mdc-text typo="headline4" tag="span" adjust-margin>{{ numberWithCommas(Math.abs(amount)) }}</mdc-text>
			</div>
			<mdc-icon icon="chevron_right" style="color: #AEAEB1;line-height: 48px;vertical-align: top;"></mdc-icon>
		</div>
		<mdc-icon v-if="internal" icon="compare_arrows" class="pre-right" style="font-size: 14px"></mdc-icon>
		<mdc-text v-else-if="amount < 0" typo="headline4" tag="span" class="pre-right" adjust-margin>-</mdc-text>
	</div>
</template>

<script>
export default {
	name: "ListSegment",
	props: ["title", "subtitle", "colour", "amount", "internal"],
	methods: {
		numberWithCommas(x) {
			return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		}
	}
};
</script>

<style scoped>
.colour {
	width: 5px;
	height: 48px;
	display: inline-block;
}

.content {
	display: inline-block;
	height: 48px;
	vertical-align: top;
}

.pre-right {
	float: right;
	padding-right: 5px;
	line-height: 48px;
	color: white;
}

.right {
	float: right;
	text-align: right;
}

.left {
	-webkit-transform-origin-x: 0;
	font-size: 16px;
}

.text {
	width: 180px;
	display: inline-block;
	font-size: 16px;
}

.segment {
	padding-bottom: 10px;
	padding-top: 10px;
	border-bottom: 1px solid #32333d;
}

.mdc-typography--headline6 {
	font-family: "Roboto Condensed";
	font-size: 1.25em;
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
		font-size: 10px;
	}
}
</style>
