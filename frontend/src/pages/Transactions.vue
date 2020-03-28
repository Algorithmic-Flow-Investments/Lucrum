<template>
	<div class="columns">
		<div class="column is-5">
			<date-select v-model="range" :target="targetDate" @input="update()"/>
			<chart-wrapper ref="chart" :stats="stats" :range="range" :top="topTransaction" @budget="setBudget" @tagcat="setTagCat"/>
			<stats :stats="stats" />
		</div>
		<div class="column is-7">
			<list ref="list" :range="range" @scroll="topTransaction=$event" :extra_params="extra_params" /> <!--:categories="budget.categories"-->
		</div>
	</div>
</template>

<script>
import ChartWrapper from "@/components/transactions/charts/ChartWrapper";
import Stats from "@/components/transactions/Stats";
import List from "@/components/transactions/List";
import DateSelect from "@/components/transactions/DateSelect";

import * as requests from "@/helpers/requests"
import moment from "moment";

export default {
	name: "Transactions",
	components: { DateSelect, List, Stats, ChartWrapper },
	data() {
		return {
			range: { min: null, max: null },
			targetDate: null,
			topTransaction: null,
			stats: null,
			budget_id: null,
			account_id: this.$route.query.account_id || null,
			eventSource: null,
			tagCat: {cat_id: null, tag_id: null}
		};
	},
	methods: {
		update() {
			this.$nextTick(() => {
				this.$refs.list.fetch();
				this.$refs.chart.fetch();
				this.fetch()
			})
		},
		fetch() {
			if (this.range.min === null || this.range.max === null) return;
			requests.get('transactions/stats', {
				params: {
					min: this.range.min.format("YYYY-M-D"),
					max: this.range.max.format("YYYY-M-D"),
					budget: this.budget_id
				}
			}).then(data => {
				this.stats = data
			})
		},
		setBudget(budget_id){
			this.budget_id = budget_id
			this.update()
		},
		setTagCat(selected){
			this.tagCat = selected
			this.update()
		},
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
			this.$refs.list.onTransactionsUpdated(transaction_ids)
		},
		onTargetsUpdated(target_ids) {
			this.$refs.list.onTargetsUpdated(target_ids)
		}
	},
	computed: {
		extra_params() {
			let params = {}
			if (this.budget_id) params.budget_id = this.budget_id
			if (this.account_id) params.account_id = this.account_id
			if (this.tagCat.cat_id) params.category_id = this.tagCat.cat_id
			if (this.tagCat.tag_id) params.tag_id = this.tagCat.tag_id
			return params;
		}
	},
	created() {
		this.fetch()
		this.targetDate = moment(this.$route.query.date)
		this.eventsConnect()
	},
	destroyed() {
		this.eventSource.close()
	}
};
</script>

<style scoped></style>
