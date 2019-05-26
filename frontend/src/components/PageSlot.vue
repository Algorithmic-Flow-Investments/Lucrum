<template>
	<div class="outer">
		<mdc-text typo="subtitle1" tag="span" adjust-margin>{{ title }}</mdc-text>
		<br />
		<mdc-text typo="headline3" tag="span" adjust-margin>{{ subtitle }}</mdc-text>
		<br />
		<line-chart :data="chart" />
		<slot></slot>
	</div>
</template>

<script>
import LineChart from "@/components/LineChart";
import { EventBus } from "../event-bus.js";

export default {
	name: "PageSlot",
	props: ["child"],
	components: { LineChart },
	data() {
		return {
			title: "",
			subtitle: "",
			chart: []
		};
	},
	created() {
		EventBus.$on("loaded/" + this.child, data => {
			this.title = data.title;
			this.subtitle = data.subtitle;
			this.chart = data.chart;
		});
	}
};
</script>

<style scoped>
.outer {
	background: #373740;
	height: 380px;
	padding: 20px;
}

.mdc-typography--headline3 {
	font-family: "Eczar", serif;
	color: white;
}

.mdc-typography--subtitle1 {
	font-family: "Roboto Condensed", sans-serif;
	color: white;
}

@media (max-width: 479px) {
	.outer {
		padding: 10px;
	}
}
</style>
