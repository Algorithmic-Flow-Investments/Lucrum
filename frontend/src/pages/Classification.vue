<template>
	<b-tabs v-model="activeTab" destroy-on-hide expanded @change="switchTab">
		<b-tab-item>
			<template slot="header">
				<span>Transactions</span><b-tag>{{untargeted_transactions}}</b-tag>
			</template>
			<list ref="transactions" :range="range" :extra_params="{target_id: -1}" @loaded="get_untargeted_transactions()"></list>
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
	import * as requests from "@/helpers/requests";
	export default {
		name: "Classification",
		components: { Tags, Targets, BTabItem, List },
		data() {
			return {
				range: {min: moment(0), max: moment()},
				activeTab: 0,
				untargeted_transactions: '...',
				eventSource: null,
			}
		},
		methods: {
			get_untargeted_transactions(){
				if (this.$refs.transactions){
					this.untargeted_transactions = this.$refs.transactions.transactions.length
				}
			},
			switchTab(e) {
				let tab;
				switch (e) {
					case 0:
						tab = 'transactions'
						break;
					case 1:
						tab = 'targets'
						break;
					case 2:
						tab = 'tags'
						break;
				}
				this.$router.push({hash: tab})
			},
			// Events stuff
			eventsConnect() {
				this.eventSource = new EventSource(requests.api + 'subscribe')
				this.eventSource.onmessage = this.onEvent
			},
			onEvent(message) {
				let event = JSON.parse(message.data)
				switch (event.event) {
					case 'TRANSACTIONS_UPDATED':
						this.onTransactionsUpdated(event.value);
						break;
					case 'TARGETS_UPDATED':
						this.onTargetsUpdated(event.value);
						break;
				}
			},
			onTransactionsUpdated(transaction_ids) {
				this.$refs.transactions.onTransactionsUpdated(transaction_ids)
			},
			onTargetsUpdated(target_ids) {
				this.$refs.transactions.onTargetsUpdated(target_ids)
			}
		},
		created() {
			this.$store.dispatch('fetch_targets').then(() => {
				this.l_targets.forEach(target => target.fetch())
			})
			this.$store.dispatch('fetch_tags')
			this.$store.dispatch('fetch_categories')

			switch (this.$route.hash) {
				case '#transactions':
					this.activeTab = 0;
					break;
				case '#targets':
					this.activeTab = 1;
					break;
				case '#tags':
					this.activeTab = 2;
					break;
			}

			this.eventsConnect()
		},
		destroyed() {
			this.eventSource.close()
		}
	};
</script>

<style scoped>

	/deep/ .sect {
		max-height: calc(100vh - 24px - 42px - 32px);
	}

</style>
