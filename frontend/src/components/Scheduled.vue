<template>
	<div>
		<list-segment
			v-for="transaction in scheduled"
			:key="scheduled.indexOf(transaction)"
			:colour="getColour(transaction)"
			:title="transaction.name"
			:subtitle="formatDate(transaction.date)"
			:amount="transaction.amount"
			:internal="transaction.internal"
		/>
	</div>
</template>

<script>
import ListSegment from "@/components/ListSegment";
import { EventBus } from "../event-bus.js";
import axios from "axios";
import moment from "moment";

function numberWithCommas(x) {
	return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export default {
	name: "Scheduled",
	components: {
		ListSegment
	},
	data() {
		return {
			total: 0,
			absTotal: 0,
			scheduled: [],
			types: {
				in: [],
				out: [],
				internal: []
			},
			colours: {
				out: ["#FF6859", "#FF857C", "#FFD7D0"],
				in: ["#FFDC78", "#FFEEBC"],
				internal: ["#789BFF"]
			},
			parent: {
				title: "",
				subtitle: "",
				chart: []
			}
		};
	},
	methods: {
		formatDate(date) {
			var date = moment(date);
			return date.format("dddd, MMMM Do");
		},
		getColour(transaction) {
			return this.colours[transaction.internal ? "internal" : transaction.amount > 0 ? "in" : "out"][
				this.types[transaction.internal ? "internal" : transaction.amount > 0 ? "in" : "out"].indexOf(transaction)
			];
		},
		fetchData() {
			axios.get(window.APIROOT + "api/scheduled").then(response => {
				this.scheduled = response.data;
				this.scheduled.sort(function(a, b) {
					return moment(a.date).unix() - moment(b.date).unix();
				});
				this.types = {
					in: this.scheduled.filter(function(item) {
						return item.amount > 0 && !item.internal;
					}),
					out: this.scheduled.filter(function(item) {
						return item.amount < 0 && !item.internal;
					}),
					internal: this.scheduled.filter(function(item) {
						return item.internal;
					})
				};
				this.total = this.scheduled.reduce(function(total, cur) {
					console.log(total, cur);
					return total + cur.amount;
				}, 0);

				this.absTotal = this.scheduled.reduce(function(total, cur) {
					console.log(total, cur);
					return total + Math.abs(cur.amount);
				}, 0);
				var parent = {
					title: "Scheduled",
					subtitle: "£" + numberWithCommas(this.total),
					chart: this.scheduled.map(
						function(cur, index) {
							return [(Math.abs(cur.amount) / this.absTotal) * 100, this.getColour(cur)];
						}.bind(this)
					)
				};
				EventBus.$emit("loaded/scheduled", parent);
			});
		}
	},
	mounted() {
		this.fetchData();
	}
};
</script>

<style scoped></style>
