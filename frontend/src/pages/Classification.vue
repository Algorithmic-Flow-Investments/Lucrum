<template>
	<b-tabs v-model="activeTab" destroy-on-hide expanded>
		<b-tab-item>
			<template slot="header">
				<span>Transactions</span><b-tag>{{untargeted_transactions}}</b-tag>
			</template>
			<list ref="transactions" :range="range" :target_id="-1" @loaded="get_untargeted_transactions()"></list>
		</b-tab-item>
		<b-tab-item>
			<template slot="header">
				<span>Targets</span>
			</template>
			<targets></targets>
		</b-tab-item>
		<b-tab-item>
			<template slot="header">
				<span>Tags</span>
			</template>
			<tags></tags>
		</b-tab-item>
	</b-tabs>
</template>

<script>
	import List from "@/components/transactions/List";
	import moment from "moment";
	import BTabItem from "buefy/src/components/tabs/TabItem";
	import Targets from "@/components/classification/Targets";
	import Tags from "@/components/classification/Tags";
	export default {
		name: "Classification",
		components: { Tags, Targets, BTabItem, List },
		data() {
			return {
				range: {min: moment(0), max: moment()},
				activeTab: 0,
				untargeted_transactions: '...'
			}
		},
		methods: {
			get_untargeted_transactions(){
				if (this.$refs.transactions){
					this.untargeted_transactions = this.$refs.transactions.transactions.length
				}
			}
		}
	};
</script>

<style scoped>

	/deep/ .sect {
		max-height: calc(100vh - 24px - 42px - 32px);
	}

</style>
