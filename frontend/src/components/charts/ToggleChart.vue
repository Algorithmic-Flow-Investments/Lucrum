<template>
	<div class="wrapper">
		<span class="one" :class="{selected: value}" @click="$emit('input', true)"><i :class="'fas fa-' + one"></i></span>
		<span class="middle" @click="selectingBudget=!selectingBudget" v-if="budget_id">{{ budget.name }}</span>
		<div class="budget" v-for="bud in budgets" v-if="selectingBudget && bud.id !== budget.id" :key="bud.id" @click="selectBudget(bud.id)">{{ bud.name }}</div>
		<span class="two" :class="{selected: !value}" @click="$emit('input', false)"><i :class="'fas fa-' + two"></i></span>
	</div>
</template>

<script>
	import * as requests from "@/helpers/requests"

	export default {
		name: "ToggleChart",
		props: ['value', 'one', 'two'],
		data() {
			return {
				budget_id: this.$route.params.budget_id || null,
				budgets: [],
				selectingBudget: false
			}
		},
		methods: {
			fetch() {
				requests.get('budgets/list').then(budgets => {
					this.budgets = budgets
					if (this.budget_id == null){
						this.selectBudget(this.budgets[0].id)
					}
					else {
						this.selectBudget(this.budgets.filter(b => b.id === this.budget.id)[0].id)
					}
				})
			},
			selectBudget(budget_id){
				this.budget_id = budget_id
				this.selectingBudget = false;
				this.$emit('budget', this.budget_id)
				this.$router.push({ query: Object.assign({}, this.$route.query, {budget_id: this.budget_id})})
			}
		},
		computed: {
			budget() {
				if (!this.budget_id) return null;
				return this.budgets.filter(budget => budget.id === this.budget_id)[0]
			}
		},
		created() {
			this.fetch()
		}
	};
</script>

<style scoped lang="scss">
	@import "../../assets/colours";

	.wrapper {
		font-size: 14px;
		width: fit-content;
		cursor: pointer;
		margin: 10px auto;
		border-radius: 20px;
		box-shadow: 0 0 2pt 1pt $primary;
		height: 2em;
		position: relative;
	}

	.one, .two {
		width: 3em;
		height: 2em;
		display: inline-block;
		border-collapse: separate;
		transition: background-color, color;
		transition-duration: .6s;
		line-height: 2em;
		text-align: center;
	}

	.middle {
		height: 2em;
		display: inline-block;
		//box-shadow: 0 0 2pt 1pt $primary;
		border-collapse: separate;
		line-height: 2em;
		text-align: center;
		padding: 0 5px;
		background-color: $primary;
		color: black;
		position: relative;
		min-width: 80px;
	}

	.one {
		border-bottom-left-radius: 20px;
		border-top-left-radius: 20px;
		border-right: 1px solid rgba(0, 0, 0, 0.1);
	}

	.two {
		border-bottom-right-radius: 20px;
		border-top-right-radius: 20px;
		border-left: 1px solid rgba(0, 0, 0, 0.1);
	}

	.selected {
		background-color: $primary;
		color: black;
	}

	.budget {
		position: absolute;
		padding: 5px;
		background: $primary;
		color: black;
		left: 50%;
		transform: translateX(-50%);
		width: fit-content;
		margin-top: 5px;
	}

	.budget:hover {
		color: nth($greens, 1)
	}

</style>
