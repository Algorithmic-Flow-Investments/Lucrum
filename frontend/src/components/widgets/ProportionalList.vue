<template>
	<div class="sect">
		<proportional-header :title="title" :total="total" :chart="chart"></proportional-header>
		<segment v-for="(item, i) in items" :title="item.name" :subtitle="item.description" :amount="item.balance" :colour="'seg-' + (i % 4 + 1)" :key="item.id"></segment>
	</div>
</template>

<script>
import Segment from "@/components/Segment";
import ProportionalHeader from "@/components/widgets/ProportionalHeader";

export default {
	name: "ProportionalList",
	props: ["title", "items"],
	components: { ProportionalHeader, Segment },
	computed: {
		total() {
			return this.items.reduce((total, item) => {
				return total += item.balance
			}, 0)
		},
		chart() {
			return this.items.map((item, i) => {
				return [item.balance / this.total * 100, 'seg-' + (i % 4 + 1)]
			})
		}
	}
};
</script>

<style scoped lang="scss">
.sect {
	padding-bottom: 5px;
}
</style>
