<template>
	<div>
		<list-segment
			v-for="account in accounts"
			:key="accounts.indexOf(account)"
			:colour="colours[accounts.indexOf(account)]"
			:title="account.name"
			:subtitle="account.description"
			:amount="account.balance"
		/>
	</div>
</template>

<script>
import ListSegment from "@/components/ListSegment";
import { EventBus } from "../event-bus.js";
import axios from "axios";

function numberWithCommas(x) {
	return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export default {
	name: "Accounts",
	components: {
		ListSegment
	},
	data() {
		return {
			total: 0,
			accounts: [],
			colours: ["#005d57", "#007d51", "#1eb980", "#37efba"],
			parent: {
				title: "",
				subtitle: "",
				chart: []
			}
		};
	},
	methods: {
		fetchData() {
			axios.get(window.APIROOT + "api/accounts").then(response => {
				this.accounts = response.data;
				this.total = this.accounts.reduce(function(total, cur) {
					console.log(total, cur);
					return total + cur.balance;
				}, 0);
				var parent = {
					title: "Accounts",
					subtitle: "£" + numberWithCommas(this.total),
					chart: this.accounts.map(
						function(cur, index) {
							return [(cur.balance / this.total) * 100, this.colours[index]];
						}.bind(this)
					)
				};
				EventBus.$emit("loaded/accounts", parent);
			});
		}
	},
	created() {
		this.fetchData();
		//APIROOT
		//load from server
		/*this.accounts = [
			{ name: "123 Santander", number: "0456", amount: 1637 },
			{ name: "Regular Saver", number: "0456", amount: 2736 },
			{ name: "Limited Access", number: "0456", amount: 27000 }
		];*/
	}
};
</script>

<style scoped></style>
